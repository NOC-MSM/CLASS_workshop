 #-----------------------------------------------------------
 #        SCRIPT FOR GENERATING THE FORCING WEIGHTS 
 #----------------------------------------------------------
 

# Load modules in a new terminal window

module swap craype-network-ofi craype-network-ucx
module swap cray-mpich cray-mpich-ucx
module load cray-hdf5-parallel/1.12.2.1
module load cray-netcdf-hdf5parallel/4.9.0.1


# Create a new directory and link your forcing and coordinates file there: 

cd $WDIR
mkdir WEIGHTS
cd WEIGHTS
ln -s $EXTRA/DOMAIN/coordinates.nc ./
ln -s $EXTRA/SURFACE_FORCING/ERA_MSL_y2017.nc ./

# Copy over the namelist files to create the weights:
cp $EXTRA/WEIGHTS/namelist* ./

#Create the weights: 

$TDIR/WEIGHTS/scripgrid.exe namelist_reshape_bilin_atmos
$TDIR/WEIGHTS/scrip.exe namelist_reshape_bilin_atmos
$TDIR/WEIGHTS/scripshape.exe namelist_reshape_bilin_atmos
$TDIR/WEIGHTS/scrip.exe namelist_reshape_bicubic_atmos
$TDIR/WEIGHTS/scripshape.exe namelist_reshape_bicubic_atmos
