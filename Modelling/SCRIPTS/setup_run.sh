#################################################################
# 		SCRIPT TO SETUP THE EXPERIMENTAL MODEL RUN
#################################################################
#

cd $EXP

#Copy the runfiles into the run directory 
cp $EXTRA/SETUP/* ./


#Link the necessary files into the run directory: 
mkdir SURFACE_FORCING
mkdir BOUNDARY_FORCING
mkdir TIDES


ln -s $EXTRA/SURFACE_FORCING/* ./SURFACE_FORCING/
ln -s $EXTRA/BOUNDARY_FORCING/* ./BOUNDARY_FORCING/
ln -s $EXTRA/BOUNDARY_FORCING/coordinates.bdy.nc ./
ln -s $EXTRA/TIDES/* ./TIDES/
ln -s $EXTRA/DOMAIN/domain_cfg.nc ./
ln -s $EXTRA/DOMAIN/coordinates.nc ./
ln -s $NEMO/cfgs/$CONFIG/BLD/bin/nemo.exe ./
ln -s $XIOS_DIR/bin/xios_server.exe ./

mkdir restarts 
cp $EXTRA/INITIAL_CONDITIONS/SANH_2017_restart_NEW.nc ./restarts/
cp $RIVERS/rivers_y2017.nc ./

# Update namelist_cfg 

# Submit the job

sbatch job_run.slurm 


# Check the status of your job submission by using:

squeue -u your_username 





















