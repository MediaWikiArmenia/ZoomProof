import lxml.etree
import json
from collections import OrderedDict

coordsnode_abbrev_lookup = {
    'WORD': 'w',
    'CHARACTER': 'c',
    'LINE': 'l',
    'PARAGRAPH': 'ph',
    'REGION': 'r',
    'PAGECOLUMNS': 'pc'
}

def convert_to_int_list(coords_string):
  """convert a comma separated coords string to a list of coord integers
     e.g. '1,2,3,4' -> [1, 2, 3, 4]"""
  return [int(coord) for coord in coords_string.split(',')]

def get_page_size(xml_tree):
  """return width, height from the OBJECT node of the xml tree"""
  width_entry = (xml_tree.xpath("//OBJECT/@width"))
  height_entry = (xml_tree.xpath("//OBJECT/@height"))
  try:
    width, height = int(width_entry[0]), int(height_entry[0])
  except KeyError:
    width, height = -1, -1
  return width, height

def get_all_coordsnodes(xml_tree):
  """return all nodes from the xml_tree that have a 'coords' attribute"""
  #xpath query for all nodes in the tree that are either ...
  #"WORD" or "LINE" or "PARAGRAPH" or "CHARACTER" or "REGION" or "PAGECOLUMNS" nodes ...
  #and have a "coords" attribute"""
  return xml_tree.xpath("""//*[self::WORD or self::LINE or self::PARAGRAPH or 
                               self::CHARACTER or self::REGION or self::PAGECOLUMNS]
                               [@coords]""")

def convert_coordinates_to_dimensions(coordinates):
  """converting coordinates of the text bounding box from
     [left_x, bottom_y, right_x, top_y]
     to
     [left_x, top_y, width, height]"""
  left_x, bottom_y, right_x, top_y = coordinates
  width = right_x - left_x
  height = bottom_y - top_y
  return [left_x, top_y, width, height]

def convert_from_string(xml_string):
  """convert an xml string into the desired JSON object representation"""
  xml_tree = lxml.etree.fromstring(xml_string.encode('utf-8'))
  coords_nodes = get_all_coordsnodes(xml_tree)
  page_width, page_height = get_page_size(xml_tree)

  #building the errors json object
  errors_json = ""
  if not coords_nodes:
    errors_json = "No text on page."

  #building up the map json object one node at a time
  map_json = []
  for node in coords_nodes:
    #create a single json node as a dictionary
    coordinates = convert_to_int_list(node.attrib['coords'])
    json_node = {
      't': node.text,
      'c': convert_coordinates_to_dimensions(coordinates),
      'e': coordsnode_abbrev_lookup[node.tag]
    }
    map_json.append(json_node)

  json_object = OrderedDict([
      ('errors', errors_json),
      ('size', {'width': page_width, 'height': page_height}),
      ('map', map_json)
  ])

  return json_object
