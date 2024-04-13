# proto_feedstock
A Prototype feedstock that implements independent metadata and data updates using pangeo forge

## Setup
### Build your recipe
- Edit the `feedstock/recipe.py` to build your pangeo-forge recipe. If you are new to pangeo-forge, [the docs](https://pangeo-forge.readthedocs.io/en/latest/composition/index.html#overview) are a great starting point
- Make sure to also edit the other files in the `/feedstock/` directory. More info on feedstock structure can be found [here](https://pangeo-forge.readthedocs.io/en/latest/deployment/feedstocks.html#meta-yaml)

### Test your recipe locally
Before we run your recipe on LEAPs Dataflow runner you should test your recipe locally.

You can do that on the LEAP-Pangeo Jupyterhub or your own computer.

1. Set up an environment with mamba or conda:
```shell
mamba create -n runner0102 python=3.11 -y
conda activate runner0102
pip install pangeo-forge-runner==0.10.2 --no-cache-dir
```

2. You can now use [pangeo-forge-runner](https://github.com/pangeo-forge/pangeo-forge-runner) from the root directory of this repository in the terminal:
```shell
pangeo-forge-runner bake \
  --repo=./ \
  --ref=main \
  --feedstock-subdir='feedstock' \
  --Bake.job_name=<recipe_id>\
  --Bake.recipe_id=<recipe_id>\
  -f config_local.py
```

>[!NOTE]
> Make sure to replace the `'recipe_id'` with the one defined in your `feedstock/meta.yaml` file.
>
>If you created multiple recipes you have to run a call like above for each one.


3. Check the output! If something looks off edit your recipe.
>[!TIP]
>The above command will by default 'prune' the recipe, meaning it will only use two of the input files you provided to avoid creating too large output.
>Keep that in mind when you check the output for correctness.

Once you are happy with the output it is time to commit your work to git, push to github and get this recipe set up for ingestion using [Google Dataflow](https://cloud.google.com/dataflow?hl=en)

### Deploy your recipe to LEAPs Google Dataflow

>[!WARNING]
>To proceed with this step you will need to have certain repository secrets set up. For security reasons this should be done by a memeber of the [LEAP Data and Computation Team](https://leap-stc.github.io/support.html#data-and-computation-team). Please open an issue on this repository and tag `@leap-stc/data-and-compute` to get assistance.

To deploy a recipe to Google Dataflow you have to trigger the "Deploy Recipes to Google Dataflow" with a single `recipe_id` as input.

### Add your dataset to the LEAP-Pangeo Catalog
Now that your awesome dataset is available as an ARCO zarr store, you should make sure that everyone else at LEAP can check this dataset out easily.

TBW: Instructions how to edit `feedstock/catalog.yaml`
