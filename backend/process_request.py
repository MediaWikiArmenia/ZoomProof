import os
import json
from collections import OrderedDict
import djvu_to_xml
from xml_to_json import XMLToJSON
import wiki_api
import data_ops
from logger import log_error, log_info
import config

def build_error_response(error_text):
  """if for some reason we can't return the desired page as JSON
     we want to return a custom error response in the same format"""
  return OrderedDict([
    ('errors', error_text),
    ('size', {}),
    ('statistics', {}),
    ('map', [])
  ])

def process_single_page(fileinfo, file_sha1, page):
  """process a single page:
     - convert to xml from .djvu file
     - convert xml to JSON
     - save JSON as file in appropriate path"""
  xml_string = djvu_to_xml.convert_from_file(config.server['tmpdir'] + fileinfo['filename'], page)
  json_object = XMLToJSON().convert_from_string(xml_string)
  data_ops.save_json_page(json_object, file_sha1, page)

def sanity_check_request(file_sha1, page):
  """check the request against common errors:
     - file can't be found in wiki commons?
     - file is not a djvu?
     - requested page is > than file pagecount? """
  #get file information from the wikicommons API
  response = wiki_api.query_file_information(file_sha1)
  fileinfo = wiki_api.process_query_response(response)

  try:
    filename = fileinfo['filename']
  except:
    filename = 'unknown filename'

  #if fileinfo came back from the wiki commons API with an error or empty
  if 'error' in fileinfo:
    error_msg = fileinfo['error']
    log_error(file_sha1, filename, page, error_msg)
    return build_error_response(error_msg), {}
  #if the file is not a .djvu
  elif 'djvu' not in fileinfo['mime'].lower():
    error_msg = "Not a valid djvu file."
    log_error(file_sha1, filename, page, error_msg)
    return build_error_response(error_msg), {}
  #if the desired page is greater than the maximum page in the file
  elif page > fileinfo['pagecount'] or page < 1:
    error_msg = "Page doesn't exist."
    log_error(file_sha1, filename, page, error_msg)
    return build_error_response(error_msg), {}
  else:
    return {}, fileinfo

def invoke_conversion(file_sha1, page, fileinfo):
  """entry point for processing a valid request 
     by sha1 checksum for the file, a page number and the fileinfo dictionary"""

  #download the .djvu file
  data_ops.download_djvu_file(fileinfo['url'], fileinfo['filename'])
  log_info(file_sha1, fileinfo['filename'], None, "Succesfully downloaded .djvu file.")

  #first convert the desired page and the -cache_before and +cache_after pages around it
  for p in range(page - config.server['cache_before'], page + config.server['cache_after'] + 1):
    if p > 1 and p <= fileinfo['pagecount']:
      process_single_page(fileinfo, file_sha1, p)
  #then convert all other pages from that file
  for p in range(1, fileinfo['pagecount'] + 1):
    if not data_ops.json_page_is_cached(file_sha1, p):
      process_single_page(fileinfo, file_sha1, p)

  data_ops.clean_up(fileinfo['filename'])
  log_info(file_sha1, fileinfo['filename'], None, "Succesfully converted .djvu file.")
