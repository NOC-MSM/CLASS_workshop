#load packages
import matplotlib.pyplot as plt
from matplotlib import cm
from netCDF4 import Dataset
import netCDF4 as nc4
import numpy as np
from cartopy import config
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import math
import geopy.distance

outfile=nc4.Dataset('/home/users/train018/output_5yrs2.nc','r',format='NETCDF4') #edit the file location and name of your outfile here

#read in trajectories
lat=outfile.variables['lat'][:,:].T #latitude in degrees 
lon=outfile.variables['lon'][:,:].T #longitude in degrees
depth=outfile.variables['z'][:,:].T #depth in meters
time=outfile.variables['time'][:,:].T #time in seconds

#convert time variable
time_days=time.copy()/86400 #number of seconds in a day 

#we have also divided the fill value of -9.22337204e+18 by 86400 - let's get rid of this
time_days[time_days==-106751991167300.64]=np.nan #replace with NaNs



#mean, median and max depth
print('Mean depth of simulation (m)')
print(np.round(np.nanmean(depth)))

print('Median depth of simulation (m)')
print(np.round(np.nanmedian(depth)))

print('Maximum depth of simulation (m)')
print(np.round(np.nanmax(depth)))

#mean and max depth change
depth_change=depth.copy()-(depth[0,0])
print('Mean depth change (m) - negative numbers = shallower trajectory')
print(np.round(np.nanmean(depth_change)))

print('Maximum depth change (m)')
print(np.round(np.nanmax(depth_change)))


#calculate distance travelled - straight line from release location to finish location

#find location of last trajectory timestep
endtraj_idx=np.argwhere(time_days[:,0]==np.nanmax(time_days[:,0])) #use the maximum time value to find the end of the trajectory

#define function to calculate the start to end (or A to B) distance
def dist_a2b(lat,lon):
    dist=np.full(len(lat[0,:]),np.nan) #allocate the distance variable
    for i in range(0,len(lat[0,:]),1):
        coords_1 = (lat[0,i], lon[0,i])
        coords_2 = (lat[endtraj_idx,i], lon[endtraj_idx,i])    
        dist[i]=geopy.distance.geodesic(coords_1, coords_2).km
        
        del coords_1
        del coords_2

    return dist


#run the function
traj_dist_a2b=dist_a2b(lat,lon)

print('Mean distance travelled - start to end (km)')
print(np.round(np.nanmean(traj_dist_a2b)))

print('Maximum distance travelled - start to end (km)')
print(np.round(np.nanmax(traj_dist_a2b)))

#distance travelled along trajectory
#define function to calculate the along trajectory or cumulative distance
def dist_cumulative(lat,lon):
    dist=np.full(len(lat[0,:]),np.nan) #allocate the distance variable
    for i in range(0,len(lat[0,:]),1):
        dist[i]=0
        for j in range(0,int(endtraj_idx),1):

            coords_1 = (lat[j,i], lon[j,i])
            coords_2 = (lat[j+1,i], lon[j+1,i])    
            dist[i]+=geopy.distance.geodesic(coords_1, coords_2).km
        
            del coords_1
            del coords_2

    return dist

#run the function
traj_dist_cumulative=dist_cumulative(lat,lon)

print('Mean distance travelled - cumulative (km)')
print(np.round(np.nanmean(traj_dist_cumulative)))

print('Maximum distance travelled - cumulative (km)')
print(np.round(np.nanmax(traj_dist_cumulative)))


#mean, median and max speed
traj_speed_kmd=traj_dist_cumulative/time_days[endtraj_idx,:]
print('Mean trajectory speed - (km/d)')
print(np.round(np.nanmean(traj_speed_kmd),3))

print('Median trajectory speed - (km/d)')
print(np.round(np.nanmedian(traj_speed_kmd),3))

print('Maximum trajectory speed - (km/d)')
print(np.round(np.nanmax(traj_speed_kmd),3))



