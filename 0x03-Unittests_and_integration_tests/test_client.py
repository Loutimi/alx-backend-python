#!/usr/bin/env python3
"""A module for testing functions in the client module."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"name": "Google"}),
        ("abc", {"name": "Abc"}),
    ])
    @patch("client.get_json")
    def test_org(
        self,
        org_name: str,
        expected_response: dict,
        mock_get_json
    ) -> None:
        """Test that .org returns the expected payload from get_json."""
        mock_get_json.return_value = expected_response

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_response)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self) -> None:
        """Test that _public_repos_url returns the repos_url from org data."""
        payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}

        with patch.object(
            GithubOrgClient, "org", new_callable=property
        ) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("test-org")
            result = client._public_repos_url

            self.assertEqual(result, payload["repos_url"])
