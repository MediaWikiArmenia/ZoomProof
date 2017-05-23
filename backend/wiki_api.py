import requests
import config

def query_file_information(file_sha1):
  """using the wikicommons API to query for file info based on the file sha1"""

  api_base_url = 'https://commons.wikimedia.org/w/api.php?'

  headers = {
    'User-Agent': config.server['user_agent']
  }
  payload = {
    'action': 'query',
    'format': 'json',
    'servedby': 1,                    #return response server name for potential logging
    'list': 'allimages',              #using the allimages API
    'aiprop': 'dimensions|mime|url',  #file properties we want to have returned
    'aisha1': file_sha1               #specifying the file by sha1 checksum
  }

  r = requests.get(api_base_url, headers=headers, params=payload)

  #return as a JSON object
  return r.json()

def process_query_response(response):
  """process the JSON information about a file returned from the API"""
  #if we got an error 
  if 'error' in response:
    return {'error': response['error']['info']}
  else:
    fileinfo = dict()
    info = response['query']['allimages'][0]

    fileinfo['response_server'] = response['servedby']
    fileinfo['filename'] = info['name']
    fileinfo['pagecount'] = info['pagecount']
    fileinfo['url'] = info['url']
    fileinfo['mime'] = info['mime']

    return fileinfo
