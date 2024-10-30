import name_dic
import os
import numpy as np
import xarray as xr
from data_processor import (
    process_trendy_nbp,
    process_trendy_ra,
    process_trendy_rh,
    process_trendy_gpp,
    process_trendy_fLuc,
    process_trendy_fFire,
    process_trendy_lai,
    ProcessTM5GOSAT,
    ProcessTRENDY,
    ProcessTM5IS,
    ProcessFire,
    ProcessFluxcom,
    ProcessFluxcomX,
    ProcessTM5Prior,
    ProcessLai,
    ProcessSIF,
    ProcessERA5,
    ProcessOCO,
    ProcessOCO2MIP,
    ProcessSIFbaseGPP,
    ProcessNIRvGPP,
    ProcessAll
)
import read_pkl
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
from matplotlib.colors import ListedColormap
from statistical_analysis import change_order
from statistical_analysis import dfn_season
from statistical_analysis import get_season_mean
from settings import define_season
from settings import order
from read_pkl import data
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
from statistical_analysis import get_mean
from latlon_plot import LatlonPlot
from statistical_analysis import pearson_map
print(__name__)
if __name__.split('.')[-1] == 'pearson_gpp_meteo':
    region = data.era5.region['name']
    nirv  = data.est['nirvgpp'].spatial.sel(time=slice('2009-01-01', '2017-12-31')) * 0.001
    sif   = data.est['sifgpp'].spatial.sel(time=slice('2009-01-01', '2017-12-31')) * (0.01 / 30)
    rain  = data.era5.spatial['tp'].sel(time=slice('2009-01-01', '2017-12-31')) * 1000
    temp  = data.era5.spatial['t2m'].sel(time=slice('2009-01-01', '2017-12-31')) - 273.15

    fig, p_nirv = LatlonPlot().create_map(region)
    map, p_nirv = pearson_map(p_nirv, sif['GOSIF'], rain)
    LatlonPlot().corelation_cbar(fig, p_nirv, map)
    LatlonPlot().elev_spatial(p_nirv)
    p_nirv.set_title('Pearson correlation between GOSIF GPP and TP')
    plt.show()

    fig, t_nirv = LatlonPlot().create_map(region)
    map, t_nirv = pearson_map(t_nirv, sif['GOSIF'], temp)
    LatlonPlot().corelation_cbar(fig, t_nirv, map)
    LatlonPlot().elev_spatial(t_nirv)
    t_nirv.set_title('Pearson correlation between GOSIF GPP and T2m')
    plt.show()

    fig, p_nirv = LatlonPlot().create_map(region)
    map, p_nirv = pearson_map(p_nirv, nirv['GPP'], rain)
    LatlonPlot().corelation_cbar(fig, p_nirv, map)
    LatlonPlot().elev_spatial(p_nirv)
    p_nirv.set_title('Pearson correlation between NIRv GPP and TP')
    plt.show()

    fig, t_nirv = LatlonPlot().create_map(region)
    map, t_nirv = pearson_map(t_nirv, nirv['GPP'], temp)
    LatlonPlot().corelation_cbar(fig, t_nirv, map)
    LatlonPlot().elev_spatial(t_nirv)
    t_nirv.set_title('Pearson correlation between NIRv GPP and T2m')
    plt.show()