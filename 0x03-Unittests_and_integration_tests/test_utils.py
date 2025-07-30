#!/usr/bin/env python3
"""A module for testing functions in the utils module."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Dict, Tuple


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: dict, key_path: tuple, expected_value: object
    ) -> None:
        """Test that access_nested_map returns the correct value."""
        result = access_nested_map(nested_map, key_path)
        self.assertEqual(result, expected_value)

    @parameterized.expand(
        [
            ({}, ("a",), KeyError),
            ({"a": 1}, ("a", "b"), KeyError),
        ]
    )
    def test_access_nested_map_exception(
        self,
        nested_map: Dict,
        path: Tuple[str],
        exception: Exception,
    ) -> None:
        """Tests `access_nested_map`'s exception raising."""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function."""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, url: str, expected_payload: dict, mock_get: Mock) -> None:
        """Test that get_json returns the correct parsed JSON data."""
        mock_response = Mock()
        mock_response.json.return_value = expected_payload
        mock_get.return_value = mock_response

        result = get_json(url)
        mock_get.assert_called_once_with(url)
        self.assertEqual(result, expected_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for the memoize decorator."""

    def test_memoize(self) -> None:
        """Test that memoize caches method results after the first call."""

        class TestClass:
            """Dummy class to test memoization."""

            def a_method(self) -> int:
                """Return a fixed integer value."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Return the result of a_method using memoization."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock:
            obj = TestClass()

            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock.assert_called_once()
