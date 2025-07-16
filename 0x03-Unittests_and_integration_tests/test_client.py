#!/usr/bin/env python3
"""A module for testing functions in the client module."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from utils import get_json
from typing import List


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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json) -> None:
        """Test that public_repos returns the correct list of repo names."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            return_value="https://fake-url.com/org/repos"
        ) as mock_repos_url:
            client = GithubOrgClient("test-org")
            repos = client.public_repos()

            # Assert output is a list of repo names
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            # Ensure both mocks were called once
            url = "https://fake-url.com/org/repos"
            mock_get_json.assert_called_once_with(url)
            mock_repos_url.assert_called_once()
