"""
A synthetic prototype recipe
"""

import zarr
import os
from dataclasses import dataclass
from typing import List, Dict
import apache_beam as beam
from datetime import datetime, timezone
from pangeo_forge_recipes.patterns import pattern_from_file_sequence
from pangeo_forge_recipes.transforms import (
    OpenURLWithFSSpec,
    OpenWithXarray,
    StoreToZarr,
    ConsolidateMetadata,
    ConsolidateDimensionCoordinates,
)
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


# copied from cmip feedstock (TODO: move to central repo?)
@dataclass
class Copy(beam.PTransform):
    target: str

    def _copy(self, store: zarr.storage.FSStore) -> zarr.storage.FSStore:
        import os
        import zarr
        import gcsfs

        # We do need the gs:// prefix?
        # TODO: Determine this dynamically from zarr.storage.FSStore
        source = f"gs://{os.path.normpath(store.path)}/"  # FIXME more elegant. `.copytree` needs trailing slash
        if self.target is False:
            # dont do anything
            return store
        else:
            fs = gcsfs.GCSFileSystem()  # FIXME: How can we generalize this?
            fs.cp(source, self.target, recursive=True)
            # return a new store with the new path that behaves exactly like the input
            # to this stage (so we can slot this stage right before testing/logging stages)
            return zarr.storage.FSStore(self.target)

    def expand(self, pcoll: beam.PCollection) -> beam.PCollection:
        return pcoll | "Copying Store" >> beam.Map(self._copy)


@dataclass
class InjectAttrs(beam.PTransform):
    inject_attrs: dict

    def _update_zarr_attrs(self, store: zarr.storage.FSStore) -> zarr.storage.FSStore:
        # TODO: Can we get a warning here if the store does not exist?
        attrs = zarr.open(store, mode="a").attrs
        attrs.update(self.inject_attrs)
        # ? Should we consolidate here? We are explicitly doing that later...
        return store

    def expand(
        self, pcoll: beam.PCollection[zarr.storage.FSStore]
    ) -> beam.PCollection[zarr.storage.FSStore]:
        return pcoll | "Injecting Attributes" >> beam.Map(self._update_zarr_attrs)


def get_pangeo_forge_build_attrs() -> dict[str, Any]:
    """Get build information (git hash and time) to add to the recipe output"""
    # Set up injection attributes
    # This is for demonstration purposes only and should be discussed with the broader LEAP/PGF community
    # - Bake in information from the top level of the meta.yaml
    # - Add a timestamp
    # - Add the git hash
    # - Add link to the meta.yaml on main
    # - Add the recipe id

    git_url_hash = f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/commit/{os.environ['GITHUB_SHA']}"
    timestamp = datetime.now(timezone.utc).isoformat()

    return {
        "pangeo_forge_build_git_hash": git_url_hash,
        "pangeo_forge_build_timestamp": timestamp,
    }


# TODO: Both these stages are generally useful. They should at least be in the utils package, maybe in recipes?


def find_recipe_meta(catalog_meta: List[Dict[str, str]], r_id: str) -> Dict[str, str]:
    # Iterate over each dictionary in the list
    for d in catalog_meta:
        # Check if the 'id' key matches the search_id
        if d["id"] == r_id:
            return d
    print(
        f"Could not find {r_id=}. Got the following recipe_ids: {[d['id'] for d in catalog_meta]}"
    )
    return None  # Return None if no matching dictionary is found


# load the global config values (we will have to decide where these ultimately live)
catalog_meta = yaml.load(open("feedstock/catalog.yaml"))

if os.getenv("GITHUB_ACTIONS") == "true":
    print("Running inside GitHub Actions.")

    # Get final store path from catalog.yaml input
    target_small = find_recipe_meta(catalog_meta["stores"], "small")["url"]
    target_large = find_recipe_meta(catalog_meta["stores"], "large")["url"]
    pgf_build_attrs = get_pangeo_forge_build_attrs()
else:
    print("Running locally. Deactivating final copy stage.")
    # this deactivates the final copy stage for local testing execution
    target_small = False
    target_large = False
    pgf_build_attrs = {}

print("Final output locations")
print(f"{target_small=}")
print(f"{target_large=}")
print(f"{pgf_build_attrs=}")

## Monthly version
input_urls_a = [
    "gs://cmip6/pgf-debugging/hanging_bug/file_a.nc",
    "gs://cmip6/pgf-debugging/hanging_bug/file_b.nc",
]
input_urls_b = [
    "gs://cmip6/pgf-debugging/hanging_bug/file_a_huge.nc",
    "gs://cmip6/pgf-debugging/hanging_bug/file_b_huge.nc",
]

pattern_a = pattern_from_file_sequence(input_urls_a, concat_dim="time")
pattern_b = pattern_from_file_sequence(input_urls_b, concat_dim="time")


# small recipe
small = (
    beam.Create(pattern_a.items())
    | OpenURLWithFSSpec()
    | OpenWithXarray()
    | StoreToZarr(
        store_name="small.zarr",
        # FIXME: This is brittle. it needs to be named exactly like in meta.yaml...
        # Can we inject this in the same way as the root?
        # Maybe its better to find another way and avoid injections entirely...
        combine_dims=pattern_a.combine_dim_keys,
    )
    | InjectAttrs(pgf_build_attrs)
    | ConsolidateDimensionCoordinates()
    | ConsolidateMetadata()
    | Copy(target=target_small)
)

# larger recipe
large = (
    beam.Create(pattern_b.items())
    | OpenURLWithFSSpec()
    | OpenWithXarray()
    | StoreToZarr(
        store_name="large.zarr",
        combine_dims=pattern_b.combine_dim_keys,
    )
    | InjectAttrs(pgf_build_attrs)
    | ConsolidateDimensionCoordinates()
    | ConsolidateMetadata()
    | Copy(target=target_large)
)
