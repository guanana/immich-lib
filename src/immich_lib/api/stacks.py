from ..base import ImmichBaseClient

class StacksMixin(ImmichBaseClient):
    """
    Mixin for Asset Stacks related endpoints.
    """
    def create_stack(self, primary_asset_id, asset_ids):
        """Create a new stack"""
        return self.post("stacks", json={"primaryAssetId": primary_asset_id, "assetIds": asset_ids})

    def get_stack(self, stack_id):
        """Get stack details"""
        return self.get(f"stacks/{stack_id}")

    def update_stack(self, stack_id, primary_asset_id):
        """Update stack primary asset"""
        return self.put(f"stacks/{stack_id}", json={"primaryAssetId": primary_asset_id})

    def delete_stack(self, stack_id):
        """Delete a stack (unstack assets)"""
        return self.delete(f"stacks/{stack_id}")

    def remove_asset_from_stack(self, stack_id, asset_id):
        """Remove a specific asset from a stack"""
        return self.delete(f"stacks/{stack_id}/assets/{asset_id}")
