from flask import Flask, jsonify, render_template
from celery import Celery
from redis import Redis
import data_ops
from process_request_djvu import DJVURequestProcessor
from process_request_pdf import PDFRequestProcessor
from logger import log_info, log_error, get_latest_log_messages
import config

#ALTER REDIS HOSTNAME BETWEEN LOCAL AND PRODUCTION HERE (check config.py)
redis_hostname = config.server['redis_hostname_production']
redis_port = config.server['redis_port']

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['CELERY_BROKER_URL'] = 'redis://{}:{}/0'.format(redis_hostname, redis_port)
app.config['CELERY_RESULT_BACKEND'] = 'redis://{}:{}/0'.format(redis_hostname, redis_port)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

redis = Redis(host=redis_hostname, port=redis_port)
redis.delete('zoomproof_processing')

djvu_processor = DJVURequestProcessor()
pdf_processor = PDFRequestProcessor()

def set_no_cache(response):
  """set the header of this response to no-cache"""
  response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response.headers['Pragma'] = 'no-cache'

def get_celery_status():
  """return None if celery is unavailable, return list of currently queued tasks if it is"""
  return celery.control.inspect().active()

@app.route('/')
def index():
  """return an index.html file as a README description of the tool
     and showing the latest (define in config) messages from the error and info log"""
  latest_errors, latest_infos = get_latest_log_messages()
  return render_template('index.html', latest_errors=latest_errors, latest_infos=latest_infos)

@app.route('/status')
def status():
  """return a short status text describing whether celery is active or not"""
  celery_status = get_celery_status()
  if celery_status is None:
    return "Celery is down."
  else:
    return "Celery is up. <br/><br/> task queue: <br/>" + str(celery_status)

@app.route('/djvujson/<string:sha1>/<int:page>.json')
def request_page_djvu(sha1, page):
  return request_page(sha1, page, djvu_processor, 'djvu')

@app.route('/pdfjson/<string:sha1>/<int:page>.json')
def request_page_pdf(sha1, page):
  return request_page(sha1, page, pdf_processor, 'pdf')

def request_page(sha1, page, processor, filetype):
  #check if the desired page is already cached
  if processor.page_is_cached(sha1, page):
    return jsonify(processor.return_cached_page(sha1, page))
  #if it is not yet cached
  #check if celery is active
  elif get_celery_status() is None:
    response = jsonify(processor.build_error_response("Celery is not active."))
    log_error(error_msg="Celery is not active.")
    set_no_cache(response)
    return response
  else:
    error_json, fileinfo = processor.sanity_check_request(sha1, page)
    #when something is not right with the request, return an error
    if error_json:
      return jsonify(error_json)
    #when the request is valid
    else:
      #asynchronous call to invoke processing the file
      process_request_async.delay(sha1, page, fileinfo, filetype)
      response = jsonify(processor.build_error_response("Processing the file, check back in a minute."))
      set_no_cache(response)
      return response

@celery.task(name='process_request_async')
def process_request_async(sha1, page, fileinfo, filetype):
  """Background task to process a file in a non-blocking way."""
  #we are maintaining a redis set with all sha1s we are currently converting
  #if we are trying to trigger the same conversion twice, it will simply return here
  #on the second attempt
  if redis.sismember('zoomproof_processing', sha1):
    return

  #add this sha1 to the redis set
  redis.sadd('zoomproof_processing', sha1)
  if filetype == 'djvu':
    djvu_processor.invoke_conversion(sha1, page, fileinfo)
  elif filetype == 'pdf':
    pdf_processor.invoke_conversion(sha1, page, fileinfo)
  #remove this sha1 from the redis set once done
  redis.srem('zoomproof_processing', sha1)
