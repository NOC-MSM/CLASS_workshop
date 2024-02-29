"""
Created on 08/02/2024 by Chelsey Baker
Parcels test script to check the setup works
"""

#ONLY EDIT THIS SECTION
#choose a location and put in the longitude, latitude and depth below
#use google earth to check if you are not sure of lat/lon/depth of the region you are interested in

tlon=-36 #target lon - must be a number between -180 and 180 
tlat=55 #target lat - must be a number between -90 and 90 
tdepth=400 #target depth - must be a number between 2 and 5500 
runtime=30 #in days - must be less than 3650 days, 10 years=365*10 - align the time you want to run for with the yearstart and year end below
yearstart=2005 #year to start simulation - must be between 2005 and 2006 
yearend=2005 #year you want simulation to end - must be between 2005 and 2006 to keep the test short
outfile_name='test' #choose a file name - do not includes spaces
homedir='/home/users/train018/' #replace YOURUSERNAME with your username e.g. trainXXX so that it points to your home directory ##'/home/user/YOURUSERNAME/'

#DO NOT EDIT BELOW HERE
####################################################################################################################################################################################
#load python packages
from parcels import FieldSet, ParticleSet, ScipyParticle, JITParticle, AdvectionAnalytical, AdvectionRK4_3D, Variable
from glob import glob
import numpy as np
from datetime import timedelta as delta
from os import path
import math
from operator import attrgetter
from netCDF4 import Dataset
import netCDF4 as nc4
import xarray as xr

# meshgrid containing 10x10 points uniformly distributed in a [0,1]x[0,1] quad
vec = np.linspace(0, 1, 10)
vec2 = np.linspace(0, 1, 10)
xsi, eta = np.meshgrid(vec, vec2)

#get particles around target release point with a 5 degree box around the target location
relbox=5/2 #size of release box in degrees divided by 2
lonCorners = [tlon-relbox, tlon+relbox, tlon+relbox, tlon-relbox]
latCorners = [tlat-relbox, tlat-relbox, tlat+relbox, tlat+relbox]
lon_r = (1-xsi)*(1-eta) * lonCorners[0] + xsi*(1-eta) * lonCorners[1] + \
        xsi*eta * lonCorners[2] + (1-xsi)*eta * lonCorners[3] #create release longitude grid
lat_r = (1-xsi)*(1-eta) * latCorners[0] + xsi*(1-eta) * latCorners[1] + \
        xsi*eta * latCorners[2] + (1-xsi)*eta * latCorners[3] #create release latitude grid  

#create a list of release lons, lats and depths                    
lons1 = lon_r.flatten()
lats1 = lat_r.flatten()
depths1 = np.full([len(lons1)],tdepth)



def get_nemo_fieldset():
    data_dir = '/gws/pw/j07/workshop/users/lagran/'
    fnames = []
    ufiles = []
    vfiles = []
    wfiles = []
    mldfiles = []
  
    #bgcfiles = []
    mesh_path = '/gws/pw/j07/workshop/users/lagran/domain/'
    mesh_mask = mesh_path + 'mesh_hgr.nc'
    bathy_path = mesh_path + 'bathy_meter.nc'
    years = range(yearstart, yearend+2)
    for y in years:
        basepath = data_dir + str(y) + '/'
        fnames = str(basepath)

        
        
        
        ufilestemp = sorted(glob(fnames +'ORCA025-N06_*m*U.nc'))
        vfilestemp = sorted(glob(fnames +'ORCA025-N06_*m*V.nc'))
        wfilestemp = sorted(glob(fnames +'ORCA025-N06_*m*W.nc'))
        mldfilestemp = sorted(glob(fnames +'ORCA025-N06_*m*T.nc'))
        
        
        ufiles += ufilestemp
        vfiles += vfilestemp
        wfiles += wfilestemp
        mldfiles += mldfilestemp

    

        
    

    filenames = {'U': {'lon': mesh_mask, 'lat': mesh_mask, 'depth': wfiles[0], 'data': ufiles},
                 'V': {'lon': mesh_mask, 'lat': mesh_mask, 'depth': wfiles[0], 'data': vfiles},
                 'W': {'lon': mesh_mask, 'lat': mesh_mask, 'depth': wfiles[0], 'data': wfiles},
                 'MLD': {'lon': mesh_mask, 'lat': mesh_mask, 'data': mldfiles},
                 'BTY': {'lon': mesh_mask, 'lat': mesh_mask, 'data': bathy_path}}
                 

    
    variables = {'U': 'uo',
                 'V': 'vo',
                 'W': 'wo',
                 'MLD': 'mldr10_1',
                 'BTY': 'Bathymetry'}
    
    dimensions = {'U': {'lon': 'glamf', 'lat': 'gphif', 'depth': 'depthw', 'time': 'time_counter'},
                  'V': {'lon': 'glamf', 'lat': 'gphif', 'depth': 'depthw', 'time': 'time_counter'},
                  'W': {'lon': 'glamf', 'lat': 'gphif', 'depth': 'depthw', 'time': 'time_counter'},
                  'MLD': {'lon': 'glamf', 'lat': 'gphif', 'time': 'time_counter'},
                  'BTY': {'lon': 'glamf', 'lat': 'gphif'}}
    
    fieldset = FieldSet.from_nemo(filenames, variables, dimensions)
    return fieldset
    

fieldset = get_nemo_fieldset()

class mldParticle(JITParticle):
    mld = Variable('mld', dtype=np.float32, initial=np.nan)
    bathy = Variable('bathy', dtype=np.float32, initial=np.nan)

def mixld(particle, fieldset, time):
    particle.mld = fieldset.MLD[particle.time, particle.depth, particle.lat, particle.lon]
    particle.bathy = fieldset.BTY[particle.time, particle.depth, particle.lat, particle.lon]

def deleteParticle(particle, fieldset, time):
    particle.delete()

def boundarydrift(particle, fieldset, time):
    if particle.lon>180:
        particle.lon=particle.lon-360
    elif particle.lon<-180:
        particle.lon=particle.lon+360

pset = ParticleSet.from_list(fieldset=fieldset, pclass=mldParticle,
                             lon=lons1, #start longitude and latitude
                             lat=lats1, 
                             depth=depths1)

pfile = pset.ParticleFile(name=homedir+outfile_name+'.zarr', outputdt=delta(hours=120),chunks=(100, 10)) #output trajectory position every 5 days

kernels = pset.Kernel(AdvectionRK4_3D) + mixld + boundarydrift #choose advection scheme and include kernels
pset.execute(kernels, runtime=delta(days=runtime), dt=delta(hours=1), recovery={ErrorCode.ErrorOutOfBounds: deleteParticle}, output_file=pfile) #execute advection scheme, runtime= length of simulation, dt=Lagrangian timestep

print(pset)

pfile.close()


outfile=xr.open_zarr(homedir+outfile_name+'.zarr')

outfile.to_netcdf(homedir+outfile_name+'.nc')
