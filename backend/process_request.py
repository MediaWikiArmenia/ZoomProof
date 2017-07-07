from collections import OrderedDict
import wiki_api
import data_ops
from logger import log_error, log_info
import config

class RequestProcessor:
  def __init__(self):
    """initialize"""
    pass

  def build_error_response(self, error_text, error_type):
    """if for some reason we can't return the desired page as JSON
       we want to return a custom error response in the same format"""
    return OrderedDict([
      ('errors', "Error {}, {}".format(str(error_type), error_text)),
      ('size', {}),
      ('statistics', {}),
      ('map', [])
    ])

  def page_is_cached(self, sha1, page):
    """return True if that page for that sha1 is already cached"""
    return data_ops.json_page_is_cached(sha1, page, self.datadir)

  def return_cached_page(self, sha1, page):
    """return the cached JSON page"""
    log_info(sha1, "", page, "Page succesfully returned.")
    return data_ops.get_cached_json_page(sha1, page, self.datadir)

  def sanity_check_request(self, file_sha1, page):
    """check the request against common errors:
       - file can't be found in wiki commons?
       - file is not of the right type?
       - requested page is > than file pagecount?"""
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
      return self.build_error_response(error_msg, 1), {}
    #if the file does not have the right mime type
    elif self.filetype not in fileinfo['mime'].lower():
      error_msg = "Not a valid {} file.".format(self.filetype)
      log_error(file_sha1, filename, page, error_msg)
      return self.build_error_response(error_msg, 2), {}
    #if the desired page is greater than the maximum page in the file
    elif page > fileinfo['pagecount'] or page < 1:
      error_msg = "Page doesn't exist."
      log_error(file_sha1, filename, page, error_msg)
      return self.build_error_response(error_msg, 3), {}
    else:
      return {}, fileinfo

  def invoke_conversion(self, file_sha1, page, fileinfo):
    """entry point for processing a valid request 
       by sha1 checksum for the file, a page number and the fileinfo dictionary"""
    log_info(file_sha1, fileinfo['filename'], None, "Starting new task to download and convert the file.")
    #download the file
    data_ops.download_file(fileinfo['url'], fileinfo['filename'])
    log_info(file_sha1, fileinfo['filename'], None, "Succesfully downloaded file.")

    #first convert the desired page and the -cache_before and +cache_after pages around it
    for p in range(page - config.server['cache_before'], page + config.server['cache_after'] + 1):
      if p > 1 and p <= fileinfo['pagecount']:
        self.process_single_page(fileinfo, file_sha1, p)
    #then convert all other pages from that file
    for p in range(1, fileinfo['pagecount'] + 1):
      if not data_ops.json_page_is_cached(file_sha1, p, self.datadir):
        self.process_single_page(fileinfo, file_sha1, p)

    data_ops.clean_up(fileinfo['filename'])
    log_info(file_sha1, fileinfo['filename'], None, "Succesfully converted file to JSON.")

  def process_single_page(self, fileinfo, file_sha1, page):
    """process a single page"""
    raise NotImplementedError
