#!/usr/bin/env python3

import unittest
from nose.tools import assert_equal
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
     """Tests the access_nested_map function."""
     @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
     ])
     def test_access_nested_map(self, map, key_path, expected_value):
          """Tests access_nested_map's output."""
          assert_equal(access_nested_map(map, key_path), expected_value)


if __name__ == "__main__":
     unittest.main()
