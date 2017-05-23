from flask import Flask, jsonify
from celery import Celery
from redis import Redis
import process_request
import data_ops
import logger
import config

#ALTER REDIS HOSTNAME BETWEEN LOCAL AND PRODUCTION HERE (check config.py)
redis_hostname = config.server['redis_hostname_production']
redis_port = config.server['redis_port']

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://{}:{}/0'.format(redis_hostname, redis_port)
app.config['CELERY_RESULT_BACKEND'] = 'redis://{}:{}/0'.format(redis_hostname, redis_port)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

redis = Redis(host=redis_hostname, port=redis_port)
redis.delete('zoomproof_processing')

logger.init_loggers()

@app.route('/<string:sha1>/<int:page>')
def request_page(sha1, page):
  #check if the desired page is already cached
  if data_ops.json_page_is_cached(sha1, page):
    logger.log_info(sha1, page, "Page succesfully returned.")
    return jsonify(data_ops.get_cached_json_page(sha1, page))
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
      return jsonify(process_request.build_error_response("Processing the file, check back in a minute."))

@celery.task
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
