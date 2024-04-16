# proto_feedstock
The prototype (and future template) of a LEAP-Pangeo feedstock.

## Setup
### Use this template
Click on the button on the top left to use this repository as a template for your new feedstock
<img width="749" alt="image" src="https://github.com/leap-stc/proto_feedstock/assets/14314623/c786b2c7-adf1-4d4c-9811-0c7a1aa9228c">


Name your feedstock according to your data  `<your_data>_feedstock`.

>[!WARNING]
> - Make sure to create the repo under the `leap-stc` github organization, not your personal account! If you already did that, you can always transfer the ownership afterwards.
> - Name your feedstock according to your data  `<your_data>_feedstock`. 

Now you can locally check out the repository.

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

2. You can now use [pangeo-forge-runner](https://github.com/pangeo-forge/pangeo-forge-runner) from the root directory of a checked out version of this repository in the shell

```shell
pangeo-forge-runner bake \
  --repo=./ \
  --ref=main \
  --feedstock-subdir='feedstock' \
  --Bake.job_name=<recipe_id>\
  --Bake.recipe_id=<recipe_id>\
  -f configs/config_local.py
```
>[!NOTE]
> Make sure to replace the `'recipe_id'` with the one defined in your `feedstock/meta.yaml` file.
>
>If you created multiple recipes you have to run a call like above for each one.

> This will save the cache and output to a subfolder of the location you are executing this from.
> If you are working on the LEAP-Pangeo hub you can just swap `configs/config_local.py` with `configs/config_local_hub.py`. This will still execute the recipe locally, but the cache and data will be stored on the LEAP scratch bucket ( under `gs://leap-scratch/<user>/<repo_name>` where `user` is your username and `repo_name` is the name of the checked out repository) and thus not exceed your allowed storage on the User Directory.




3. Check the output! If something looks off edit your recipe.
>[!TIP]
>The above command will by default 'prune' the recipe, meaning it will only use two of the input files you provided to avoid creating too large output.
>Keep that in mind when you check the output for correctness.

Once you are happy with the output it is time to commit your work to git, push to github and get this recipe set up for ingestion using [Google Dataflow](https://cloud.google.com/dataflow?hl=en)

### Activate the linting CI and clean up your repo
[Pre-Commit](https://pre-commit.com) linting is already pre-configured in this repository. To run the checks locally simply do:
```shell
pip install pre-commit
pre-commit install
pre-commit run --all-files
```
Then create a new branch and add those fixes (and others that were not able to auto-fix). From now on pre-commit will run checks after every commit.

Alternatively (or additionally) you can use the  [pre-commit CI Github App](https://results.pre-commit.ci/) to run these checks as part of every PR.
To proceed with this step you will need assistance a memeber of the [LEAP Data and Computation Team](https://leap-stc.github.io/support.html#data-and-computation-team). Please open an issue on this repository and tag `@leap-stc/data-and-compute` and ask for this repository to be added to the pre-commit.ci app.

### Deploy your recipe to LEAPs Google Dataflow

>[!WARNING]
>To proceed with this step you will need to have certain repository secrets set up. For security reasons this should be done by a memeber of the [LEAP Data and Computation Team](https://leap-stc.github.io/support.html#data-and-computation-team). Please open an issue on this repository and tag `@leap-stc/data-and-compute` to get assistance.

To deploy a recipe to Google Dataflow you have to trigger the "Deploy Recipes to Google Dataflow" with a single `recipe_id` as input.

### Add your dataset to the LEAP-Pangeo Catalog
Now that your awesome dataset is available as an ARCO zarr store, you should make sure that everyone else at LEAP can check this dataset out easily.

TBW: Instructions how to edit `feedstock/catalog.yaml`
