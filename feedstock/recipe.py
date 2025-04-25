"""Example recipe"""

import xarray as xr
from distributed import Client

client = Client()
client

input_urls = ['https://<data-provider>/../../<file1.nc>']


# Note: there are lots of ways to create a Zarr store from a collection of archival files.
# Chat with the data and compute team if you have questions.
# The example here opens up a collection of file urls with Xarray's open_mfdataset
# which.. can be difficult for very large datasets.

ds = xr.open_mfdataset(
    input_urls, chunks={}, parallel=True, coords='minimal', data_vars='minimal', compat='override'
)

# Note: Chunking your dataset is important for your analysis use case! ie. time-series vs spatial analysis
# A good rule of thumb 100MB chunk sizes.

ds = ds.chunk({'time': 10, 'lat': 180, 'lon': 360})

# Good practice is trying to build a smaller Zarr from a subset of your inputs files for testing.
# Note: This writes to leap-scratch. Once we all feel good about the recipe, we can write to leap-persistant.
ds.to_zarr(
    'gs://leap-scratch/<your_user_name>/<dataset_name.zarr>',
    zarr_format=3,
    consolidated=False,
    mode='w',
)
