"""
A prototype based on MetaFlux
"""

import apache_beam as beam
from pangeo_forge_recipes.patterns import pattern_from_file_sequence
from pangeo_forge_recipes.transforms import (
    OpenURLWithFSSpec,
    OpenWithXarray,
    StoreToZarr,
    ConsolidateMetadata,
    ConsolidateDimensionCoordinates,
)

# Common Parameters
dataset_url = 'https://zenodo.org/record/7761881/files'


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
        store_name='proto_a.zarr',
        combine_dims=pattern_a.combine_dim_keys,
    )
    |ConsolidateCoordinates()
    |ConsolidateMetadata()
)

proto_b = (
    beam.Create(pattern_b.items())
    | OpenURLWithFSSpec()
    | OpenWithXarray()
    | StoreToZarr(
        store_name='proto_b.zarr',
        combine_dims=pattern_b.combine_dim_keys,
    )
    |ConsolidateCoordinates()
    |ConsolidateMetadata()
)
