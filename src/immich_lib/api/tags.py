from ..base import ImmichBaseClient

class TagsMixin(ImmichBaseClient):
    """
    Mixin for Tags related endpoints.
    """
    def list_tags(self):
        """Get all tags"""
        return self.get("tags")

    def create_tag(self, name, type="TEXT"):
        """Create a new tag"""
        return self.post("tags", json={"name": name, "type": type})

    def get_tag(self, tag_id):
        """Get specific tag info"""
        return self.get(f"tags/{tag_id}")

    def update_tag(self, tag_id, name):
        """Update a tag"""
        return self.patch(f"tags/{tag_id}", json={"name": name})

    def delete_tag(self, tag_id):
        """Delete a tag"""
        return self.delete(f"tags/{tag_id}")

    def tag_assets(self, tag_id, asset_ids):
        """Add a tag to assets"""
        return self.put(f"tags/{tag_id}/assets", json={"ids": asset_ids})

    def untag_assets(self, tag_id, asset_ids):
        """Remove a tag from assets"""
        return self.delete(f"tags/{tag_id}/assets", json={"ids": asset_ids})
