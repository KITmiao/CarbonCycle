import pandas as pd
import xarray as xr
import name_dic
import numpy as np
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
from matplotlib.colors import LogNorm
from name_dic import months
from statistical_analysis import change_order
from statistical_analysis import dfn_season
from settings import order
from read_pkl import data
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
from plots.plots_design import DefineCmaps, RegionBox
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
def color_for_obs():
    colors = plt.cm.viridis(np.linspace(0, 1, 256))
    colors[0] = np.array([1, 1, 1, 1])
    custom_cmap = ListedColormap(colors)
    return custom_cmap
def count_gosat_obs(lat_range,lon_range,remotec,acos,ls_type):
    lat_range[0] = lat_range[0] - 1
    lat_range[1] = lat_range[1] + 1
    lon_range[0] = lon_range[0] - 1
    lon_range[1] = lon_range[1] + 1
    lats_bnd = np.arange(lat_range[0], lat_range[1], 2.0)
    lats     = np.arange(lat_range[0] + 1, lat_range[1] + 1, 2.0)
    lons_bnd = np.arange(lon_range[0], lon_range[1], 3.0)
    lons     = np.arange(lon_range[0] + 1.5, lon_range[1] + 1.5, 3.0)
    years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    num_remotec = np.zeros([len(lats), len(lons), 12])
    num_acos    = np.zeros([len(lats), len(lons), 12])
    k = 0
    for mn in months:
        if k != 12:
            # print(yr, mn, j)
            ds = remotec[
                (remotec['Month'] == mn)
            ]
            # print(yr,mn,ds['lat'])
            i = 0
            for lat_bnd in lats_bnd:
                lat_min = lat_bnd
                lat_max = lat_bnd + 2
                j = 0
                for lon_bnd in lons_bnd:
                    lon_min = lon_bnd
                    lon_max = lon_bnd + 3
                    if ls_type == 'all':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            & (ds.lon > lon_min)
                            & (ds.lon <= lon_max)
                            ]
                    if ls_type == 'water':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            & (ds.lon > lon_min)
                            & (ds.lon <= lon_max)
                            & (ds['land_flag'] == 1)
                            ]
                    if ls_type == 'land':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            & (ds.lon > lon_min)
                            & (ds.lon <= lon_max)
                            & (ds['land_flag'] == 0)
                            ]
                    num_remotec[i, j, k] = len(ds2['CO2'])
                    j += 1
                i += 1
        k += 1


    k = 0
    for mn in months:
        if k != 12:
            #print(yr, mn, j)
            ds = acos[
                (acos['Month'] == mn)
            ]
            # print(yr,mn,ds['lat'])
            i = 0
            for lat_bnd in lats_bnd:
                lat_min = lat_bnd
                lat_max = lat_bnd + 2
                j = 0
                for lon_bnd in lons_bnd:
                    lon_min = lon_bnd
                    lon_max = lon_bnd + 3
                    if ls_type == 'all':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            & (ds.lon > lon_min)
                            & (ds.lon <= lon_max)
                            ]
                    if ls_type == 'water':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            & (ds.lon > lon_min)
                            & (ds.lon <= lon_max)
                            & (ds.land_frac <= 5)
                            ]
                    if ls_type == 'land':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            & (ds.lon > lon_min)
                            & (ds.lon <= lon_max)
                            & (ds.land_frac >= 1)
                            & (ds['quality'] == 0)
                            ]
                    num_acos[i, j, k] = len(ds2['CO2'])
                    j += 1
                i += 1
        k += 1
                #print(yr, mn, j)


    return num_remotec, num_acos, lats, lons, lats_bnd, lons_bnd
def obs_plot(lons, lats, data, title):
    fig = plt.figure(figsize=[6, 3])
    ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    print(f"Data min: {data.min()}, Data max: {data.max()}")
    map = ax1.pcolormesh(lons, lats, data, cmap=color_for_obs(),norm=LogNorm(vmin=1, vmax=1000))
    for lat in lats_bnd:
        ax1.axhline(lat, color='grey', linewidth=0.5)
    for lon in lons_bnd:
        ax1.axvline(lon, color='grey', linewidth=0.5)
    ax1.coastlines(color='crimson', linewidth=2)
    ax1.set_title(title)
    cbar1 = fig.colorbar(map, ax=ax1, extend='both', orientation='horizontal')
    cbar1.set_label('Number of measurements')
    cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    gl = ax1.gridlines(draw_labels=True, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    if setting_region2:
        from read_pkl import data2
        region2 = data2.trendy['nbp'].region['name']
        RegionBox(region2).rectangle(ax1)
    plt.show()
if __name__.split('.')[-1] == 'latlon_gosat_points':
    from settings import define_season, setting_region2
    seasons = dfn_season(define_season['start_month'], define_season['number_of_months'])
    mn1     = months[seasons[0]-1]
    mn2     = months[seasons[-1]-1]
    print(__name__)
    lat_range = [data.gosat['nbp'].region['lat_min'], data.gosat['nbp'].region['lat_max']]
    lon_range = [data.gosat['nbp'].region['lon_min'], data.gosat['nbp'].region['lon_max']]
    remotec   = data.concentration['REMOTEC']
    acos      = data.concentration['ACOS']
    remo_no, acos_no, lats, lons,lats_bnd,lons_bnd = count_gosat_obs(lat_range, lon_range, remotec, acos, 'land')
    remo = np.zeros_like(remo_no[:, :, 0])
    acos = np.zeros_like(acos_no[:, :, 0])
    for s in seasons:
        remo = remo + remo_no[:,:,s-1]
        acos = acos + acos_no[:,:,s-1]
    obs_plot(lons, lats, remo, 'GOSAT/RemoTeC '+mn1+'— '+mn2)
    obs_plot(lons, lats, acos, 'GOSAT/ACOS '+mn1+'— '+mn2)