import unittest
from unittest.mock import patch, MagicMock
import requests
from immich_lib.api.folders import FoldersMixin


class TestFoldersMixin(unittest.TestCase):
    def setUp(self):
        # Create a mock client instance
        self.server_url = "http://localhost:2283"
        self.api_key = "test-api-key"
        # Create a minimal mock client that inherits from FoldersMixin
        self.client = type("MockClient", (FoldersMixin,), {})()
        self.client.server_url = self.server_url
        self.client.api_url = f"{self.server_url}/api"
        self.client.headers = {"x-api-key": self.api_key}
        self.client.session = MagicMock()

    @patch("requests.Session.request")
    def test_list_folders_success(self, mock_request):
        """Test successful list folders"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "folder1", "importPath": "/path/to/folder1"},
            {"id": "folder2", "importPath": "/path/to/folder2"},
        ]
        mock_request.return_value = mock_response

        result = self.client.list_folders()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "folder1")

    @patch("requests.Session.request")
    def test_list_folders_empty_response(self, mock_request):
        """Test list folders with empty response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = []
        mock_request.return_value = mock_response

        result = self.client.list_folders()
        self.assertEqual(result, [])

    @patch("requests.Session.request")
    def test_create_folder_success(self, mock_request):
        """Test successful folder creation"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "newfolder123",
            "importPath": "/new/path",
        }
        mock_request.return_value = mock_response

        result = self.client.create_folder("/new/path")
        self.assertEqual(result["id"], "newfolder123")

    @patch("requests.Session.request")
    def test_create_folder_error(self, mock_request):
        """Test folder creation with error response"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"message": "Invalid path"}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Bad Request", response=mock_response
        )
        mock_request.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.create_folder("/invalid/path")

    @patch("requests.Session.request")
    def test_delete_folder_success(self, mock_request):
        """Test successful folder deletion"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.delete_folder("folder123")
        self.assertTrue(result)

    @patch("requests.Session.request")
    def test_delete_folder_error(self, mock_request):
        """Test folder deletion with error"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Internal Server Error", response=mock_response
        )
        mock_request.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.delete_folder("folder123")


if __name__ == "__main__":
    unittest.main()
