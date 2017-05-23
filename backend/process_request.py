import os
import json
import djvu_to_xml
import xml_to_json
import wiki_api
import data_ops
import config

#TODO refactor

def build_error_response(error_text):
  """if for some reason we can't return the desired page as JSON
     we want to return a custom error response in the same format"""
  return {
    'errors': error_text,
    'map': []
  }

def process_single_page(fileinfo, file_sha1, page):
  """process a single page:
     - convert to xml from .djvu file
     - convert xml to JSON
     - save JSON as file in appropriate path"""
  xml_string = djvu_to_xml.convert_from_file(config.server['tmpdir'] + fileinfo['filename'], page)
  json_object = xml_to_json.convert_from_string(xml_string)
  data_ops.save_json_page(json_object, file_sha1, page)

def sanity_check_request(file_sha1, page):
  """check the request against common errors:
     - page number negative?
     - file can't be found in wiki commons?
     - file is not a djvu?
     - requested page is > than file pagecount? """
  #TODO file can't be found in wiki commons
  if page < 1:
    return build_error_response("Negative page number"), {}

  #get file information from the wikicommons API
  response = wiki_api.query_file_information(file_sha1)
  fileinfo = wiki_api.process_query_response(response)

  if 'djvu' not in fileinfo['mime']:
    return build_error_response("Not a valid djvu file."), {}
  elif page > fileinfo['pagecount']:
    return build_error_response("Page doesn't exist."), {}
  else:
    return {}, fileinfo

def invoke_conversion(file_sha1, page, fileinfo):
  """entry point for processing a valid request 
     by sha1 checksum for the file, a page number and the fileinfo dictionary"""

  #download the .djvu file
  data_ops.download_djvu_file(fileinfo['url'], fileinfo['filename'])

  #first convert the +-3 around the desired page
  for p in range(page-3, page+4):
    if not p < 1 or p > fileinfo['pagecount']:
      process_single_page(fileinfo, file_sha1, p)
  #then convert all the rest from that file
  for p in range(1, fileinfo['pagecount'] + 1):
    if not data_ops.json_page_is_cached(file_sha1, p):
      process_single_page(fileinfo, file_sha1, p)

  data_ops.clean_up(fileinfo['filename'])

  return build_error_response("Building desired page, check back in a minute.")
