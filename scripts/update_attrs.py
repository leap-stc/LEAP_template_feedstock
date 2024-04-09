# This script updates the attributes of all the zarr stores that are created by the recipe, based on the current version of meta.yaml

import zarr
import os
import pathlib
from ruamel.yaml import YAML
yaml = YAML(typ='safe')
import gcsfs
from datetime import datetime, timezone
from .feedstock.recipe import latest_store_prefix
print(f"Using {latest_store_prefix=}")

fs = gcsfs.GCSFileSystem()

# # For later, get the current git hash and add to the updated attribute
timestamp = datetime.now(timezone.utc).isoformat()

# read info from meta.yaml
meta_path = './feedstock/meta.yaml'
meta = yaml.load(pathlib.Path(meta_path))

def update_zarr_attrs(store_path:str, additonal_attrs:dict):
    """
    Update the attributes of a zarr store with the given dictionary
    """
        # Check if store exists and otherwise give a useful warning
    if not fs.exists(store_path):
        print(f"Warning: Store {store_path} does not exist. Skipping.")
    else:
        print(f"Updating {store_path} with {additonal_attrs=}")
        store = zarr.open(zarr.storage.FSStore(store_path), mode='a')
        store.attrs.update(additonal_attrs)
        zarr.convenience.consolidate_metadata(store_path) #Important: do not pass the store object here!
    return store_path

# Loop over each recipe 
for recipe in meta['recipes']:
    id = recipe['id']
    assert 'object' in recipe.keys() #(FIXME: this does not support dict objects yet...)

    # Some how get the store path from the recipe
    store_path = f'{latest_store_prefix}/{id}.zarr'
    # This only works if the store name in the recipe is the same as the id...which is easy to get wrong!!! 

    # add the infor from the top level of the meta.yaml
    top_level_meta = {
            f"pangeo-forge-{k}": meta.get(k, 'none') for k in [
                'description', 
                'provenance',
                'maintainers',
            ]
            }

    attr_updates = recipe | top_level_meta
    
    # Information for reproducibility
    attr_updates['attrs_updated_source'] = f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/commit/{os.environ['GITHUB_SHA']}"
    attr_updates['attrs_updated_time_utc'] = timestamp
    
    check_path = update_zarr_attrs(store_path, attr_updates)