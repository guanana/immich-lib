import unittest
from unittest.mock import patch, MagicMock
import requests
from immich_lib.api.stacks import StacksMixin


class TestStacksMixin(unittest.TestCase):
    def setUp(self):
        # Create a mock client instance
        self.server_url = "http://localhost:2283"
        self.api_key = "test-api-key"
        # Create a minimal mock client that inherits from StacksMixin
        self.client = type("MockClient", (StacksMixin,), {})()
        self.client.server_url = self.server_url
        self.client.api_url = f"{self.server_url}/api"
        self.client.headers = {"x-api-key": self.api_key}
        self.client.session = MagicMock()

    @patch("requests.Session.request")
    def test_create_stack_success(self, mock_request):
        """Test successful stack creation"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "stack123",
            "primaryAssetId": "asset1",
            "assetIds": ["asset1", "asset2"],
        }
        mock_request.return_value = mock_response

        result = self.client.create_stack("asset1", ["asset2", "asset3"])
        self.assertEqual(result["id"], "stack123")

    @patch("requests.Session.request")
    def test_get_stack_success(self, mock_request):
        """Test successful stack retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "stack123",
            "primaryAssetId": "asset1",
            "assetIds": ["asset1", "asset2"],
        }
        mock_request.return_value = mock_response

        result = self.client.get_stack("stack123")
        self.assertEqual(result["id"], "stack123")

    @patch("requests.Session.request")
    def test_update_stack_success(self, mock_request):
        """Test successful stack update"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "stack123",
            "primaryAssetId": "asset2",
            "assetIds": ["asset1", "asset2"],
        }
        mock_request.return_value = mock_response

        result = self.client.update_stack("stack123", "asset2")
        self.assertEqual(result["primaryAssetId"], "asset2")

    @patch("requests.Session.request")
    def test_delete_stack_success(self, mock_request):
        """Test successful stack deletion"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.delete_stack("stack123")
        self.assertTrue(result)

    @patch("requests.Session.request")
    def test_remove_asset_from_stack_success(self, mock_request):
        """Test successful asset removal from stack"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.remove_asset_from_stack("stack123", "asset1")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
