import lxml.etree
from to_json import ToJSONConverter

coordsnode_abbrev_lookup = {
    'WORD': 'w',
    'CHARACTER': 'c',
    'LINE': 'l',
    'PARAGRAPH': 'ph',
    'REGION': 'r',
    'PAGECOLUMNS': 'pc'
}

class XMLToJSON(ToJSONConverter):
  def __init__(self):
    """initialize"""
    self.document_tree = None
    self.textnodes = None

  def _get_page_size(self):
    """return width, height from the document tree"""
    width_entry = (self.document_tree.xpath("//OBJECT/@width"))
    height_entry = (self.document_tree.xpath("//OBJECT/@height"))
    try:
      width, height = int(width_entry[0]), int(height_entry[0])
    except KeyError:
      width, height = -1, -1
    return width, height

  def _set_textnodes(self):
    """set text nodes from the document tree"""
    #xpath query for all nodes in the tree that are either ...
    #"WORD" or "LINE" or "PARAGRAPH" or "CHARACTER" or "REGION" or "PAGECOLUMNS" nodes ...
    #and have a "coords" attribute"""
    self.textnodes = self.document_tree.xpath("""//*[self::WORD or self::LINE or self::PARAGRAPH or 
                                                     self::CHARACTER or self::REGION or self::PAGECOLUMNS]
                                                     [@coords]""")

  def _set_document_tree(self, document_string):
    """set the document tree from the document string"""
    self.document_tree = lxml.etree.fromstring(document_string.encode('utf-8'))

  def _get_coordinates(self, node):
    """get coordinates from a text node"""
    return self._convert_to_int_list(node.attrib['coords'])

  def _convert_to_int_list(self, coords_string):
    """convert a comma separated coords string to a list of coord integers
       e.g. '1,2,3,4' -> [1, 2, 3, 4]"""
    return [int(coord) for coord in coords_string.split(',')]

  def _text_category(self, node_tag):
    """return the category of this particular text node, e.g. word or line"""
    return coordsnode_abbrev_lookup[node_tag]
