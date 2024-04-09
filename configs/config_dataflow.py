
FEEDSTOCK_NAME = "proto_feedstock" #Can we get this at runtime?
BUCKET_PREFIX = f"gs://leap-scratch/jbusecke/{FEEDSTOCK_NAME}" #FIXME: Change to data-library eventually
c.Bake.prune = 0
c.Bake.bakery_class = "pangeo_forge_runner.bakery.dataflow.DataflowBakery"
c.DataflowBakery.use_public_ips = True
c.DataflowBakery.service_account_email = "julius-leap-dataflow@leap-pangeo.iam.gserviceaccount.com"
c.DataflowBakery.project_id = "leap-pangeo"
c.DataflowBakery.temp_gcs_location = f"{BUCKET_PREFIX}/temp"
c.DataflowBakery.use_dataflow_prime = False
c.TargetStorage.fsspec_class = "gcsfs.GCSFileSystem"
c.InputCacheStorage.fsspec_class = "gcsfs.GCSFileSystem"
c.TargetStorage.root_path = f"{BUCKET_PREFIX}/{{job_name}}/output"
c.InputCacheStorage.root_path = f"{BUCKET_PREFIX}/cache/" # make this a global cache?