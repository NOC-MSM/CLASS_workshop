## Notebooks

This directory contains the main materials for the AMM componennt of the 
workshop.

Users can configure the appropriate conda environment by taking the following
steps :

1) First login to your JASMIN user area and login to a sci machine
```
ssh sci1
```

2) Ensure jaspy is loaded
```
module load jaspy
```

3) Initialise conda. Once initialised, you will need to refresh the session 
   using `exit` then `ssh sci1`.
```
conda init
```

4) create conda environment (using mamba - it is faster!)
```
mamba env create -f environment.yml
```

5) Activate conda environment
```
conda activate coast_wrk_shp
```

6) Add environment to ipython kernel
```
conda run --name coast_wrk_shp python -m ipykernel install --user --name coast_wrk_shp
```
