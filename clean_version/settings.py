from name_dic import trendy_names_v11 as all_models
import input
setting = input.Africa_05N15N
setting_region2 = None#input.Northern_africa_itcz_east
setting_region3 = None
# Path of the .pkl files
path           = "/home/mhuang/mycode/pkl"
# Define x-axis oder （month order） in the season cycle plots
order          = [6,7,8,9,10,11,12,1,2,3,4,5]
# the period-mean field you want to show in "latlon_*.py"
spatial_period = {
    'start':'2009-04-01', #'2015-10-01' 2017-05-01
    'end':'2018-12-31'     #'2016-03-01' 2018-04-30
}
# define the season for seasonal spatial study
define_season  = {
    'start_month':6,
    'number_of_months':6
}
# write the TRENDY models you want to check in the lon-lat plots
trendy_models  = ['LPJ','LPX-Bern']#['LPJ','LPX-Bern','CABLE-POP','DLEM']#['JULES','JSBACH','LPJ','LPX-Bern','OCN','ORCHIDEE','SDGVM','CABLE-POP','DLEM','ISBA-CTRIP']#['DLEM','LPJ','CABLE-POP']
# if turn on the anomaly_mod, the lat-lon plots will be shown as variable's anomaly plot
# if turn off, the lat-lon plots will be shown as variable's value plot
invs_anomaly_mod                  = None
meteo_anomaly_mod                 = None
gpp_anomaly_mod                   = True
# if turn on the topography_mod, the lat-lon plots will show contour of elevation
# if turn off, the lat-lon plots will be shown as variable's value plot
topography_mod                    = True
# if turn on the trendy_season_mod, the lat-lon plots will show your defined season mean
# if turn off, the lat-lon plots will be shown your defined period mean
trendy_season_mod                 = True

temperature_spatial_value_range   = [0,35]
precipitation_spatial_value_range = [0,10]
wind_field_arrow_density          = 4
wind_field_arrow_length           = 80
# settings for seasonal variability
era5_var                          = 'tp'
gosat_var                         = 'mean'
trendy_var                        = 'ter'
gpp_var                           = 'sifgpp'

# settings for EOF
sst_product                       = 'COBE'  # 'HadI' or 'COBE'
number_of_EOFs                    = 2
reconstruct_EOFs                  = [0,1,2,3]
Pacific_range                     = [-25,25,115,285]#,120,285 [-60,60,115,285]
IndiaOc_range                     = [30,-30,30,120]
Atlantc_range                     = []
sst_clim                          = '/home/mhuang/data/nontrendy/sst.mon.ltm.nc'

# - Do you want to show plots of study region?
# - None (No, I don't)    /     - True (Yes, I want)
check_study_region = None

# - Do you want to show plots of study region in a global view?
# - None (No, I don't)    /     - True (Yes, I want)
check_study_region_glb = None

# - Do you want to show plots of CO2 concentration?
# - None (No, I don't)    /     - True (Yes, I want)
check_concentration = None

# - Do you want to show plots of inversed net CO2 flux?
# - None (No, I don't)    /     - True (Yes, I want)
# - 'Running mean' (if you want to show running mean)
check_invs = None

# - Do you want to show difference of 2 regions' inversed net CO2 flux?
# - None (No, I don't)    /     - True (Yes, I want)
# - 'Running mean' (if you want to show running mean)
check_invs_2region_diff = None

# - Do you want to show IAV?
# - None (No, I don't)    /     - True (Yes, I want)
check_IAV = None

# - Do you want to show IAV of nbps without monthly fluxes?
# - None (No, I don't)    /     - True (Yes, I want)
check_IAV_nbps = None

# - Do you want to show plots of hovmollers?
# - None (No, I don't)    /     - True (Yes, I want)
check_hovmollers = 'True'

# - Do you want to show spatial plots of obervations?
# - None (No, I don't)    /     - True (Yes, I want)
check_obs_spatial = None

# - Do you want to show plots of TM5-4DVAR's prior, in-situ invers, +GOSAT invers?
# - None (No, I don't)    /     - True (Yes, I want)
check_prior = None

# - Do you want to show plots of RemoTeC & ACOS?
# - None (No, I don't)    /     - True (Yes, I want)
check_gosat = None

# - Do you want to show plots of TM5-4DVAR CAMS & CT2022?
# - None (No, I don't)    /     - True (Yes, I want)
check_insitu = None

# - Do you want to show plots of each TRENDY model comparing with in-situ invers and +GOSAT?
# - None (No, I don't)    /     - True (Yes, I want)
check_individual_trendy = None

