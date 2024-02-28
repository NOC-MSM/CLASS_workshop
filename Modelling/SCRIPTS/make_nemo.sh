 
#################################################################
# *******	DOWNLOAD AND COMPILE NEMO 	**********
#################################################################

#---------------------------------------------------------------
#1. DOWNLOAD NEMO
#--------------------------------------------------------------

cd $WDIR

# Download NEMO  (only use firts time you install. Comment out before compiling once nemo is installed)
svn co http://forge.ipsl.jussieu.fr/nemo/svn/NEMO/branches/UKMO/NEMO_4.0.4_mirror NEMO_4.0.4 


#---------------------------------------------------------------
#2. LOAD MODULES
#---------------------------------------------------------------


module swap craype-network-ofi craype-network-ucx
module swap cray-mpich cray-mpich-ucx
module load cray-hdf5-parallel/1.12.2.1
module load cray-netcdf-hdf5parallel/4.9.0.1


#----------------------------------------------------------------
#3. COMPILING NEMO 
#----------------------------------------------------------------
# Get the Architecture file 
#ATTENTION modify the following file to have the correct path for xios


#cp /work/n01/shared/nemo/ARCH/arch-X86_ARCHER2-Cray.fcm $NEMO/arch/arch-X86_ARCHER2-Cray.fcm
cp $EXTRA/NEMO/ARCH/arch-X86_ARCHER2-Cray.fcm $NEMO/arch/arch-X86_ARCHER2-Cray.fcm

cd $NEMO
# go to ext/FCM/lib/Fcm/Config.pm and change
# FC_MODSEARCH => '',             # FC flag, specify "module" path
#to
#FC_MODSEARCH => '-J',           # FC flag, specify "module" path
sed -i "s/FC_MODSEARCH => ''/FC_MODSEARCH => '-J'/g" ext/FCM/lib/Fcm/Config.pm


cd $NEMO
# Compile NEMO first to create necessary folders
./makenemo -n $CONFIG -r AMM12  -m X86_ARCHER2-Cray -j 16


# The MY_SRC directory in $CDIR contains files that tell NEMO how to run. 
# E.g. The key file "unlocks" the different modules we want NEMO to use. We can use the MY_SRC dir to incorporate any changes into the main code without changing the core scripts. 
# Copy over the key and necessary MY_SRC file to your configuration directory:
cd $CDIR/$CONFIG
cp $EXTRA/cpp_DEMO.fcm cpp_$CONFIG.fcm
cp -r $EXTRA/MY_SRC ./


# Compile NEMO with updates included 
cd $NEMO
./makenemo -r $CONFIG -m X86_ARCHER2-Cray -j 16 clean
./makenemo -r $CONFIG -m X86_ARCHER2-Cray -j 16


cd $SCRIPTS


##############################################################
# 		*****	FINISHED!!	*****
##############################################################

