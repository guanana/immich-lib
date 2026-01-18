from ..base import ImmichBaseClient

class MiscellaneousMixin(ImmichBaseClient):
    """
    Mixin for various smaller API categories (Timeline, API Keys, Library settings).
    """
    # Timeline
    def get_timeline(self, **kwargs):
        """Get the asset timeline"""
        return self.get("timeline", params=kwargs)

    def get_timeline_buckets(self, **kwargs):
        """Get timeline buckets"""
        return self.get("timeline/buckets", params=kwargs)

    # API Keys
    def list_api_keys(self):
        """List all API keys for the user"""
        return self.get("api-keys")

    def create_api_key(self, name):
        """Create a new API key"""
        return self.post("api-keys", json={"name": name})

    def delete_api_key(self, key_id):
        """Delete an API key"""
        return self.delete(f"api-keys/{key_id}")

    # Library
    def get_library_info(self):
        """Get library statistics and info"""
        return self.get("library")

    def cleanup_library(self):
        """Trigger library cleanup"""
        return self.post("library/cleanup")
