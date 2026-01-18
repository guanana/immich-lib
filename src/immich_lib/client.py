import os
import requests

try:
    from tqdm import tqdm
except ImportError:
    # Fallback to no progress bar if tqdm is missing to ensure script remains functional
    class tqdm:
        """A simple fallback for tqdm when it is not installed."""
        def __init__(self, total=None, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def update(self, n=1): pass

class ImmichClient:
    """
    A client for interacting with the Immich API (v2.x compatible).

    Attributes:
        server_url (str): The base URL of the Immich server (e.g., http://immich.local:2283).
        api_url (str): The full URL for the API endpoints (server_url + /api).
        headers (dict): headers sent with every request, containing the API key.
    """

    def __init__(self, server_url, api_key):
        """
        Initialize the ImmichClient.

        Args:
            server_url (str): The base URL of the Immich server.
            api_key (str): The API key for authentication.
        """
        self.server_url = server_url.rstrip("/")
        self.api_url = f"{self.server_url}/api"
        # x-api-key is the standard header for Immich API key authentication
        self.headers = {
            "x-api-key": api_key,
            "Accept": "application/json"
        }

    def check_auth(self):
        """
        Verify the connection and authentication with the Immich server.

        This method performs a two-step verification:
        1. Checks the public '/server/version' endpoint to confirm server reachability.
        2. Checks the protected '/albums' endpoint to verify the API key validity.

        Returns:
            dict: The server version information if successful, None otherwise.
        """
        try:
            # First, check the version (public)
            version_response = requests.get(f"{self.api_url}/server/version", headers=self.headers, timeout=10)
            version_response.raise_for_status()
            version_info = version_response.json()

            # Then, check a protected endpoint to verify the API key
            # /api/albums returns 401 if unauthorized and 200 if key is valid (even if empty)
            auth_response = requests.get(f"{self.api_url}/albums", headers=self.headers, timeout=10)
            auth_response.raise_for_status()
            
            return version_info
        except Exception as e:
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 401:
                print("Error: Authentication failed. Please check your IMMICH_API_KEY.")
            else:
                print(f"Error connecting to Immich: {e}")
            return None

    def list_albums(self):
        """
        List all albums available on the server, including shared ones.

        This method merges results from the base '/albums' endpoint and the 
        '/albums?shared=true' endpoint to ensure all accessible albums are visible.

        Returns:
            list: A list of unique album dictionaries if successful, empty list otherwise.
        """
        try:
            # Fetch owned albums
            response = requests.get(f"{self.api_url}/albums", headers=self.headers, timeout=10)
            response.raise_for_status()
            albums = response.json()

            # Fetch shared albums
            shared_response = requests.get(f"{self.api_url}/albums", headers=self.headers, params={"shared": "true"}, timeout=10)
            if shared_response.status_code == 200:
                shared_albums = shared_response.json()
                # Merge lists using ID as the key to avoid duplicates if an album is both owned and shared
                album_map = {a['id']: a for a in albums}
                for a in shared_albums:
                    if a['id'] not in album_map:
                        album_map[a['id']] = a
                albums = list(album_map.values())
            
            return albums
        except Exception as e:
            print(f"Error fetching albums: {e}")
            return []

    def get_album(self, album_id):
        """
        Get details and assets of a specific album.

        Args:
            album_id (str): The UUID of the album.

        Returns:
            dict: The album details including an 'assets' list if successful, None otherwise.
        """
        try:
            # Modern endpoint for specific album details and its assets
            response = requests.get(f"{self.api_url}/albums/{album_id}", headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching album {album_id}: {e}")
            return None

    def list_assets(self):
        """
        List all assets across the entire library.

        Uses the '/search/metadata' endpoint with an empty query as a fallback method 
        that works reliably for restricted API keys in Immich v2.x.

        Returns:
            list: A list of asset dictionaries if successful, empty list otherwise.
        """
        try:
            # Search metadata with empty query returns all accessible assets for the current user
            response = requests.post(
                f"{self.api_url}/search/metadata", 
                headers=self.headers, 
                json={}, 
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            # The search API returns assets in the 'assets' -> 'items' subpath
            return data.get('assets', {}).get('items', [])
        except Exception as e:
            print(f"Error fetching assets: {e}")
            return []

    def find_album(self, identifier):
        """
        Find an album by its UUID or Name (case-insensitive).

        Args:
            identifier (str): The UUID string or the descriptive name of the album.

        Returns:
            dict: The album dictionary if found, None otherwise.
        """
        albums = self.list_albums()
        for album in albums:
            # Check for direct UUID match or case-insensitive name match
            if album['id'] == identifier or album.get('albumName', '').lower() == identifier.lower():
                return album
        return None

    def get_asset_info(self, asset_id):
        """
        Get metadata information for a specific asset.

        Args:
            asset_id (str): The UUID of the asset.

        Returns:
            dict: The asset metadata dictionary if successful, None otherwise.
        """
        try:
            # Modern endpoint for detailed asset metadata
            response = requests.get(f"{self.api_url}/assets/{asset_id}", headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching asset info for {asset_id}: {e}")
            return None

    def download_asset(self, asset_id, output_path):
        """
        Download the original file of a specific asset.

        Args:
            asset_id (str): The UUID of the asset to download.
            output_path (str): The local filesystem path where the file will be saved.

        Returns:
            bool: True if the download completed successfully, False otherwise.
        """
        try:
            # Modern endpoint for original asset download with stream support
            response = requests.get(f"{self.api_url}/assets/{asset_id}/original", headers=self.headers, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            # Save the stream to a file with a progress bar (if tqdm is available)
            with open(output_path, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(output_path)) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            return True
        except Exception as e:
            print(f"Error downloading asset {asset_id}: {e}")
            return False
