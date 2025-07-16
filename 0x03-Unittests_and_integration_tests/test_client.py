#!/usr/bin/env python3
"""A module for testing functions in the client module."""

import unittest
from unittest import TestCase
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from utils import get_json
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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
            new_callable=PropertyMock,
            return_value="https://fake-url.com/org/repos"
        ) as mock_repos_url:
            client = GithubOrgClient("test-org")
            repos = client.public_repos()

            # Assert output is a list of repo names
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            # Ensure both mocks were called once
            url_example = "https://fake-url.com/org/repos"
            mock_get_json.assert_called_once_with(url_example)
            mock_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license correctly identifies matching license keys."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "apache2_repos": apache2_repos
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get with side_effect per URL."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Configure side_effect based on URL
        def side_effect(url):
            if url == "https://api.github.com/orgs/my-org":
                mock_response = Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            elif url == cls.org_payload["repos_url"]:
                mock_response = Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            return None

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns all repo names."""
        client = GithubOrgClient("my-org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters repos by license key."""
        client = GithubOrgClient("my-org")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
