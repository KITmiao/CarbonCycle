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
from statistical_analysis import change_order
from settings import order
from read_pkl import data
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
from plots.plots_design import DefineCmaps
import xarray as xr
import os
def meteo_spatial(fig, ax, value, obj, cmap):
    map = ax.pcolormesh(value.longitude, value.latitude, value, cmap=cmap, vmin=1, vmax=2000)
    cbar1 = fig.colorbar(map, ax=ax, extend='both', orientation='horizontal')
    cbar1.set_label('elevation (m)')
    cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    ax.set_xlim(data.fire['fire'].region['lon_min'] - 3, data.fire['fire'].region['lon_max'] + 3)
    ax.set_ylim(data.fire['fire'].region['lat_min'] - 3, data.fire['fire'].region['lat_max'] + 3)
    ax.set_title(f'{obj.upper()}')
    gl = ax.gridlines(draw_labels=True, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    return ax, cbar1
def plts(value, obj, cmap):
    fig = plt.figure(figsize=[6, 3])
    ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax1,cbar = meteo_spatial(fig, ax1, value[obj], obj, cmap)
    ax1.coastlines()
    return cbar
print(__name__)
if __name__.split('.')[-1] == 'latlon_elevation':
    path      = '/home/mhuang/data/trendy/v11'
    fname     = 'GMTED2010_15n240_1000deg.nc'
    elevation = xr.open_dataset(os.path.join(path,fname))
    Reds      = DefineCmaps().white_to_red()
    plts(elevation, 'elevation', 'gist_earth_r')
    plt.show()
