c.Bake.prune = 0
c.Bake.bakery_class = 'pangeo_forge_runner.bakery.local.LocalDirectBakery'
c.LocalDirectBakery.num_workers = 16
BUCKET_PREFIX = "./proto_feedstock/output"
c.TargetStorage.fsspec_class = "fsspec.implementations.local.LocalFileSystem"
c.TargetStorage.root_path = f"{BUCKET_PREFIX}/{{job_name}}/output"
c.InputCacheStorage.root_path = f"{BUCKET_PREFIX}/cache/"
c.InputCacheStorage.fsspec_class = "fsspec.implementations.local.LocalFileSystem"