"""Example recipe"""

import xarray as xr
from distributed import Client
from obstore.store import S3Store
from zarr.storage import ObjectStore

# Optional: This will start a dask distributed client for parallel processing.
client = Client()
print(client.scheduler.address)


# ---------- Input files ------------------
# Starting with a subset of your input files can be helpful for testing.
input_urls = ['https://<data-provider>/../../<file1.nc>']


# ---------- Combine ----------------------
# Note: there are lots of ways to create a Zarr store from a collection of archival files.
# Chat with the data and compute team if you have questions.
# The example here opens up a collection of file urls with Xarray's open_mfdataset
ds = xr.open_mfdataset(
    input_urls, chunks={}, parallel=True, coords='minimal', data_vars='minimal', compat='override'
)

# ---------- Chunk ----------------------
# Note: Chunking your dataset is important for your analysis use case! ie. time-series vs spatial analysis
# A good rule of thumb 100MB chunk sizes.
ds = ds.chunk({'time': 10, 'lat': 180, 'lon': 360})


# ---------- WRITE ----------------------
# This example writes to LEAP's OSN inbox bucket.

# UPDATE THIS!
DATASET_NAME = '<INSERT_YOUR_DATASET_NAME_HERE>'

osnstore = S3Store(
    'leap-pangeo-inbox',
    prefix=f'{DATASET_NAME}/{DATASET_NAME}.zarr',
    aws_endpoint='https://nyu1.osn.mghpcc.org',
    access_key_id='<ASK LEAP DCT MEMBERS FOR CREDENTIALS>',
    secret_access_key='<ASK LEAP DCT MEMBERS FOR CREDENTIALS>',
    client_options={'allow_http': True},
)
zstore = ObjectStore(osnstore)

ds.to_zarr(
    zstore,
    zarr_format=3,
    consolidated=False,
    mode='w',
)
