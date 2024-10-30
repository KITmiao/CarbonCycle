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
from plots.plots_design import DefineCmaps
import statistical_analysis as sa
def elev_spatial(ax):
    path = '/home/mhuang/data/trendy/v11'
    fname = 'GMTED2010_15n240_1000deg.nc'
    elev = xr.open_dataset(os.path.join(path, fname))
    contour = ax.contour(elev.longitude, elev.latitude, elev.elevation
                         , levels=10, colors='black', linewidths=0.5)
def meteo_spatial(fig, ax, value, obj, period, cmap, vmin, vmax):
    start = period['start']
    end = period['end']
    map = ax.pcolormesh(value.lon, value.lat, value, cmap=cmap, vmin=vmin, vmax=vmax)
    cbar1 = fig.colorbar(map, ax=ax, extend='both', orientation='horizontal')
    ax.set_xlim(data.fire['fire'].region['lon_min'] - 3, data.fire['fire'].region['lon_max'] + 3)
    ax.set_ylim(data.fire['fire'].region['lat_min'] - 3, data.fire['fire'].region['lat_max'] + 3)
    if topo:
        elev_spatial(ax)
    ax.set_title(f'seasonal varibility {obj.upper()}')
    gl = ax.gridlines(draw_labels=True, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    return ax, cbar1
def plts(value, obj, cmap, range):
    vmin = range[0]
    vmax = range[1]
    fig  = plt.figure(figsize=[6, 3])
    ax1  = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax1,cbar = meteo_spatial(fig, ax1, value, obj, spatial_period, cmap, vmin=vmin, vmax=vmax)
    ax1.coastlines()
    return ax1, cbar
print(__name__)
if __name__.split('.')[-1] == 'latlon_SV_trendy':
    from settings import trendy_models
    from settings import trendy_var
    from settings import spatial_period
    from settings import topography_mod as topo
    Blues = DefineCmaps().white_to_blue()
    Reds = DefineCmaps().white_to_red()
    i = 0
    for models in trendy_models:
        if trendy_var == 'ter':
            x = data.trendy['ra'].spatial[models].sel(time=slice(spatial_period['start'], spatial_period['end']))
            + data.trendy['rh'].spatial[models].sel(time=slice(spatial_period['start'], spatial_period['end']))
        else:
            x = data.trendy[trendy_var].spatial[models].sel(time=slice(spatial_period['start'], spatial_period['end']))
        if i == 0:
            variable = x
            i = i + 1
        else:
            variable = variable + x
    variable = variable/len(trendy_models)
    std       = variable.groupby("time.year").std(dim='time')
    sv       = std.mean(dim='year')
    sv       = sa.zscore(sv)
    plot1, cbar1 = plts(sv, trendy_var, 'RdYlBu_r', [-3, 3])
    cbar1.set_label(f'{trendy_var} seasonal variability')
    cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    plt.show()