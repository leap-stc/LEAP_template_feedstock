"""
A prototype based on MetaFlux
"""
import zarr
import os
from dataclasses import dataclass
import apache_beam as beam
from pangeo_forge_recipes.patterns import pattern_from_file_sequence
from pangeo_forge_recipes.transforms import (
    OpenURLWithFSSpec,
    OpenWithXarray,
    StoreToZarr,
    ConsolidateMetadata,
    ConsolidateDimensionCoordinates,
)

# copied from cmip feedstock (TODO: move to central repo?)
@dataclass
class Copy(beam.PTransform):
    target_prefix: str
    
    def _copy(self,store: zarr.storage.FSStore) -> zarr.storage.FSStore:
        import os
        import zarr
        import gcsfs
        # We do need the gs:// prefix? 
        # TODO: Determine this dynamically from zarr.storage.FSStore
        source = f"gs://{os.path.normpath(store.path)}/" #FIXME more elegant. `.copytree` needs trailing slash
        target = os.path.join(*[self.target_prefix]+source.split('/')[-3:])
        # gcs = gcsio.GcsIO()
        # gcs.copytree(source, target)
        print(f"HERE: Copying {source} to {target}")
        fs = gcsfs.GCSFileSystem()
        fs.cp(source, target, recursive=True)
        # return a new store with the new path that behaves exactly like the input 
        # to this stage (so we can slot this stage right before testing/logging stages)
        return zarr.storage.FSStore(target)
        
    def expand(self, pcoll: beam.PCollection) -> beam.PCollection:
        return (pcoll
            | "Copying Store" >> beam.Map(self._copy)
        )

# Common Parameters
dataset_url = 'https://zenodo.org/record/7761881/files'
latest_store_prefix = 'gs://leap-scratch/jbusecke/proto_feedstock/latest/'

## Monthly version
input_urls_a = [f'{dataset_url}/METAFLUX_GPP_RECO_monthly_{y}.nc' for y in range(2001, 2003)]
input_urls_b = [f'{dataset_url}/METAFLUX_GPP_RECO_monthly_{y}.nc' for y in range(2003, 2005)]

pattern_a = pattern_from_file_sequence(input_urls_a, concat_dim='time')
pattern_b = pattern_from_file_sequence(input_urls_b, concat_dim='time')

proto_a = (
    beam.Create(pattern_a.items())
    | OpenURLWithFSSpec()
    | OpenWithXarray()
    | StoreToZarr(
        store_name='proto-a.zarr', 
        #FIXME: This is brittle. it needs to be named exactly like in meta.yaml...
        # Can we inject this in the same way as the root?
        # Maybe its better to find another way and avoid injections entirely...
        combine_dims=pattern_a.combine_dim_keys,
    )
    |ConsolidateDimensionCoordinates()
    |ConsolidateMetadata()
    |Copy(target_prefix=latest_store_prefix)
)

proto_b = (
    beam.Create(pattern_b.items())
    | OpenURLWithFSSpec()
    | OpenWithXarray()
    | StoreToZarr(
        store_name='proto-b.zarr',
        combine_dims=pattern_b.combine_dim_keys,
    )
    |ConsolidateDimensionCoordinates()
    |ConsolidateMetadata()
    |Copy(target_prefix=latest_store_prefix)
)
