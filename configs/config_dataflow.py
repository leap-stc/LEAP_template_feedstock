# FEEDSTOCK_NAME = "proto_feedstock"  # Can we get this at runtime?
c.Bake.prune = 1
c.Bake.bakery_class = "pangeo_forge_runner.bakery.dataflow.DataflowBakery"
c.DataflowBakery.use_dataflow_prime = False
c.DataflowBakery.use_public_ips = True
c.DataflowBakery.service_account_email = (
    "julius-leap-dataflow@leap-pangeo.iam.gserviceaccount.com"
)
c.DataflowBakery.project_id = "leap-pangeo"
c.DataflowBakery.temp_gcs_location = f"gs://leap-scratch/data-library/feedstocks/temp/{FEEDSTOCK_NAME}"
c.TargetStorage.fsspec_class = "gcsfs.GCSFileSystem"
c.InputCacheStorage.fsspec_class = "gcsfs.GCSFileSystem"
c.TargetStorage.root_path = f"gs://leap-scratch/data-library/feedstocks/output/{FEEDSTOCK_NAME}/{{job_name}}/output"
c.InputCacheStorage.root_path = f"gs://leap-scratch/data-library/feedstocks/cache"  # make this a global cache?
