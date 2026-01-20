import unittest
from unittest.mock import patch, MagicMock
import requests
from immich_lib.client import ImmichClient


class TestMiscellaneousMixin(unittest.TestCase):
    def setUp(self):
        # Create a proper client instance that will be used for testing
        self.server_url = "http://localhost:2283"
        self.api_key = "test-api-key"
        self.client = ImmichClient(self.server_url, self.api_key)

    @patch("requests.Session.request")
    def test_get_timeline_success(self, mock_request):
        """Test successful timeline retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "bucket1", "assets": []},
            {"id": "bucket2", "assets": []},
        ]
        mock_request.return_value = mock_response

        result = self.client.get_timeline()
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_get_timeline_buckets_success(self, mock_request):
        """Test successful timeline buckets retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "bucket1", "name": "2023"},
            {"id": "bucket2", "name": "2024"},
        ]
        mock_request.return_value = mock_response

        result = self.client.get_timeline_buckets(year=2023)
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_list_api_keys_success(self, mock_request):
        """Test successful API keys listing"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "key1", "name": "Test Key 1"},
            {"id": "key2", "name": "Test Key 2"},
        ]
        mock_request.return_value = mock_response

        result = self.client.list_api_keys()
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_create_api_key_success(self, mock_request):
        """Test successful API key creation"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "newkey123",
            "name": "New API Key",
            "secretKey": "secret123",
        }
        mock_request.return_value = mock_response

        result = self.client.create_api_key("New API Key")
        self.assertEqual(result["id"], "newkey123")

    @patch("requests.Session.request")
    def test_delete_api_key_success(self, mock_request):
        """Test successful API key deletion"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.delete_api_key("key123")
        self.assertTrue(result)

    @patch("requests.Session.request")
    def test_get_library_info_success(self, mock_request):
        """Test successful library info retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"id": "lib123", "stats": {"assetCount": 100}}
        mock_request.return_value = mock_response

        result = self.client.get_library_info()
        self.assertEqual(result["id"], "lib123")

    @patch("requests.Session.request")
    def test_cleanup_library_success(self, mock_request):
        """Test successful library cleanup"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.cleanup_library()
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
