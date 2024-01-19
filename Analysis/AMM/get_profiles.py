import sys
sys.path.append("/home/users/ryapat30/NOC/COAsT")

import coast
import xarray as xr
import matplotlib.pyplot as plt

def plot_surface_differences():
    """ plot surface temperature differences between model and observations """ 

    # set model paths
    path = "/gws/nopw/j04/jmmp/tmp_slwa/AMM7_SSB_sample/"
    model_path = path +  "amm7_1d_20040101_20040131_grid_T.nc"
    jmmp_path = "/gws/nopw/j04/jmmp/"
    domcfg_path = jmmp_path + "public/AMM15/DOMAIN_CFG/GEG_SF12.nc"
    
    # set coast config paths
    cfg_path = "/home/users/ryapat30/NOC/COAsT/config/"
    en4_json = cfg_path + "example_en4_profiles.json"
    nemo_json = cfg_path + "example_nemo_grid_t.json"

    # set observation path
    en4_path="/gws/nopw/j04/class_vol2/senemo/shared/EN4/processed/AMM15/"
    fn_prof = en4_path + "AMM15_processed_200401.nc"

    # get nemo output
    nemo = coast.Gridded(model_path, domcfg_path, config=nemo_json)

    # mask land and rename depth
    nemo.dataset["landmask"] = nemo.dataset.bottom_level == 0
    nemo.dataset = nemo.dataset.rename({"depth_0": "depth"})

    # get en4 profiles
    en4_profiles = coast.Profile(config=en4_json)
    en4_profiles.dataset = xr.open_dataset(fn_prof, chunks={'id_dim':10000})

    # interpolate to commom grid
    en4_profiles, nemo_profiles = interp_model_to_obs(en4_profiles, nemo)
    en4_reg_dep, nemo_reg_depth = interp_to_regular_depth(obs_profiles,
                                                          nemo_profiles)

    # difference between nemo and obs
    surface_erros = get_surface_differences(en4_reg_depth, nemo_reg_depth)

    # Plot (obs. - model) upper 10m averaged temperatures
    surface_errors.plot_map(var_str="diff_temperature")
  
    # save
    plt.savefig("surface_temperature_errors.png")

def interp_model_to_obs(obs_profiles, model, too_far):
    """
    Interpolate model to horizontal positions of observations

    Nearest neighbour interpolation of Gridded model object to observations
    data that above a distance threshold from observations is discarded.
    """

    # nearest neighbour interplation to profile positions
    model_profiles = obs_profiles.obs_operator(model) 

    # drop data where interpolation distance is greater than "too_far"
    keep_indices = model_profiles.dataset.interp_dist <= too_far
    model_profiles = model_profiles.isel(id_dim=keep_indices)
    obs_profile = obs_profiles.isel(id_dim=keep_indices)

    return obs_profiles, model_profiles

def interp_to_regular_depth(obs_profiles, model_profiles):
    """
    Interpolate model and observations to common vertical grid
    """

    # initialise COAST object
    analysis = coast.ProfileAnalysis()

    # Set target depth levels
    ref_depth = np.concatenate((np.arange(1, 100, 10),
                                np.arange(100, 1000, 5)))
    
    # Interpolate model profiles onto observation depths
    model_profiles_obs_grid = analysis.interpolate_vertical(model_profiles,
                                                         obs_profiles,
                                                         interp_method="linear")
    
    # Interpolate model profiles to reference depths
    model_profiles_ref_grid = analysis.interpolate_vertical(
                                         model_profiles_obs_grid,
                                         ref_depth)

    # Interpolate obs. profiles to reference depths
    obs_profiles_ref_grid = analysis.interpolate_vertical(obs_rofiles,
                                                          ref_depth)

    return obs_profiles_ref_grid, model_profiles_ref_grid

def get_surface_differences(obs_profiles, model_profiles, lower_bound=10):
    """
    calculate difference between model and observations at the surface
    """

    # obs. and model average over top layer 
    model_profiles_surface = analysis.depth_means(model_profiles,
                                                  [0, lower_bound])
    obs_profiles_surface   = analysis.depth_means(obs_profiles,
                                                  [0, lower_bound])

    # get difference
    surface_errors = analysis.difference(obs_profiles_surface,
                                         model_profiles_surface)

    return surface_errors
    

plot_surface_differences()
