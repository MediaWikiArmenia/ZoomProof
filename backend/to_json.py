from collections import OrderedDict
import json
from statistics import calculate_mean, calculate_median, calculate_mode

class ToJSONConverter:
  def __init__(self):
    """initialize"""
    pass

  def _get_width_height_statistics(self, width_list, height_list):
    """calculate some statistics such as max, min, average, median and mode
       of the widths and heights of all text objects on the page"""
    width_list, height_list = sorted(width_list), sorted(height_list)
    #width, height statistics
    max_width, max_height = max(width_list), max(height_list)
    min_width, min_height = min(width_list), min(height_list)
    average_width, average_height = calculate_mean(width_list), calculate_mean(height_list)
    median_width, median_height = calculate_median(width_list), calculate_median(height_list)
    mode_width, mode_height = calculate_mode(width_list), calculate_mode(height_list)

    return {
        'max': [max_width, max_height],
        'min': [min_width, min_height],
        'average': [average_width, average_height],
        'median': [median_width, median_height],
        'mode': [mode_width, mode_height]
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

  def _build_map_object(self, width_list, height_list):
    """building up the map json object one node at a time"""
    map_json = []
    for node in self.textnodes:
      #create a single json map node as a dictionary
      coordinates = self._get_coordinates(node)
      left_x, top_y, width, height = self._convert_coordinates_to_dimensions(coordinates)
      width_list.append(width)
      height_list.append(height)
      json_node = {
        't': node.text,
        'c': [left_x, top_y, width, height],
        'e': self._text_category(node.tag)
      }
      map_json.append(json_node)
    return map_json

  def _build_statistics_object(self, width_list, height_list):
    """return the statistics json object"""
    if width_list and height_list:
      wh_statistics = self._get_width_height_statistics(width_list, height_list)
    else:
      wh_statistics = {}
    return wh_statistics

  def convert_from_string(self, document_string):
    """convert an xml string into the desired JSON object representation"""
    self._set_document_tree(document_string)
    self._set_textnodes()

    errors_json = self._build_errors_object()
    size_json = self._build_size_object()

    width_list, height_list = [], []
    map_json = self._build_map_object(width_list, height_list)
    statistics_json = self._build_statistics_object(width_list, height_list)

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
