from collections import OrderedDict
import json
from statistics import calculate_mean, calculate_median, calculate_mode

textnode_name_lookup = {
    'w': 'word',
    'c': 'char',
    'l': 'line',
    'ph': 'paragraph',
    'r': 'region',
    'pc': 'pagecolumns'
}

class ToJSONConverter:
  def __init__(self):
    """initialize"""
    pass

  def _get_statistics_single_category(self, width_list, height_list):
    """calculate some statistics such as max, min, average, median and mode
       of the widths and heights of all text objects in one category"""
    if not width_list or not height_list:
      return {}

    width_list, height_list = sorted(width_list), sorted(height_list)
    #width, height statistics
    max_width, max_height = max(width_list), max(height_list)
    min_width, min_height = min(width_list), min(height_list)
    average_width, average_height = calculate_mean(width_list), calculate_mean(height_list)
    median_width, median_height = calculate_median(width_list), calculate_median(height_list)
    mode_width, mode_height = calculate_mode(width_list), calculate_mode(height_list)

    return {
        'number': len(width_list),
        'dimensions': {
          'max': [max_width, max_height],
          'min': [min_width, min_height],
          'average': [average_width, average_height],
          'median': [median_width, median_height],
          'mode': [mode_width, mode_height]
          }
        }

  def _convert_coordinates_to_dimensions(self, coordinates):
    """converting coordinates of the text bounding box from
       [left_x, bottom_y, right_x, top_y]
       to
       [left_x, top_y, width, height]"""
    left_x, bottom_y, right_x, top_y = coordinates
    width = round(right_x - left_x, 3)
    height = round(bottom_y - top_y, 3)
    return [left_x, top_y, width, height]

  def _build_errors_object(self):
    """return the errors json object"""
    errors_json = ""
    if not self.textnodes:
      errors_json = "No text on page."
    return errors_json

  def _build_size_object(self):
    """return the size json object"""
    page_width, page_height = self._get_page_size()
    return {'width': page_width, 'height': page_height}

  def _build_map_object(self, cat_width_lists, cat_height_lists, all_x, all_y):
    """building up the map json object one node at a time"""
    map_json = []
    for node in self.textnodes:
      #create a single json map node as a dictionary
      coordinates = self._get_coordinates(node)
      all_x.append(coordinates[0])
      all_x.append(coordinates[2])
      all_y.append(coordinates[1])
      all_y.append(coordinates[3])
      left_x, top_y, width, height = self._convert_coordinates_to_dimensions(coordinates)
      text_category = self._text_category(node.tag)
      json_node = {
        't': node.text,
        'c': [left_x, top_y, width, height],
        'e': text_category
      }
      cat_width_lists[text_category].append(width)
      cat_height_lists[text_category].append(height)
      map_json.append(json_node)
    return map_json

  def _build_statistics_object(self, cat_width_lists, cat_height_lists, all_x, all_y):
    """calculate some statistics such as max, min, average, median and mode
       of the widths and heights of all text objects in each category on the page"""
    statistics = {}
    #statistics for each category
    for cat in textnode_name_lookup.keys():
      cat_stats = self._get_statistics_single_category(cat_width_lists[cat], cat_height_lists[cat])
      if cat_stats:
        statistics[textnode_name_lookup[cat]] = cat_stats
    #overall statistics
    total_stats = self._get_statistics_single_category([width for width_list in cat_width_lists.values() for width in width_list],
                                                       [height for height_list in cat_height_lists.values() for height in height_list])
    if total_stats:
      statistics['total'] = total_stats
      statistics['total']['area'] = [min(all_x), min(all_y), max(all_x), max(all_y)]

    return statistics


  def convert_from_string(self, document_string):
    """convert an xml string into the desired JSON object representation"""
    self._set_document_tree(document_string)
    self._set_textnodes()

    errors_json = self._build_errors_object()
    size_json = self._build_size_object()

    cat_width_lists = {'w': [], 'c': [], 'l': [], 'ph': [], 'r': [], 'pc': []}
    cat_height_lists = {'w': [], 'c': [], 'l': [], 'ph': [], 'r': [], 'pc': []}
    all_x, all_y = [], []
    map_json = self._build_map_object(cat_width_lists, cat_height_lists, all_x, all_y)
    statistics_json = self._build_statistics_object(cat_width_lists, cat_height_lists, all_x, all_y)

    json_object = OrderedDict([
        ('errors', errors_json),
        ('size', size_json),
        ('statistics', statistics_json),
        ('map', map_json)
    ])

    return json_object

  def _set_document_tree(self, document_string):
    """set the document tree from the document string"""
    raise NotImplementedError

  def _set_textnodes(self):
    """set textnodes from the document tree"""
    raise NotImplementedError

  def _get_coordinates(self):
    """get list of coordinates from the text nodes"""
    raise NotImplementedError

  def _get_page_size(self):
    """get the page size from the document tree"""
    raise NotImplementedError

  def _text_category(self, node_tag):
    """return the category of this particular text node, e.g. word or line"""
    raise NotImplementedError
