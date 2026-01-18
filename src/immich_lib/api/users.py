from ..base import ImmichBaseClient

class UsersMixin(ImmichBaseClient):
    """
    Mixin for Users related endpoints.
    """
    def list_users(self):
        """Get all users"""
        return self.get("users")

    def create_user(self, email, password, name, is_admin=False):
        """Create a new user"""
        data = {
            "email": email,
            "password": password,
            "name": name,
            "isAdmin": is_admin
        }
        return self.post("users", json=data)

    def get_me(self):
        """Get information about the current user"""
        return self.get("users/me")

    def get_user(self, user_id):
        """Get information about a specific user"""
        return self.get(f"users/{user_id}")

    def update_user(self, user_id, **kwargs):
        """Update user information"""
        return self.put(f"users/{user_id}", json=kwargs)

    def delete_user(self, user_id):
        """Delete a user"""
        return self.delete(f"users/{user_id}")
