
############################################################
# ********	DOWNLOAD AND INSTALL XIOS	*********
############################################################

#-----------------------------------------------------------
# 1. LOAD MODULES 
#-----------------------------------------------------------

cd $WDIR

module swap craype-network-ofi craype-network-ucx
module swap cray-mpich cray-mpich-ucx
module load cray-hdf5-parallel/1.12.2.1
module load cray-netcdf-hdf5parallel/4.9.0.1

#-----------------------------------------------------------
# 2. DOWNLOAD AND COMPILE XIOS 
#-----------------------------------------------------------

# Download XIOS
svn checkout http://forge.ipsl.jussieu.fr/ioserver/svn/XIOS/branchs/xios-2.5 $XIOS_DIR
cd $XIOS_DIR

# Copy the architecture file 
#cp /work/n01/shared/nemo/xios-2.5/arch/arch-X86_ARCHER2-Cray.* arch/.
cp $EXTRA/XIOS/ARCH/arch-X86_ARCHER2-Cray.* arch/.

# Compile XIOS
./make_xios --prod --arch X86_ARCHER2-Cray --netcdf_lib netcdf4_par --full --job 4

# ATTENTION! The first compile will fail - this is okay!  
# Need to go to $XIOS_DIR/tools/FCM/lib/Fcm/Config.pm and change:
# FC_MODSEARCH => '',             # FC flag, specify "module" path
#to
#FC_MODSEARCH => '-J',           # FC flag, specify "module" path  
sed -i "s/FC_MODSEARCH => ''/FC_MODSEARCH => '-J'/g" tools/FCM/lib/Fcm/Config.pm

# Now recompile XIOS. This time it should work. 
./make_xios --prod --arch X86_ARCHER2-Cray --netcdf_lib netcdf4_par --full --job 4


cd $SCRIPTS


############################################################
#      ****** 		FINISHED!! 		*******
############################################################

