import unittest
from unittest.mock import patch, MagicMock
import requests
from immich_lib.api.trash import TrashMixin


class TestTrashMixin(unittest.TestCase):
    def setUp(self):
        # Create a mock client instance
        self.server_url = "http://localhost:2283"
        self.api_key = "test-api-key"
        # Create a minimal mock client that inherits from TrashMixin
        self.client = type("MockClient", (TrashMixin,), {})()
        self.client.server_url = self.server_url
        self.client.api_url = f"{self.server_url}/api"
        self.client.headers = {"x-api-key": self.api_key}
        self.client.session = MagicMock()

    @patch("requests.Session.request")
    def test_get_trash_success(self, mock_request):
        """Test successful trash retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "asset1", "originalFileName": "deleted1.jpg"},
            {"id": "asset2", "originalFileName": "deleted2.png"},
        ]
        mock_request.return_value = mock_response

        result = self.client.get_trash()
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_empty_trash_success(self, mock_request):
        """Test successful trash emptying"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.empty_trash()
        self.assertTrue(result)

    @patch("requests.Session.request")
    def test_restore_trash_success(self, mock_request):
        """Test successful trash restore"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.restore_trash()
        self.assertTrue(result)

    @patch("requests.Session.request")
    def test_restore_assets_success(self, mock_request):
        """Test successful individual asset restore"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"status": "success"}
        mock_request.return_value = mock_response

        result = self.client.restore_assets(["asset1", "asset2"])
        self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    unittest.main()
