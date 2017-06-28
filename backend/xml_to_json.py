import lxml.etree
import json
from collections import OrderedDict, Counter

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

def calculate_mean(numbers):
  """calculate the mean of a list of numbers"""
  return round(sum(numbers) / len(numbers), 3)

def calculate_median(numbers):
  """calculate the median of a list of numbers"""
  l = len(numbers)
  center_pos = (l - 1) // 2
  #if numbers has an odd length
  if l % 2 == 1: 
    #return center element
    return numbers[center_pos]
  #if numbers has an even length
  else:
    #return mean of two center elements
    return round((numbers[center_pos] + numbers[center_pos + 1]) / 2, 3)

def calculate_mode(numbers):
  """calculate the mode (the most common element) of numbers"""
  count = Counter(numbers)
  #return element of (element, count) that has the highest count
  return count.most_common(1)[0][0]

def get_width_height_statistics(width_list, height_list):
  """calculate some statistics such as max, min, average, median and mode
     of the widths and heights of all text objects on the page"""
  width_list, height_list = sorted(width_list), sorted(height_list)
  #width statistics
  max_width = max(width_list)
  min_width = min(width_list)
  average_width = calculate_mean(width_list)
  median_width = calculate_median(width_list)
  mode_width = calculate_mode(width_list)
  #height statistics
  max_height = max(height_list)
  min_height = min(height_list)
  average_height = calculate_mean(height_list)
  median_height = calculate_median(height_list)
  mode_height = calculate_mode(height_list)

  return {
      'max': [max_width, max_height],
      'min': [min_width, min_height],
      'average': [average_width, average_height],
      'median': [median_width, median_height],
      'mode': [mode_width, mode_height]
      }

def convert_from_string(xml_string):
  """convert an xml string into the desired JSON object representation"""
  xml_tree = lxml.etree.fromstring(xml_string.encode('utf-8'))
  coords_nodes = get_all_coordsnodes(xml_tree)
  page_width, page_height = get_page_size(xml_tree)

  #building the errors json object
  errors_json = ""
  if not coords_nodes:
    errors_json = "No text on page."

  width_list, height_list = [], []
  #building up the map json object one node at a time
  map_json = []
  for node in coords_nodes:
    #create a single json node as a dictionary
    coordinates = convert_to_int_list(node.attrib['coords'])
    left_x, top_y, width, height = convert_coordinates_to_dimensions(coordinates)
    width_list.append(width)
    height_list.append(height)
    json_node = {
      't': node.text,
      'c': [left_x, top_y, width, height],
      'e': coordsnode_abbrev_lookup[node.tag]
    }
    map_json.append(json_node)

  if width_list and height_list:
    wh_statistics = get_width_height_statistics(width_list, height_list)
  else:
    wh_statistics = {}

  json_object = OrderedDict([
      ('errors', errors_json),
      ('size', {'width': page_width, 'height': page_height}),
      ('statistics', wh_statistics),
      ('map', map_json)
  ])

  return json_object
