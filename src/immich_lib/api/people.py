from ..base import ImmichBaseClient

class PeopleMixin(ImmichBaseClient):
    """
    Mixin for People related endpoints.
    """
    def get_all_people(self, with_hidden=False):
        """Get all people"""
        return self.get("people", params={"withHidden": with_hidden})

    def get_person(self, person_id):
        """Get information about a specific person"""
        return self.get(f"people/{person_id}")

    def update_person(self, person_id, **kwargs):
        """Update person information"""
        return self.put(f"people/{person_id}", json=kwargs)

    def get_person_assets(self, person_id):
        """Get all assets for a specific person"""
        return self.get(f"people/{person_id}/assets")

    def merge_people(self, primary_person_id, subordinate_person_ids):
        """Merge multiple people into one"""
        data = {"ids": subordinate_person_ids}
        return self.post(f"people/{primary_person_id}/merge", json=data)
