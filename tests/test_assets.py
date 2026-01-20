import unittest
from unittest.mock import patch, MagicMock
import requests
import os
import tempfile
from immich_lib.api.assets import AssetsMixin


# Create a test class that inherits from AssetsMixin to create tests
class TestAssetsMixin(unittest.TestCase):
    def setUp(self):
        # Create a mock client instance
        self.server_url = "http://localhost:2283"
        self.api_key = "test-api-key"
        # Create a minimal mock client that inherits from AssetsMixin
        self.client = type("MockClient", (AssetsMixin,), {})()
        self.client.server_url = self.server_url
        self.client.api_url = f"{self.server_url}/api"
        self.client.headers = {"x-api-key": self.api_key}
        self.client.session = MagicMock()

    @patch("requests.Session.request")
    def test_list_assets_success(self, mock_request):
        """Test successful list assets with various filter parameters"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "assets": {
                "items": [
                    {"id": "asset1", "originalFileName": "test1.jpg"},
                    {"id": "asset2", "originalFileName": "test2.jpg"},
                ]
            }
        }
        mock_request.return_value = mock_response

        # Test with no filters
        result = self.client.list_assets()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "asset1")

        # Test with filter parameters
        result = self.client.list_assets(isFavorite=True, type="IMAGE")
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_list_assets_empty_response(self, mock_request):
        """Test list assets with empty response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"assets": {"items": []}}
        mock_request.return_value = mock_response

        result = self.client.list_assets()
        self.assertEqual(result, [])

    @patch("requests.Session.request")
    def test_list_assets_no_assets_key(self, mock_request):
        """Test list assets with missing assets key"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"other": "data"}
        mock_request.return_value = mock_response

        result = self.client.list_assets()
        self.assertEqual(result, [])

    @patch("requests.Session.request")
    def test_get_asset_info_success(self, mock_request):
        """Test successful get asset info"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "test123",
            "originalFileName": "test.jpg",
        }
        mock_request.return_value = mock_response

        result = self.client.get_asset_info("test123")
        self.assertEqual(result["id"], "test123")

    @patch("requests.Session.request")
    def test_get_asset_info_error(self, mock_request):
        """Test get asset info with error response"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"message": "Asset not found"}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Not Found", response=mock_response
        )
        mock_request.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.get_asset_info("nonexistent")

    @patch("requests.Session.request")
    def test_update_asset_success(self, mock_request):
        """Test successful asset update"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"id": "test123", "isFavorite": True}
        mock_request.return_value = mock_response

        result = self.client.update_asset("test123", isFavorite=True)
        self.assertEqual(result["isFavorite"], True)

    @patch("requests.Session.request")
    def test_delete_assets_success(self, mock_request):
        """Test successful asset deletion"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.delete_assets(["asset1", "asset2"])
        self.assertTrue(result)

    @patch("requests.Session.request")
    def test_delete_assets_error(self, mock_request):
        """Test asset deletion with error"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Internal Server Error", response=mock_response
        )
        mock_request.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.delete_assets(["asset1"])

    @patch("requests.Session.request")
    def test_download_asset_success_with_path(self, mock_request):
        """Test successful asset download with file path"""
        # Mock response for downloading the asset
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "image/jpeg", "content-length": "1024"}
        mock_response.iter_content.return_value = [b"test data"]

        # Mock file operations
        with patch("builtins.open", MagicMock()) as mock_open:
            with patch("tqdm") as mock_tqdm:
                mock_tqdm_instance = MagicMock()
                mock_tqdm.return_value.__enter__.return_value = mock_tqdm_instance

                mock_request.return_value = mock_response

                # Create temporary directory and file
                with tempfile.TemporaryDirectory() as tmpdir:
                    test_file = os.path.join(tmpdir, "test.jpg")
                    result = self.client.download_asset("asset123", test_file)

                    # Should return True to indicate success
                    self.assertTrue(result)

    @patch("requests.Session.request")
    def test_download_asset_success_no_path(self, mock_request):
        """Test asset download without file path (returns response)"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "image/jpeg"}
        mock_request.return_value = mock_response

        result = self.client.download_asset("asset123")
        self.assertEqual(result, mock_response)

    @patch("requests.Session.request")
    def test_view_asset_success(self, mock_request):
        """Test successful asset thumbnail view"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "image/jpeg"}
        mock_request.return_value = mock_response

        result = self.client.view_asset("asset123")
        self.assertEqual(result, mock_response)

    @patch("requests.Session.request")
    def test_upload_asset_success(self, mock_request):
        """Test successful asset upload"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "uploaded123",
            "originalFileName": "new.jpg",
        }
        mock_request.return_value = mock_response

        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
            tmp_file.write("test content")
            tmp_file_path = tmp_file.name

        try:
            # Mock file open operation
            with patch("builtins.open", MagicMock()):
                mock_request.return_value = mock_response

                result = self.client.upload_asset(tmp_file_path, isFavorite=True)
                self.assertEqual(result["id"], "uploaded123")
        finally:
            # Clean up temp file
            os.unlink(tmp_file_path)


if __name__ == "__main__":
    unittest.main()
