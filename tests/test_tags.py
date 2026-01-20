import unittest
from unittest.mock import patch, MagicMock
import requests
from immich_lib.api.tags import TagsMixin


class TestTagsMixin(unittest.TestCase):
    def setUp(self):
        # Create a mock client instance
        self.server_url = "http://localhost:2283"
        self.api_key = "test-api-key"
        # Create a minimal mock client that inherits from TagsMixin
        self.client = type("MockClient", (TagsMixin,), {})()
        self.client.server_url = self.server_url
        self.client.api_url = f"{self.server_url}/api"
        self.client.headers = {"x-api-key": self.api_key}
        self.client.session = MagicMock()

    @patch("requests.Session.request")
    def test_list_tags_success(self, mock_request):
        """Test successful tags listing"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "tag1", "name": "Vacation", "type": "TEXT"},
            {"id": "tag2", "name": "Family", "type": "TEXT"},
        ]
        mock_request.return_value = mock_response

        result = self.client.list_tags()
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_create_tag_success(self, mock_request):
        """Test successful tag creation"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "newtag123",
            "name": "New Tag",
            "type": "TEXT",
        }
        mock_request.return_value = mock_response

        result = self.client.create_tag("New Tag")
        self.assertEqual(result["id"], "newtag123")

    @patch("requests.Session.request")
    def test_get_tag_success(self, mock_request):
        """Test successful tag retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "tag123",
            "name": "Vacation",
            "type": "TEXT",
        }
        mock_request.return_value = mock_response

        result = self.client.get_tag("tag123")
        self.assertEqual(result["name"], "Vacation")

    @patch("requests.Session.request")
    def test_update_tag_success(self, mock_request):
        """Test successful tag update"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "tag123",
            "name": "Updated Vacation",
            "type": "TEXT",
        }
        mock_request.return_value = mock_response

        result = self.client.update_tag("tag123", "Updated Vacation")
        self.assertEqual(result["name"], "Updated Vacation")

    @patch("requests.Session.request")
    def test_delete_tag_success(self, mock_request):
        """Test successful tag deletion"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.delete_tag("tag123")
        self.assertTrue(result)

    @patch("requests.Session.request")
    def test_tag_assets_success(self, mock_request):
        """Test successful asset tagging"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"assetId": "asset1", "status": "success"},
            {"assetId": "asset2", "status": "success"},
        ]
        mock_request.return_value = mock_response

        result = self.client.tag_assets("tag123", ["asset1", "asset2"])
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_untag_assets_success(self, mock_request):
        """Test successful asset untagging"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.untag_assets("tag123", ["asset1", "asset2"])
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
