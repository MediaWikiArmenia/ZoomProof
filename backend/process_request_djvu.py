import djvu_to_xml
from xml_to_json import XMLToJSON
import data_ops
import config
from process_request import RequestProcessor

class DJVURequestProcessor(RequestProcessor):
  def __init__(self):
    """initialize"""
    self.filetype = 'djvu'
    self.datadir = config.server['datadir_djvujson']

  def process_single_page(self, fileinfo, file_sha1, page):
    """process a single page:
       - convert to xml from .djvu file
       - convert xml to JSON
       - save JSON as file in appropriate path"""
    xml_string = djvu_to_xml.convert_from_file(config.server['tmpdir'] + fileinfo['filename'], page)
    json_object = XMLToJSON().convert_from_string(xml_string)
    data_ops.save_json_page(json_object, file_sha1, page, self.datadir)