# - Do you want to check whether the TRENDY NBP = GPP-Ra-Rh-fFire-fLuc?
# - None (No, I don't)    /     - True (Yes, I want)
check_individual_nbp = None

# - Do you want to show plots of fire emissions comparing with difference betweenin-situ invers and +GOSAT?
# - None (No, I don't)    /     - True (Yes, I want)
check_fires_role = None

# - Do you want to show plots of GOSAT, TRENDY NBP?
# - None (No, I don't)    /     - True (Yes, I want)
check_nbp = None

# - Do you want to show plots of GOSAT-fire, NEE, TER and GPP?
# - None (No, I don't)    /     - True (Yes, I want)
check_nee = None

# - Do you want to show plots of meteorology time series?
# - None (No, I don't)    /     - True (Yes, I want)
check_meteo = None

# - Do you want to show plots of GPP and GOSIF GPP?
# - None (No, I don't)    /     - True (Yes, I want)
check_gpp_with_gosif_gpp = None

# - Do you want to show plots of GPP and NIRv GPP?
# - None (No, I don't)    /     - True (Yes, I want)
check_gpp_with_nirv_gpp = None

# - Do you want to show spatial distribution of in-situ and +GOSAT inversions?
# - None (No, I don't)    /     - True (Yes, I want)
check_invs_spatial = None

# - Do you want to show spatial distribution of +GOSAT/RemoTeC & ACOS inversions?
# - None (No, I don't)    /     - True (Yes, I want)
check_invs_gosat_spatial = None

# - Do you want to show spatial distribution of seasonnal variability of +GOSAT/RemoTeC & ACOS inversions?
# - None (No, I don't)    /     - True (Yes, I want)
check_SV_invs_gosat_spatial = None

# - Do you want to show spatial distribution of TM5-4DVAR & CAMS & CT2022 inversions?
# - None (No, I don't)    /     - True (Yes, I want)
check_invs_insitu_spatial = None

# - Do you want to show spatial distribution of all inversions substract fire?
# - None (No, I don't)    /     - True (Yes, I want)
check_invs_fire_spatial = None

# Do you want to show the spatial pattern of meteorology variables?
# - None (No, I don't)    /     - True (Yes, I want)
check_meteo_spatial = None

# Do you want to show the spatial pattern of meteorology seasonal variability?
# - None (No, I don't)    /     - True (Yes, I want)
check_SV_meteo_spatial = None

# Do you want to show the spatial pattern of elevation?
# - None (No, I don't)    /     - True (Yes, I want)
check_elevation_spatial = None

# - Do you want to show spatial distribution of fire emission?
# - None (No, I don't)    /     - True (Yes, I want)
check_fire_spatial = None

# - Do you want to show spatial distribution of gpps?
# - None (No, I don't)    /     - True (Yes, I want)
check_gpp_spatial = None

# - Do you want to show spatial distribution of gpps seasonal variabilitiy?
# - None (No, I don't)    /     - True (Yes, I want)
check_SV_gpp_spatial = None

# - Do you want to show spatial distribution of reconstructed gpps?
# - None (No, I don't)    /     - True (Yes, I want)
check_ter_spatial = None

# - Do you want to show spatial distribution of SOC?
# - None (No, I don't)    /     - True (Yes, I want)
check_soc_spatial = None

# - Do you want to show spatial distribution of TRENDY NBP?
# - None (No, I don't)    /     - True (Yes, I want)
check_trendy_nbp_spatial = None

# - Do you want to show spatial distribution of TRENDY GPP?
# - None (No, I don't)    /     - True (Yes, I want)
check_trendy_gpp_spatial = None

# - Do you want to show seasonal variability of spatial distribution of TRENDY?
# - None (No, I don't)    /     - True (Yes, I want)
check_SV_trendy_spatial = None

# - Do you want to show spatial distribution of pearson correlation of GPP and meteo?
# - None (No, I don't)    /     - True (Yes, I want)
check_pearson_gpp_meteo = None

# - Do you want to show spatial distribution of pearson correlation of reconstructed TER and meteo?
# - None (No, I don't)    /     - True (Yes, I want)
check_pearson_ter_meteo = None

# - Do you want to show scatter plot of MAP and MAT, with 3rd dim NBP?
# - None (No, I don't)    /     - True (Yes, I want)
scatter_MAP_MAT_NBP   = None

# - Do you want to show scatter plot of MAP and MAT, with 3rd dim GPP?
# - None (No, I don't)    /     - True (Yes, I want)
scatter_MAP_MAT_GPP   = None

# - Do you want to plot NBP with PCs?
# - None (No, I don't)
# - 'PCF' (with Pacific SSTa PCs)    /     - 'IDA' (with India ocean SSTa PCs)
nbp_with_PCFpcs   = None