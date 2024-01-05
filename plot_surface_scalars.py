import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmocean
import cartopy.feature as cfeature
import numpy as np
import matplotlib
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

# set default font size
matplotlib.rcParams.update({"font.size": 8})

def add_cbar(ax, p):
    """
    Add horizontal colour bar beneath axis.
    """

    pos = ax.get_position()
    cbar_ax = fig.add_axes([pos.x0, 0.12, 
                            pos.x1 - pos.x0, 0.02])
    cbar = fig.colorbar(p, cax=cbar_ax, orientation='horizontal')
    cbar.ax.text(0.5, -2.8, r"Temperature ($^{\circ}$C)", fontsize=8,
                 rotation=0, transform=cbar.ax.transAxes,
                 va='top', ha='center')


def plot_surface_scalars():

    # set paths
    path = "/gws/nopw/j04/jmmp/tmp_slwa/AMM7_SSB_sample/"
    fn = "amm7_1d_20000101_20000131_grid_T.nc"

    # get data and select time
    ds = xr.open_dataset(path + fn, chunks=-1)
    ds_t0 = ds.sel(time_counter="2000-01-01").isel(deptht=0).squeeze()
    
    # set axes
    proj_dict = {"projection": ccrs.PlateCarree()}
    fig, axs = plt.subplots(2, figsize=(6.5,4.0), subplot_kw=proj_dict)
    plt.subplots_adjust(left=0.10, right=0.90, top=0.95, bottom=0.22)
    
    # set colour bar limits
    tmin=8
    tmax=16
    smin=34
    smax=35

    # render temperature
    pt = axs.pcolor(ds_t0.nav_lon, ds_t0.nav_lat, ds_t0.votemper, 
                    vmin=tmin, vmax=tmax, transform=plt_proj, 
                    cmap=cmocean.cm.thermal, shading="nearest")

    # render salinity
    ps = axs.pcolor(ds_t0.nav_lon, ds_t0.nav_lat, ds_t0.vosaline, 
                    vmin=smin, vmax=smax, transform=plt_proj, 
                    cmap=cmocean.cm.thermal, shading="nearest")

    # format axes
    for ax in axs:
        ax.set_ylim(44,temp0.nav_lat.max().values)
        
        ax.add_feature(cfeature.LAND, zorder=100, edgecolor='k')
        ax.set_xticks([-25, -20, -15, -10, -5, 0, 5, 10],
                      crs=ccrs.PlateCarree())
        ax.set_yticks([45, 50, 55, 60], crs=ccrs.PlateCarree())
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)
    
    # set color bars 
    add_cbar(axs[0], pt)
    add_cbar(axs[0], ps)

    ## add date title
    #date_str = "Date: " + temp0.time_counter.dt.strftime("%Y-%m-%d").values
    #print (date_str)
    #ax[0].text(0.5,0.97, date_str, transform=fig.transFigure, ha="center",va="top")

    # add axes labels
    for ax in axs:
        ax.set_xlabel("Longitude")
    axs[0].set_ylabel("Latitude")
    
    plt.savefig("AMM7_SSB_surface_scalars.png", dpi=600)

plot_surface_scalars()
