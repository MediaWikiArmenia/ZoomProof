import unittest
import xml_to_json
import json

class TestXMLToJSON(unittest.TestCase):
  def test_convert_to_json_object(self):
    """test xml to json conversion on the specification files"""
    test_cases = (
        ('lines.json', 'lines.xml'), 
        ('words.json', 'words.xml')
    )

    for test_case in test_cases:

      with open('./tests/'+test_case[1]) as xml_file: 
        xml_string = xml_file.read()
      with open('./tests/'+test_case[0]) as json_file: 
        json_object = json.load(json_file)

      self.assertEqual(xml_to_json.convert_to_json_object(xml_string), json_object)

  def test_convert_to_int_list(self):
    """test the conversion of a coords string to an int list"""
    #TODO assert for non-positive integers?
    #TODO assert for coords list with len() != 4?
    test_case = ([13, 277, 313, 19], '13,277,313,19')
    self.assertEqual(xml_to_json.convert_to_int_list(test_case[1]), test_case[0])
