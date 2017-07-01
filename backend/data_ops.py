import os
import json
import config
import requests

def save_json_page(json_object, file_sha1, page, datadir):
  """save the JSON object for this page from the file with file_sha1 in
     'datadir/file_sha1/page.json' """
  #create data directory for that file if necessary
  if not os.path.exists(datadir + file_sha1):
    os.makedirs(datadir + file_sha1)

  #save json file
  with open('{}{}/{}.json'.format(datadir, file_sha1, page), 'w', encoding='utf-8') as json_file:
    #create a JSON string, allowing utf-8 characters, compact version without whitespace
    json_string = json.dumps(json_object, ensure_ascii=False, separators=(',', ':'))
    json_file.write(json_string)

def json_page_is_cached(file_sha1, page, datadir):
  """check if the processed JSON for the page in that file is already available"""
  return os.path.isfile('{}{}/{}.json'.format(datadir, file_sha1, page))

def get_cached_json_page(file_sha1, page, datadir):
  """return the cached json page"""
  with open('{}{}/{}.json'.format(datadir, file_sha1, page), 'r', encoding='utf-8') as json_file:
    return json.load(json_file)

def download_file(url, filename):
  """download the file at the given url"""
  if os.path.isfile(config.server['tmpdir'] + filename):
    return
  else:
    r = requests.get(url, stream=True)
    with open(config.server['tmpdir'] + filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024): 
        if chunk:
          f.write(chunk)

def clean_up(filename):
  """remove the file that was downloaded before"""
  os.remove(config.server['tmpdir'] + filename)
