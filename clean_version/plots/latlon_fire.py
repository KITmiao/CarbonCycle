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
from matplotlib.colors import ListedColormap
from statistical_analysis import get_mean
from statistical_analysis import change_order
from statistical_analysis import dfn_season
from statistical_analysis import get_season_mean
from settings import order
from settings import spatial_period
from settings import define_season
from read_pkl import data
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
def color_for_fire():
    colors = plt.cm.afmhot_r(np.linspace(0, 1, 256))
    colors[0] = np.array([1, 1, 1, 1])
    custom_cmap = ListedColormap(colors)
    return custom_cmap
def fire_mean_spatial(fig, ax, value, obj, period):
    custom_cmap = color_for_fire()
    start       = period['start']
    end         = period['end']
    #feild  = get_mean(value, period)
    #feild  = value.sel(time=slice(start, end)).mean(dim=['time'], skipna=True)
    map = ax.pcolormesh(value.lon, value.lat, value, cmap=custom_cmap, vmin=0, vmax=2.5)
    cbar1 = fig.colorbar(map, ax=ax, extend='both', orientation='horizontal')
    cbar1.set_label('CO$_2$ flux (gC/m$^2$/day)')
    cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    ax.set_xlim(data.fire['fire'].region['lon_min'] - 3, data.fire['fire'].region['lon_max'] + 3)
    ax.set_ylim(data.fire['fire'].region['lat_min'] - 3, data.fire['fire'].region['lat_max'] + 3)
    ax.set_title(f'{obj.upper()} mean fire emission from {start} to {end}')
    gl = ax.gridlines(draw_labels=True, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    return ax
print(__name__)
if __name__.split('.')[-1] == 'latlon_fire':
    season = dfn_season(define_season['start_month'], define_season['number_of_months'])
    fires = ['gfed', 'gfas', 'finn']
    for name in fires:
        fig   = plt.figure(figsize=[6, 3])
        ax1   = fig.add_subplot(111, projection=ccrs.PlateCarree())
        field = get_mean(data.fire['fire'].spatial[name], spatial_period)
        ax1 = fire_mean_spatial(fig, ax1, field, name, spatial_period)
        ax1.coastlines()

        fig = plt.figure(figsize=[6, 3])
        ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
        field = get_season_mean(data.fire['fire'].spatial[name], spatial_period, season)
        ax1 = fire_mean_spatial(fig, ax1, field, name+str(season), spatial_period)
        ax1.coastlines()

    mean_fire = get_mean(data.fire['fire'].spatial, spatial_period)
    avg_fire  = (mean_fire['gfed']+mean_fire['gfas']+mean_fire['finn'])/3
    fig = plt.figure(figsize=[6, 3])
    ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax1 = fire_mean_spatial(fig, ax1, avg_fire, 'averaged', spatial_period)
    ax1.coastlines()
    plt.show()



