#!/usr/bin/env python3
"""A module for testing the utils module.
"""
import unittest
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

class TestGetJson(unittest.TestCase):
    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("requests.get")
    def test_get_json(self, url, expected_payload, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = expected_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(url)

        # Assertions
        mock_get.assert_called_once_with(url)
        self.assertEqual(result, expected_payload)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()

            # Call a_property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Check result is correct both times
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method was only called once due to memoization
            mock_method.assert_called_once()
