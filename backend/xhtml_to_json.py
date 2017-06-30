import lxml.html
from to_json import ToJSONConverter

class XHTMLToJSON(ToJSONConverter):
  def __init__(self):
    """initialize"""
    self.document_tree = None
    self.textnodes = None

  def _get_page_size(self):
    """return width, height from the document tree"""
    width_entry = (self.document_tree.xpath("//body/doc/page/@width"))
    height_entry = (self.document_tree.xpath("//body/doc/page/@height"))
    try:
      width, height = float(width_entry[0]), float(height_entry[0])
    except KeyError:
      width, height = -1, -1
    return width, height

  def _set_textnodes(self):
    """set 'word' nodes from the document tree"""
    #xpath query for all nodes in the tree that are either 'word' nodes
    self.textnodes = self.document_tree.xpath("""//*[self::word]""")

  def _set_document_tree(self, document_string):
    """set the document tree from the document string"""
    self.document_tree = lxml.html.fromstring(document_string.encode('utf-8'))

  def _get_coordinates(self, node):
    """get coordinates from a text node"""
    return [
        round(float(node.attrib['xmin']), 3),
        round(float(node.attrib['ymax']), 3),
        round(float(node.attrib['xmax']), 3),
        round(float(node.attrib['ymin']), 3)
        ]

  def _text_category(self, node_tag):
    """return the category of this particular text node, e.g. word or line"""
    #the pdf xhtml nodes are always "words"
    return 'w'
