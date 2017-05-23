from flask import Flask, jsonify
from celery import Celery
import process_request
import data_ops

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/<string:sha1>/<int:page>')
def request_page(sha1, page):
  if data_ops.json_page_is_cached(sha1, page):
    return jsonify(data_ops.get_cached_json_page(sha1, page))
  else:
    #asynchronous call to invoke processing the file
    process_request_async.delay(sha1, page)
    return jsonify(process_request.build_error_response("Check back in a minute"))

@celery.task
def process_request_async(sha1, page):
  """Background task to process a djvu file in a non-blocking way."""
  print("test")
  process_request.page_request(sha1, page)
