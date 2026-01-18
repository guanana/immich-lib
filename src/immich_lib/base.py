import requests
import os

class ImmichBaseClient:
    """
    Base client for Immich API, handling authentication and low-level requests.
    """
    def __init__(self, server_url, api_key):
        self.server_url = server_url.rstrip("/")
        self.api_url = f"{self.server_url}/api"
        self.headers = {
            "x-api-key": api_key,
            "Accept": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _request(self, method, endpoint, **kwargs):
        """
        Internal helper to perform HTTP requests.
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        # Merge extra headers if provided
        headers = kwargs.pop('headers', {})
        
        response = self.session.request(method, url, headers=headers, **kwargs)
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Try to extract error message from JSON response
            try:
                error_data = response.json()
                error_msg = error_data.get('message', str(e))
                print(f"Immich API Error ({response.status_code}): {error_msg}")
            except Exception:
                print(f"Immich API Error ({response.status_code}): {e}")
            raise

        if response.status_code == 204:
            return True
        
        # For stream downloads or specific content types, return raw response if requested
        if kwargs.get('stream') or 'application/json' not in response.headers.get('Content-Type', ''):
            return response

        return response.json()

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self._request("PATCH", endpoint, **kwargs)
