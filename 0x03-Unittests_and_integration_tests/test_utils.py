import unittest
from nose.tools import assert_equal
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
     @parameterized.expand([
        ("nested_map",{"a": 1}, "path",("a",)),
        ("nested_map",{"a": {"b": 2}}, "path",("a",)),
        ("nested_map", {"a": {"b": 2}}, "path",("a", "b")),
     ])
     def test_access_nested_map(self,input_name,input_value,path_name,expected_value):
          assert_equal(access_nested_map(input_value, path_name), expected_value)