from ..base import ImmichBaseClient

class SearchMixin(ImmichBaseClient):
    """
    Mixin for Search related endpoints.
    """
    def search_metadata(self, query=None, **kwargs):
        """Search assets by metadata"""
        data = kwargs
        if query: data["query"] = query
        return self.post("search/metadata", json=data)

    def search_places(self, query):
        """Search places"""
        return self.get("search/places", params={"query": query})

    def search_smart(self, query, **kwargs):
        """Smart search (using CLIP)"""
        params = {"query": query}
        params.update(kwargs)
        return self.get("search/smart", params=params)

    def get_explore_data(self):
        """Get explore data (places, objects, etc.)"""
        return self.get("search/explore")
