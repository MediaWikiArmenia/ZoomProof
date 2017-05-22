from flask import Flask
from flask import jsonify
import process_request
import data_ops

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/<string:sha1>/<int:page>')
def request_page(sha1, page):
  if data_ops.json_page_is_cached(sha1, page):
    return jsonify(data_ops.get_cached_json_page(sha1, page))
  else:
    #TODO spawn new unblocking process here
    return jsonify(process_request.page_request(sha1, page))
