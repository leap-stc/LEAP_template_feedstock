# This assumes that runner is called from a github action
# where these environment variables are set.
import os
repo_path = os.environ['GITHUB_REPOSITORY']
access_key_id = os.environ['OSN_LEAP_PIPELINE_KEY']
secret_access_key = os.environ['OSN_LEAP_PIPELINE_KEY_SECRET']

FEEDSTOCK_NAME = repo_path.split('/')[-1]

c.Bake.prune = 1
c.Bake.bakery_class = "pangeo_forge_runner.bakery.dataflow.DataflowBakery"
c.DataflowBakery.use_dataflow_prime = True
c.DataflowBakery.max_workers = 50
c.DataflowBakery.use_public_ips = True
c.DataflowBakery.service_account_email = (
    "leap-community-bakery@leap-pangeo.iam.gserviceaccount.com"
)

c.DataflowBakery.project_id = "leap-pangeo"
c.DataflowBakery.temp_gcs_location = f"gs://leap-scratch/data-library/feedstocks/temp/{FEEDSTOCK_NAME}"
c.InputCacheStorage.fsspec_class = "gcsfs.GCSFileSystem"
c.InputCacheStorage.root_path = f"gs://leap-scratch/data-library/feedstocks/cache"

s3_args = {
       "key": access_key_id,
       "secret": secret_access_key,
       "client_kwargs":{"endpoint_url":"https://nyu1.osn.mghpcc.org"}
   }

c.TargetStorage.fsspec_class = "s3fs.S3FileSystem"
c.TargetStore.fsspec_args = s3_args
c.TargetStorage.root_path = f"leap-pangeo-pipeline/{FEEDSTOCK_NAME}/"
