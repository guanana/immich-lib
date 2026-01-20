import unittest
from unittest.mock import patch, MagicMock
from immich_lib.client import ImmichClient


class TestSearchMixin(unittest.TestCase):
    def setUp(self):
        # Create a proper client instance that will be used for testing
        self.server_url = "http://localhost:2283"
        self.api_key = "test-api-key"
        self.client = ImmichClient(self.server_url, self.api_key)

    @patch("requests.Session.request")
    def test_search_metadata_success(self, mock_request):
        """Test successful metadata search"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "assets": {
                "items": [
                    {"id": "asset1", "originalFileName": "test.jpg"},
                    {"id": "asset2", "originalFileName": "photo.png"},
                ]
            }
        }
        mock_request.return_value = mock_response

        # Test search with query and filters
        result = self.client.search_metadata("sunset", isFavorite=True, type="IMAGE")
        self.assertEqual(len(result["assets"]["items"]), 2)

    @patch("requests.Session.request")
    def test_search_metadata_no_query(self, mock_request):
        """Test metadata search without query"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "assets": {"items": [{"id": "asset1", "originalFileName": "test.jpg"}]}
        }
        mock_request.return_value = mock_response

        result = self.client.search_metadata(isFavorite=True)
        self.assertEqual(len(result["assets"]["items"]), 1)

    @patch("requests.Session.request")
    def test_search_places_success(self, mock_request):
        """Test successful places search"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "place1", "name": "Paris"},
            {"id": "place2", "name": "London"},
        ]
        mock_request.return_value = mock_response

        result = self.client.search_places("Paris")
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_search_smart_success(self, mock_request):
        """Test successful smart search"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "asset1", "originalFileName": "smart1.jpg"},
            {"id": "asset2", "originalFileName": "smart2.png"},
        ]
        mock_request.return_value = mock_response

        result = self.client.search_smart("sunset at beach", limit=10)
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_get_explore_data_success(self, mock_request):
        """Test successful explore data retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "places": ["Paris", "London"],
            "people": ["John", "Jane"],
        }
        mock_request.return_value = mock_response

        result = self.client.get_explore_data()
        self.assertEqual(len(result["places"]), 2)


if __name__ == "__main__":
    unittest.main()
