from ..base import ImmichBaseClient

class PartnersMixin(ImmichBaseClient):
    """
    Mixin for Partner sharing related endpoints.
    """
    def list_partners(self, direction="shared-with-me"):
        """Get partners the user is sharing with or who are sharing with the user"""
        return self.get("partners", params={"direction": direction})

    def create_partner(self, partner_id):
        """Start sharing with a partner"""
        return self.post(f"partners/{partner_id}")

    def update_partner(self, partner_id, **kwargs):
        """Update partner sharing settings"""
        return self.put(f"partners/{partner_id}", json=kwargs)

    def delete_partner(self, partner_id):
        """Stop sharing with a partner"""
        return self.delete(f"partners/{partner_id}")
