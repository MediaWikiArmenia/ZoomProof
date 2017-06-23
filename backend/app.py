from flask import Flask, jsonify, render_template
from celery import Celery
from redis import Redis
import process_request
import data_ops
from logger import log_info, get_latest_log_messages
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

def set_no_cache(response):
  """set the header of this response to no-cache"""
  response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response.headers['Pragma'] = 'no-cache'

@app.route('/')
def index():
  """return an index.html file as a README description of the tool
     and showing the latest (define in config) messages from the error and info log"""
  latest_errors, latest_infos = get_latest_log_messages()
  return render_template('index.html', latest_errors=latest_errors, latest_infos=latest_infos)

@app.route('/djvujson/<string:sha1>/<int:page>.json')
def request_page(sha1, page):
  #check if the desired page is already cached
  #NOTE: this is actually not required within the current app configuration...
  #...because atm the nginx server serves the cached file if available and...
  #...redirects to the flask app only if no cached file is available
  if data_ops.json_page_is_cached(sha1, page):
    return return_cached_page_json(sha1, page)
  #if it is not yet cached
  else:
    error_json, fileinfo = process_request.sanity_check_request(sha1, page)
    #when something is not right with the request, return an error
    if error_json:
      return jsonify(error_json)
    #when the request is valid
    else:
      #asynchronous call to invoke processing the file
      process_request_async.delay(sha1, page, fileinfo)
      response = jsonify(process_request.build_error_response("Processing the file, check back in a minute."))
      set_no_cache(response)
      return response

def return_cached_page_json(sha1, page):
  """return json of the cached page"""
  #NOTE: as of now the logger won't log the correct filename here (because we won't know it at this point)
  #but this is not an issue because the webserver will usually serve the static .json files once processed
  log_info(sha1, "", page, "Page succesfully returned.")
  return jsonify(data_ops.get_cached_json_page(sha1, page))

@celery.task(name='process_request_async')
def process_request_async(sha1, page, fileinfo):
  """Background task to process a djvu file in a non-blocking way."""
  #we are maintaining a redis set with all sha1s we are currently converting
  #if we are trying to trigger the same conversion twice, it will simply return here
  #on the second attempt
  if redis.sismember('zoomproof_processing', sha1):
    return

  #add this sha1 to the redis set
  redis.sadd('zoomproof_processing', sha1)
  process_request.invoke_conversion(sha1, page, fileinfo)
  #remove this sha1 from the redis set once done
  redis.srem('zoomproof_processing', sha1)
