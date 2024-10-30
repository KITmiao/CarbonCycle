import name_dic
import os
import numpy as np
import xarray as xr
import pandas as pd
import input
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
import settings
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
from plots.plots_design import DefineCmaps, RegionBox
from settings import setting

if __name__.split('.')[-1] == 'latlon_studyregion_glbview':
    #region1 = data.trendy['nbp'].region['name']
    #region2 = data2.trendy['nbp'].region['name']
    fig = plt.figure(figsize=[10, 6])
    ax  = fig.add_subplot(111, projection=ccrs.PlateCarree())

    ax  = LatlonPlot().glb_map(ax)
    modis_land = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
    cmap, norm, colors, txt = DefineCmaps().landcover()
    map = ax.pcolormesh(
        modis_land.lon, modis_land.lat, modis_land.eco_type
        , cmap=cmap, transform=ccrs.PlateCarree(),norm=norm
    )
    cbar = fig.colorbar(map)
    cbar.set_ticks(np.arange(len(colors)))
    cbar.set_ticklabels(txt)

    """
    from settings import spatial_period
    season = dfn_season(define_season['start_month'], define_season['number_of_months'])
    gosat = data3.gosat['nbp'].spatial
    gosat_name = data3.gosat['nbp'].name
    gosat_all = get_mean(gosat, spatial_period)
    gosat_sea = get_season_mean(gosat, spatial_period, season)
    gosat_avg = (gosat_all[gosat_name[0]] + gosat_all[gosat_name[1]]) / 2
    gosat_mean = (gosat[gosat_name[0]] + gosat[gosat_name[1]]) / 2
    gosat_sea_avg = get_season_mean(gosat_mean, spatial_period, season)
    all_periods = {
        'start': '2009-01-01',
        'end': '2018-12-31'
    }
    clim_sea = get_season_mean(gosat, all_periods, season)
    clim_all = get_mean(gosat, all_periods)
    gosat_all = gosat_all - clim_all
    gosat_sea = gosat_sea - clim_sea
    gosat_avg = (gosat_all[gosat_name[0]] + gosat_all[gosat_name[1]]) / 2
    gosat_mean = (gosat[gosat_name[0]] + gosat[gosat_name[1]]) / 2
    gosat_sea_avg = get_season_mean(gosat_mean, spatial_period, season)
    gosat_sea_avg = gosat_sea_avg - (clim_sea[gosat_name[0]] + clim_sea[gosat_name[1]]) / 2

    ax.pcolormesh(gosat_avg.lon, gosat_avg.lat, gosat_avg, vmin=-1, vmax=1, cmap=plt.cm.seismic)
    ax.set_xlim(data3.fire['fire'].region['lon_min'] - 3, data3.fire['fire'].region['lon_max'] + 3)
    ax.set_ylim(data3.fire['fire'].region['lat_min'] - 3, data3.fire['fire'].region['lat_max'] + 3)
    """
    if data:
        region1 = data.trendy['nbp'].region['name']
        RegionBox(region1).rectangle(ax)
    if settings.setting_region2:
        from read_pkl import data2
        region2 = data2.trendy['nbp'].region['name']
        RegionBox(region2).rectangle(ax)
    #RegionBox(region5).rectangle(ax)
    #RegionBox(region6).rectangle(ax)
    RegionBox(region1).obspack(ax, setting['OBSPACK'])
    ax.coastlines()
    plt.tight_layout()
    plt.show()
