## Notebooks

This directory contains the main materials for the AMM componennt of the 
workshop.

Users can configure the appropriate conda environment by taking the following
steps:

1) Ensure jaspy is loaded

``module load jaspy``

2) create conda environment

``conda env create -f environment.yml``

3) activate conda environment

``conda activate coast_wrk_sh``

4) add environment to ipython kernel
``conda run --name coast_wrk_shp python -m ipykernel install --user --name coast_wrk_shp``
