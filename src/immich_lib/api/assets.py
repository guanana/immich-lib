from ..base import ImmichBaseClient
import os
try:
    from tqdm import tqdm
except ImportError:
    class tqdm:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def update(self, *args): pass

class AssetsMixin(ImmichBaseClient):
    """
    Mixin for Assets related endpoints.
    """
    def list_assets(self, **kwargs):
        """
        List all assets. 
        Note: The standard way for full library list is through search/metadata with empty query
        as it respects API key restrictions better in v2.x.
        """
        return self.post("search/metadata", json=kwargs).get('assets', {}).get('items', [])

    def get_asset_info(self, asset_id):
        """Get metadata for a specific asset"""
        return self.get(f"assets/{asset_id}")

    def update_asset(self, asset_id, **kwargs):
        """Update asset metadata (isFavorite, isArchived, description, etc.)"""
        return self.put(f"assets/{asset_id}", json=kwargs)

    def delete_assets(self, ids):
        """Delete multiple assets"""
        return self.delete("assets", json={"ids": ids})

    def download_asset(self, asset_id, output_path=None, stream=True):
        """Download high-quality/original asset"""
        response = self.get(f"assets/{asset_id}/original", stream=stream)
        if not output_path:
            return response
        
        # If output_path is provided, handle the streaming save
        try:
            total_size = int(response.headers.get('content-length', 0))
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

    def view_asset(self, asset_id, size="preview", edited=False):
        """Retrieve thumbnail/preview for an asset"""
        params = {"size": size, "edited": edited}
        return self.get(f"assets/{asset_id}/thumbnail", params=params, stream=True)

    def upload_asset(self, file_path, **kwargs):
        """
        Upload a new asset.
        file_path: local path to the file
        kwargs: deviceAssetId, deviceId, fileCreatedAt, fileModifiedAt, isFavorite, duration
        """
        # This usually requires multipart/form-data with 'assetData' key
        with open(file_path, 'rb') as f:
            files = {'assetData': f}
            data = kwargs
            return self.post("assets", files=files, data=data)
