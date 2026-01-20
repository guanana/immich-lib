import unittest
from unittest.mock import patch, MagicMock
import requests
from immich_lib.api.users import UsersMixin


class TestUsersMixin(unittest.TestCase):
    def setUp(self):
        # Create a mock client instance
        self.server_url = "http://localhost:2283"
        self.api_key = "test-api-key"
        # Create a minimal mock client that inherits from UsersMixin
        self.client = type("MockClient", (UsersMixin,), {})()
        self.client.server_url = self.server_url
        self.client.api_url = f"{self.server_url}/api"
        self.client.headers = {"x-api-key": self.api_key}
        self.client.session = MagicMock()

    @patch("requests.Session.request")
    def test_list_users_success(self, mock_request):
        """Test successful users listing"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = [
            {"id": "user1", "email": "user1@example.com", "name": "User One"},
            {"id": "user2", "email": "user2@example.com", "name": "User Two"},
        ]
        mock_request.return_value = mock_response

        result = self.client.list_users()
        self.assertEqual(len(result), 2)

    @patch("requests.Session.request")
    def test_create_user_success(self, mock_request):
        """Test successful user creation"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "newuser123",
            "email": "newuser@example.com",
            "name": "New User",
        }
        mock_request.return_value = mock_response

        result = self.client.create_user(
            "newuser@example.com", "password123", "New User", is_admin=True
        )
        self.assertEqual(result["id"], "newuser123")

    @patch("requests.Session.request")
    def test_get_me_success(self, mock_request):
        """Test successful current user retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "currentuser123",
            "email": "current@example.com",
            "name": "Current User",
        }
        mock_request.return_value = mock_response

        result = self.client.get_me()
        self.assertEqual(result["name"], "Current User")

    @patch("requests.Session.request")
    def test_get_user_success(self, mock_request):
        """Test successful specific user retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "user123",
            "email": "user@example.com",
            "name": "User",
        }
        mock_request.return_value = mock_response

        result = self.client.get_user("user123")
        self.assertEqual(result["name"], "User")

    @patch("requests.Session.request")
    def test_update_user_success(self, mock_request):
        """Test successful user update"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "id": "user123",
            "email": "updated@example.com",
            "name": "Updated User",
        }
        mock_request.return_value = mock_response

        result = self.client.update_user("user123", email="updated@example.com")
        self.assertEqual(result["email"], "updated@example.com")

    @patch("requests.Session.request")
    def test_delete_user_success(self, mock_request):
        """Test successful user deletion"""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        result = self.client.delete_user("user123")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
