Installation
============

This is a beta library, so the only installation is a development install. To install:

 1. clone the code repository `git clone https://github.com/USGS-Astrogeology/automated-metadata-generation`
 2. `cd` into the repository
 3. and create a conda environment using `conda create -n amg -f environment.yml`
 4. then activate the conda environment `conda activate amg`
 5. install this library `python setup.py develop`

Development Installation
========================
Is identical to the standard installation except the dev environment.yml should be used in the third step:

`conda create -n amg -f environment-dev.yml`