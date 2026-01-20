import unittest
from unittest.mock import patch, MagicMock
import requests
from immich_lib.client import ImmichClient


class TestPartnersMixin(unittest.TestCase):
    def setUp(self):
        # Create a proper client instance that will be used for testing
        self.server_url = "http://localhost:2283"
        self.api_key = "test-api-key"
        self.client = ImmichClient(self.server_url, self.api_key)

    @patch("requests.Session.request")
    def test_list_partners_success(self, mock_request):
        """Test successful partners listing"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "partner1", "userId": "user123", "name": "Partner 1"},
            {"id": "partner2", "userId": "user456", "name": "Partner 2"},
        ]
        mock_request.return_value = mock_response

        result = self.client.list_partners("shared-with-me")
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_list_partners_with_direction(self, mock_request):
        """Test partners listing with different direction"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "partner1", "userId": "user123", "name": "Partner 1"}
        ]
        mock_request.return_value = mock_response

        result = self.client.list_partners("shared-by-me")
        self.assertEqual(len(result), 1)

    @patch("requests.Session.request")
    def test_create_partner_success(self, mock_request):
        """Test successful partner creation"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "newpartner123",
            "userId": "user456",
            "name": "New Partner",
        }
        mock_request.return_value = mock_response

        result = self.client.create_partner("user456")
        self.assertEqual(result["id"], "newpartner123")

    @patch("requests.Session.request")
    def test_update_partner_success(self, mock_request):
        """Test successful partner update"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "partner123",
            "userId": "user456",
            "isArchived": True,
        }
        mock_request.return_value = mock_response

        result = self.client.update_partner("partner123", isArchived=True)
        self.assertEqual(result["isArchived"], True)

    @patch("requests.Session.request")
    def test_delete_partner_success(self, mock_request):
        """Test successful partner deletion"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.delete_partner("partner123")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
