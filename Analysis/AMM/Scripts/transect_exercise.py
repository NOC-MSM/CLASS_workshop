import sys
sys.path.append("/home/users/ryapat30/NOC/COAsT")

import coast
import matplotlib.pyplot as plt

def plot_transect_examples():
    """
    Master function for calcualting temperature, velocities and transport along
    a transec
    """

    # set model paths
    path = "/gws/nopw/j04/jmmp/tmp_slwa/AMM7_SSB_sample/"
    model_path_t = path +  "amm7_1d_20040101_20040131_grid_T.nc"
    model_path_u = path +  "amm7_1d_20040101_20040131_grid_U.nc"
    model_path_v = path +  "amm7_1d_20040101_20040131_grid_V.nc"
    jmmp_path = "/gws/nopw/j04/jmmp/"
    domcfg_path = path + "amm7_SSB_mesh_mask.nc"
    
    # set coast config paths
    cfg_path = "/home/users/ryapat30/NOC/COAsT/config/"
    nemo_t_json = cfg_path + "example_nemo_grid_t.json"
    nemo_u_json = cfg_path + "example_nemo_grid_u.json"
    nemo_v_json = cfg_path + "example_nemo_grid_v.json"
    nemo_f_json = cfg_path + "example_nemo_grid_v.json"

    # get nemo output
    nemo_t = coast.Gridded(model_path_t, domcfg_path, config=nemo_t_json)
    nemo_u = coast.Gridded(model_path_u, domcfg_path, config=nemo_u_json)
    nemo_v = coast.Gridded(model_path_v, domcfg_path, config=nemo_v_json)
    nemo_f = coast.Gridded(fn_domain=domcfg_path, config=nemo_f_json)

    # get transects
    tran_t = coast.TransectT(nemo_t, (54, -15), (56, -12))
    tran_f = coast.TransectF(nemo_f, (54, -15), (56, -12))

    # add normal velociites to transect
    tran_f.calc_flow_across_transect(nemo_u, nemo_v)

    # plotting
    plot_transect_temperature(tran_t)
    plot_cross_transect_velocities(tran_f)
    plot_cross_transect_transport(tran_f)

def plot_transect_temperature(tran_t):
    """
    Plot time-mean temperature along extracted transect
    """

    # time mean temperature
    temp_mean = tran_t.data.temperature.mean(dim="t_dim")

    # plot time-mean temperature along transect
    plt.figure()
    temp_mean.plot.pcolormesh(y="depth_0", yincrease=False)
    plt.savefig("AMM7_transect_time_mean_temperature_example.png")

def plot_cross_transect_velocities(tran_f):
    """
    Plot time-mean velocities across extracted transect
    """

    # To do this we can plot the ‘normal_velocities’ variable.
    cross_vel_mean = tran_f.data_cross_tran_flow.normal_velocities.mean(
                                                                    dim="t_dim")

    # plot time-mean cross transect velocities
    plt.figure()
    cross_vel_mean.plot.pcolormesh(yincrease=False, y="depth_0",
                                   cbar_kwargs={"label": "m/s"})
    plt.savefig("AMM7_transect_time_mean_velocities_example.png")
    
def plot_cross_transect_transport(tran_f):
    """
    Plot time-mean transport across extracted transect
    """

    # To do this we can plot the ‘normal_transports’ variable.
    cross_transport_mean = tran_f.data_cross_tran_flow.normal_transports.mean(
                                                                    dim="t_dim")
 
    # plot cross transect transport
    plt.figure()
    cross_transport_mean.plot()
    plt.ylabel("Sv")
    plt.savefig("AMM7_transect_time_mean_transport_example.png")

if __name__ == "__main__":

    plot_transect_examples()
