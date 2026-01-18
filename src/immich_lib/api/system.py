from ..base import ImmichBaseClient

class SystemMixin(ImmichBaseClient):
    """
    Mixin for System and Server related endpoints.
    """
    def get_server_version(self):
        """Get the current server version"""
        return self.get("server/version")

    def get_server_info(self):
        """Get general server information"""
        return self.get("server/info")

    def get_server_statistics(self):
        """Get server statistics"""
        return self.get("server/statistics")

    def get_server_config(self):
        """Get server configuration"""
        return self.get("server/config")

    def get_storage_info(self):
        """Get storage usage information"""
        return self.get("system-metadata/storage-info")

    def check_auth(self):
        """
        Verify the connection and authentication with the Immich server.
        """
        try:
            version_info = self.get_server_version()
            # Verify API key by calling a simple protected endpoint
            self.get("albums")
            return version_info
        except Exception:
            return None
