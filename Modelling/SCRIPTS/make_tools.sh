###################################################################
#		*** MAKE THE NEMO TOOLS ***
###################################################################

#------------------------------------------------------------------
# 1. Load the modules 
#------------------------------------------------------------------

cd $WDIR

module swap craype-network-ofi craype-network-ucx
module swap cray-mpich cray-mpich-ucx
module load cray-hdf5-parallel/1.12.2.1
module load cray-netcdf-hdf5parallel/4.9.0.1


#-------------------------------------------------------------------
# 2. Apply the patches 
#-------------------------------------------------------------------

# Apply the necessary patches to the weight file code: 

cd $NEMO/tools/WEIGHTS/src
patch -b < $EXTRA/patch_files/scripinterp_mod.patch
patch -b < $EXTRA/patch_files/scripinterp.patch
patch -b < $EXTRA/patch_files/scrip.patch
patch -b < $EXTRA/patch_files/scripshape.patch
patch -b < $EXTRA/patch_files/scripgrid.patch


# And finally compile the NEMO tools: 

cd $NEMO/tools
./maketools -m X86_ARCHER2-Cray -n NESTING
./maketools -m X86_ARCHER2-Cray -n REBUILD_NEMO
./maketools -m X86_ARCHER2-Cray -n WEIGHTS
./maketools -m X86_ARCHER2-Cray -n DOMAINcfg

cd $SCRIPTS


#####################################################################
#       	***		FINISHED!!!		***
#####################################################################	

