# LEAP Template Feedstock
This repository serves as template/documentation/testing ground for Leap-Pangeo Data Library Feedstocks.

## Setup
Every dataset that is part of the LEAP-Pangeo Data Library is represented by a repository. You can easily create one by following the instructions below.

### Use this template
- Click on the button on the top left to use this repository as a template for your new feedstock
<img width="749" alt="image" src="https://github.com/leap-stc/proto_feedstock/assets/14314623/c786b2c7-adf1-4d4c-9811-0c7a1aa9228c">

>[!IMPORTANT]
> - Make the repo public
> - Make sure to create the repo under the `leap-stc` github organization, not your personal account!
> - Name your feedstock according to your data  `<your_data>_feedstock`.
> - Optional but encouraged: Give the `leap-stc/data-and-compute` team admin access (so we can make changes without bothering you). To do so go to `Settings > Collaborators and Teams > Add Teams` and add `leap-stc/data-and-compute` with admin role.
>
>  If you made a mistake here it is not a huge problem. All these settings can be changed after you created the repo.

- Now you can locally check out the repository.

> [!NOTE]
> The instructions below are specific for testing recipes locally but downloading and producing data on GCS cloud buckets. If you are running the recipes locally you have to minimally modify some of the steps as noted below.

### Are you linking or ingesting data?
If the data you want to work with is already available as ARCO format in a publically accessible cloud bucket, you can simply link it and add it to the LEAP catalog.

If you want to transform your dataset from e.g. a bunch of netcdf files into a zarr store you will have to build a recipe.

<details>
<summary>

#### Linking existing ARCO datasets

</summary>

To link an existing dataset all you need to do is to modify `'feedstock/meta.yaml'` and `'feedstock/catalog.yaml'`. Enter the information about the dataset in `'feedstock/meta.yaml'` and then add corresponding entries (the `'id'` parameter has to match) in `'feedstock/catalog.yaml'`, where the url can point to any publically available cloud storage.

<details>
<summary> Example from the [`arco-era5_feedstock](https://github.com/leap-stc/arco-era5_feedstock): </summary>

`meta.yaml`

```
title: "ARCO ERA5"
description: >
   Analysis-Ready, Cloud Optimized ERA5 data ingested by Google Research
recipes:
  - id: "0_25_deg_pressure_surface_levels"
  - id: "0_25_deg_model_levels"
provenance:
  providers:
    - name: "Google Research"
      description: >
      Hersbach, H., Bell, B., Berrisford, P., Hirahara, S., Horányi, A.,
      Muñoz‐Sabater, J., Nicolas, J., Peubey, C., Radu, R., Schepers, D.,
      Simmons, A., Soci, C., Abdalla, S., Abellan, X., Balsamo, G.,
      Bechtold, P., Biavati, G., Bidlot, J., Bonavita, M., De Chiara, G.,
      Dahlgren, P., Dee, D., Diamantakis, M., Dragani, R., Flemming, J.,
      Forbes, R., Fuentes, M., Geer, A., Haimberger, L., Healy, S.,
      Hogan, R.J., Hólm, E., Janisková, M., Keeley, S., Laloyaux, P.,
      Lopez, P., Lupu, C., Radnoti, G., de Rosnay, P., Rozum, I., Vamborg, F.,
      Villaume, S., Thépaut, J-N. (2017): Complete ERA5: Fifth generation of
      ECMWF atmospheric reanalyses of the global climate. Copernicus Climate
      Change Service (C3S) Data Store (CDS).

      Hersbach et al, (2017) was downloaded from the Copernicus Climate Change
      Service (C3S) Climate Data Store. We thank C3S for allowing us to
      redistribute the data.

      The results contain modified Copernicus Climate Change Service
      information 2022. Neither the European Commission nor ECMWF is
      responsible for any use that may be made of the Copernicus information
      or data it contains.
      roles:
        - producer
        - licensor
  license: "Apache Version 2.0"
maintainers:
  - name: "Julius Busecke"
    orcid: "0000-0001-8571-865X"
    github: jbusecke
```

`catalog.yaml`

```
# All the information important to cataloging.
"ncviewjs:meta_yaml_url": "https://github.com/leap-stc/arco-era5_feedstock/blob/main/feedstock/meta.yaml" # !!! Make sure to change this to YOUR feedstock!!!
tags:
  - atmosphere
  - reanalysis
  - zarr
stores:
  - id: "0_25_deg_pressure_surface_levels"
    name: "This dataset contains most pressure-level fields and all surface-level field regridded to a uniform 0.25° resolution. It is a superset of the data used to train GraphCast and NeuralGCM"
    url: "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"

  - id: "0_25_deg_model_levels"
    name: "This dataset contains 3D fields at 0.25° resolution with ERA5's native vertical coordinates (hybrid pressure/sigma coordinates)."
    url: "'gs://gcp-public-data-arco-era5/ar/model-level-1h-0p25deg.zarr-v1'"
```

</details>

</details>

<details>
<summary>

#### Build a Zarr recipe

</summary>

##### Build and test your recipe on the LEAP-Pangeo Jupyterhub

- Edit the `feedstock/recipe.py` to build your  recipe.

- Make sure to also edit the other files in the `/feedstock/` directory. More info on feedstock structure can be found [here](https://pangeo-forge.readthedocs.io/en/latest/deployment/feedstocks.html#meta-yaml)
- 🚨 You should not have to modify any of the files outside the `feedstock` folder (and this README)! If you run into a situation where you think changes are needed, please open an issue and tag @leap-stc/data-and-compute.

#### Test your recipe locally
- TODO:

#### Activate the linting CI and clean up your repo
[Pre-Commit](https://pre-commit.com) linting is already pre-configured in this repository. To run the checks locally simply do:
```shell
pip install pre-commit
pre-commit install
pre-commit run --all-files
```
Then create a new branch and add those fixes (and others that were not able to auto-fix). From now on pre-commit will run checks after every commit.

Alternatively (or additionally) you can use the  [pre-commit CI Github App](https://results.pre-commit.ci/) to run these checks as part of every PR.
To proceed with this step you will need assistance a memeber of the [LEAP Data and Computation Team](https://leap-stc.github.io/support.html#data-and-computation-team). Please open an issue on this repository and tag `@leap-stc/data-and-compute` and ask for this repository to be added to the pre-commit.ci app.



### Add your dataset to the LEAP-Pangeo Catalog
Now that your awesome dataset is available as an ARCO zarr store, you should make sure that everyone else at LEAP can check this dataset out easily.
Open a PR to our [catalog input file](https://github.com/leap-stc/data-management/blob/main/catalog/input.yaml) and add a link to this repos `'catalog.yaml'` there. See [here](https://github.com/leap-stc/data-management/pull/132) for an example PR for the [`arco-era5_feedstock](https://github.com/leap-stc/arco-era5_feedstock).

### Clean up

- [ ] Replace the instructions in this README.
