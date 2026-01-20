import unittest
from unittest.mock import patch, MagicMock
import requests
from immich_lib.api.people import PeopleMixin


class TestPeopleMixin(unittest.TestCase):
    def setUp(self):
        # Create a mock client instance
        self.server_url = "http://localhost:2283"
        self.api_key = "test-api-key"
        # Create a minimal mock client that inherits from PeopleMixin
        self.client = type("MockClient", (PeopleMixin,), {})()
        self.client.server_url = self.server_url
        self.client.api_url = f"{self.server_url}/api"
        self.client.headers = {"x-api-key": self.api_key}
        self.client.session = MagicMock()

    @patch("requests.Session.request")
    def test_get_all_people_success(self, mock_request):
        """Test successful people listing"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "person1", "name": "John Doe", "thumbnail": "/thumb1.jpg"},
            {"id": "person2", "name": "Jane Smith", "thumbnail": "/thumb2.jpg"},
        ]
        mock_request.return_value = mock_response

        result = self.client.get_all_people()
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_get_all_people_with_hidden(self, mock_request):
        """Test people listing with hidden parameter"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "person1", "name": "John Doe", "thumbnail": "/thumb1.jpg"}
        ]
        mock_request.return_value = mock_response

        result = self.client.get_all_people(with_hidden=True)
        self.assertEqual(len(result), 1)

    @patch("requests.Session.request")
    def test_get_person_success(self, mock_request):
        """Test successful person retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "person123",
            "name": "John Doe",
            "birthDate": "1980-01-01",
            "thumbnail": "/thumb.jpg",
        }
        mock_request.return_value = mock_response

        result = self.client.get_person("person123")
        self.assertEqual(result["name"], "John Doe")

    @patch("requests.Session.request")
    def test_update_person_success(self, mock_request):
        """Test successful person update"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "person123",
            "name": "Updated Name",
            "birthDate": "1980-01-01",
        }
        mock_request.return_value = mock_response

        result = self.client.update_person("person123", name="Updated Name")
        self.assertEqual(result["name"], "Updated Name")

    @patch("requests.Session.request")
    def test_get_person_assets_success(self, mock_request):
        """Test successful person assets retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "asset1", "originalFileName": "photo1.jpg"},
            {"id": "asset2", "originalFileName": "photo2.jpg"},
        ]
        mock_request.return_value = mock_response

        result = self.client.get_person_assets("person123")
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_merge_people_success(self, mock_request):
        """Test successful people merge"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = ["person456", "person789"]
        mock_request.return_value = mock_response

        result = self.client.merge_people("person123", ["person456", "person789"])
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
