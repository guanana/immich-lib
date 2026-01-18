from ..base import ImmichBaseClient

class TrashMixin(ImmichBaseClient):
    """
    Mixin for Trash related endpoints.
    """
    def get_trash(self):
        """Get all items in the trash"""
        return self.get("trash")

    def empty_trash(self):
        """Empty the trash"""
        return self.delete("trash")

    def restore_trash(self):
        """Restore all items from the trash"""
        return self.post("trash/restore")

    def restore_assets(self, ids):
        """Restore specific assets from the trash"""
        return self.post("trash/restore/assets", json={"ids": ids})
