import pdf_to_xhtml
from xhtml_to_json import XHTMLToJSON
import data_ops
import config
from process_request import RequestProcessor

class PDFRequestProcessor(RequestProcessor):
  def __init__(self):
    """initialize"""
    self.filetype = 'pdf'
    self.datadir = config.server['datadir_pdfjson']

  def process_single_page(self, fileinfo, file_sha1, page):
    """process a single page:
       - convert to xhtml from .pdf file
       - convert xhtml to JSON
       - save JSON as file in appropriate path"""
    xhtml_string = pdf_to_xhtml.convert_from_file(config.server['tmpdir'] + fileinfo['filename'], page)
    json_object = XHTMLToJSON().convert_from_string(xhtml_string)
    data_ops.save_json_page(json_object, file_sha1, page, self.datadir)
