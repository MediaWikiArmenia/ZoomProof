import os
import json
import config

def save_json_page(json_object, file_sha1, page):
  """save the JSON object for this page from the file with file_sha1 in
     'datadir/file_sha1/page.json' """
  #create data directory for that file if necessary
  if not os.path.exists(config.server['datadir'] + file_sha1):
    os.makedirs(config.server['datadir'] + file_sha1)

  #save json file
  with open('{}{}/{}.json'.format(config.server['datadir'], file_sha1, page), 'w', encoding='utf-8') as json_file:
    json_file.write(json.dumps(json_object, ensure_ascii=False))

def json_page_is_cached(file_sha1, page):
  """check if the processed JSON for the page in that file is already available"""
  return os.path.isfile('{}{}/{}.json'.format(config.server['datadir'], file_sha1, page))

def get_cached_json_page(file_sha1, page):
  """return the cached json page"""
  with open('{}{}/{}.json'.format(config.server['datadir'], file_sha1, page), 'r', encoding='utf-8') as json_file:
    return json.load(json_file)

def download_djvu_file(url, filename):
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
  """remove the .djvu file that was downloaded before"""
  os.remove(config.server['tmpdir'] + filename)
