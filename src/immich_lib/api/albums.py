from ..base import ImmichBaseClient

class AlbumsMixin(ImmichBaseClient):
    """
    Mixin for Albums related endpoints.
    """
    def list_albums(self, shared=None):
        """List all albums. If shared is None, merges owned and shared albums."""
        if shared is not None:
            params = {"shared": "true" if shared else "false"}
            return self.get("albums", params=params)
        
        # Merge owned and shared by default
        owned = self.get("albums", params={"shared": "false"})
        shared_list = self.get("albums", params={"shared": "true"})
        
        album_map = {a['id']: a for a in owned}
        for a in shared_list:
            if a['id'] not in album_map:
                album_map[a['id']] = a
        return list(album_map.values())

    def create_album(self, album_name, asset_ids=None, description=None):
        """Create a new album"""
        data = {"albumName": album_name}
        if asset_ids: data["assetIds"] = asset_ids
        if description: data["description"] = description
        return self.post("albums", json=data)

    def get_album(self, album_id):
        """Get details of a specific album"""
        return self.get(f"albums/{album_id}")

    def update_album(self, album_id, album_name=None, description=None, album_thumbnail_asset_id=None):
        """Update album details"""
        data = {}
        if album_name: data["albumName"] = album_name
        if description: data["description"] = description
        if album_thumbnail_asset_id: data["albumThumbnailAssetId"] = album_thumbnail_asset_id
        return self.patch(f"albums/{album_id}", json=data)

    def delete_album(self, album_id):
        """Delete an album"""
        return self.delete(f"albums/{album_id}")

    def add_assets_to_album(self, album_id, asset_ids):
        """Add assets to an album"""
        return self.put(f"albums/{album_id}/assets", json={"ids": asset_ids})

    def remove_assets_from_album(self, album_id, asset_ids):
        """Remove assets from an album"""
        return self.delete(f"albums/{album_id}/assets", json={"ids": asset_ids})

    def add_users_to_album(self, album_id, users):
        """
        Share album with users.
        users: list of dictionaries with 'userId' and 'role'
        """
        return self.put(f"albums/{album_id}/users", json={"users": users})

    def remove_user_from_album(self, album_id, user_id):
        """Remove a user from an album. Use 'me' to leave."""
        return self.delete(f"albums/{album_id}/user/{user_id}")

    # Helper methods from previous implementation
    def find_album(self, identifier):
        """Find an album by ID or name (case-insensitive)"""
        # Try both owned and shared
        albums = self.list_albums(shared=False)
        shared_albums = self.list_albums(shared=True)
        
        # Merge unique
        album_map = {a['id']: a for a in albums}
        for a in shared_albums:
            if a['id'] not in album_map:
                album_map[a['id']] = a
        
        for album in album_map.values():
            if album['id'] == identifier or album.get('albumName', '').lower() == identifier.lower():
                return album
        return None
