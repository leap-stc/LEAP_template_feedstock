# This script updates the attributes of all the zarr stores that are created by the recipe, based on the current version of meta.yaml

import zarr
import pathlib
from ruamel.yaml import YAML
yaml = YAML(typ='safe')

# # For later, get the current git hash and add to the updated attribute
# git_hash = os.popen('git rev-parse HEAD').read().strip()

# read info from meta.yaml
meta_path = './feedstock/meta.yaml'
meta = yaml.load(pathlib.Path(meta_path))

# Loop over each recipe 
for recipe in meta['recipes']:
    id = recipe['id']
    assert 'object' in recipe.keys() #(FIXME: this does not support dict objects yet...)

    # Some how get the store path from the recipe
    store_path = f'gs://leap-scratch/jbusecke/proto_feedstock/{id}.zarr' # how can I extract this for multiple recipes using the config files?

    fsstore = zarr.storage.FSStore(store_path)

    # Check if store exists and otherwise give a useful warning
    if not fsstore.exists(''):
        print(f"Warning: Store {store_path} does not exist. Skipping.")
        continue

    # Get the current store object
    store = zarr.open(fsstore, mode='a')

    # add the infor from the top level of the meta.yaml
    top_level_meta = {
            k: meta.get(k, 'none') for k in [
                'description', 
                'provenance',
                'maintainers',
            ]
            }

    meta_updates = recipe | top_level_meta
    
    ## For later: Add the git hash as 'git_hash_attrs_updated'
    # meta_updates['git_hash_attrs_updated'] = git_hash
    meta_updates['git_hash_attrs_updated'] = 'some_fake_hash'
    
    store.attrs.update(meta_updates)
    zarr.convenience.consolidate_metadata(store_path) #Important: do not pass the store object here!


