c.Bake.prune = 1
c.Bake.bakery_class = "pangeo_forge_runner.bakery.local.LocalDirectBakery"
# BUCKET_PREFIX = "gs://leap-scratch/<username>/<feedstock_name>/" # replace <> values and uncomment
c.TargetStorage.fsspec_class = "gcsfs.GCSFileSystem"
c.InputCacheStorage.fsspec_class = "gcsfs.GCSFileSystem"
c.TargetStorage.root_path = f"{BUCKET_PREFIX}/output/{{job_name}}"
c.InputCacheStorage.root_path = f"{BUCKET_PREFIX}/cache/"
