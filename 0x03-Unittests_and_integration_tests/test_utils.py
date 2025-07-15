#!/usr/bin/env python3
"""A module for testing the utils module.
"""
import unittest
from typing import Dict, Tuple, Union
from unittest.mock import patch, Mock
from parameterized import parameterized
from nose.tools import assert_equal
from utils import (
    access_nested_map,
    get_json,
    memoize,
)



class TestAccessNestedMap(unittest.TestCase):
    """Tests the access_nested_map function."""
    @parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, key_path, expected_value):
        """Tests access_nested_map's output."""
        assert_equal(access_nested_map(nested_map, key_path), expected_value)


    @parameterized.expand([
    ({}, ("a",), KeyError),
    ({"a": 1}, ("a", "b"), TypeError),
    ])
    def test_access_nested_map_exception(self, nested_map, key_path, expected_exception):
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, key_path)
    

