# create a 'catalog zarr' for any given recipe
import os
import json
import zarr
import xarray as xr
from ruamel.yaml import YAML
yaml = YAML(typ='safe')

# grap the recipe id from envionment variables
recipe_id = os.environ['RECIPE_ID'] # id rather fail here then have weird 'None...' stores

# load the global config values (we will have to decide where these ultimately live)
catalog_meta = yaml.load(open('feedstock/catalog.yaml'))
recipe_meta = catalog_meta['recipes'][recipe_id]

data_prefix = catalog_meta['data_store_prefix']
catalog_prefix = catalog_meta['catalog_store_prefix']

data_store_path = os.path.join(data_prefix,f"{recipe_id}.zarr")
catalog_store_path = os.path.join(catalog_prefix,f"{recipe_id}-catalog.zarr")
pyramid_store_path = recipe_meta['pyramid_store_path']

def parse_cf_for_ncviewjs(store: zarr.storage.FSStore) -> zarr.storage.FSStore:
    """Logic to add the necessary cf attributes to a zarr store for ncviewjs"""
    return {}

parsed_attrs = parse_cf_for_ncviewjs(zarr.storage.FSStore(data_store_path))

bake_attrs = parsed_attrs | recipe_meta['extra_metadata']

print(bake_attrs)
print(f"{data_store_path=}")
print(f"{catalog_store_path=}")

ds = xr.Dataset(attrs=bake_attrs)
ds.to_zarr(catalog_store_path, mode='w')


