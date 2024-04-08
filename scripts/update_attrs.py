# This script updates the attributes of all the zarr stores that are created by the recipe, based on the current version of meta.yaml

import zarr
import os
import pathlib
from ruamel.yaml import YAML
yaml = YAML(typ='safe')
import gcsfs
from datetime import datetime, timezone

fs = gcsfs.GCSFileSystem()

# # For later, get the current git hash and add to the updated attribute
git_hash = os.popen('git rev-parse HEAD').read().strip()
timestamp = datetime.now(timezone.utc).isoformat()

# read info from meta.yaml
meta_path = './feedstock/meta.yaml'
meta = yaml.load(pathlib.Path(meta_path))

def update_zarr_attrs(store_path:str, additonal_attrs:dict):
    """
    Update the attributes of a zarr store with the given dictionary
    """
    store = zarr.open(zarr.storage.FSStore(pathlib.Path(store_path)), mode='a')
    store.attrs.update(additonal_attrs)
    zarr.convenience.consolidate_metadata(store_path) #Important: do not pass the store object here!
    return store_path

# Loop over each recipe 
for recipe in meta['recipes']:
    id = recipe['id']
    assert 'object' in recipe.keys() #(FIXME: this does not support dict objects yet...)

    # Some how get the store path from the recipe
    store_path = f'gs://leap-scratch/jbusecke/proto_feedstock/{id}.zarr' # how can I extract this for multiple recipes using the config files?

    # Check if store exists and otherwise give a useful warning
    if not fs.exists(store_path):
        print(f"Warning: Store {store_path} does not exist. Skipping.")
        continue

    # add the infor from the top level of the meta.yaml
    top_level_meta = {
            k: meta.get(k, 'none') for k in [
                'description', 
                'provenance',
                'maintainers',
            ]
            }

    attr_updates = recipe | top_level_meta
    
    # Information for reproducibility
    attr_updates['attrs_updated_git_hash'] = git_hash
    attr_updates['attrs_updated_time_utc'] = timestamp 
    check_path = update_zarr_attrs(store_path, attr_updates)
    print(f"Updated {check_path} with {attr_updates=}")