# proto_feedstock
A Prototype feedstock that implements independent metadata and data updates using pangeo forge

## Setup
You need to set the repo action secret `"GCP_DATAFLOW_SERVICE_KEY"` as an auth JSON to a service account that has access to both storage and dataflow.

## What does this do?

### Update output zarr attrs from meta.yaml

### Run a full recipe

## How to run locally
mamba create -n runner0102 python=3.11 -y
conda activate runner0102
pip install pangeo-forge-runner==0.10.2 --no-cache-dir

pangeo-forge-runner bake \
  --repo=https://github.com/leap-stc/proto_feedstock.git \
  --ref=main \
  --feedstock-subdir='feedstock' \
  --Bake.job_name=proto_a\
  --Bake.recipe_id=proto_a\
  -f config_local.py