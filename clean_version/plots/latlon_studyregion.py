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
from plots.plots_design import DefineCmaps
from settings import setting
def rectangle(region, ax):
    rect = plt.Rectangle(
        (name_dic.transcom[region]['lon_min'], name_dic.transcom[region]['lat_min'])
        , name_dic.transcom[region]['lon_max'] - name_dic.transcom[region]['lon_min']
        , name_dic.transcom[region]['lat_max'] - name_dic.transcom[region]['lat_min']
        , edgecolor='k', linewidth=2, facecolor='none')
    ax.add_patch(rect)
def obspack(ax):
    obspack         = pd.read_csv(setting['OBSPACK'])
    obspack['Type'] = obspack['Type'].replace({
        'aircraft-flask': 'aircraft',
        'aircraft-insitu': 'aircraft',
        'aircraft-pfp': 'aircraft',
        'shipboard-flask': 'ship',
        'shipboard-insitu': 'ship',
        'surface-flask': 'surface',
        'surface-insitu': 'surface',
        'surface-pfp': 'surface',
        'tower-insitu': 'surface'
    })
    type = {
        'aircore': {'color': 'k', 'marker': 'o'},
        'aircraft': {'color': 'k', 'marker': '>'},
        'ship': {'color': 'purple', 'marker': 'o'},
        'surface': {'color': 'purple', 'marker': 'x'}
    }
    for key, value in obspack.groupby('Type'):
        value.plot.scatter(x='Longitude', y='Latitude', s=50, label=key, **type[key], ax=ax)
        ax.legend(loc='lower left')
print(__name__)
if __name__.split('.')[-1] == 'latlon_studyregion':
    region = data.trendy['nbp'].region['name']
    region = 'Northern Africa'
    fig = plt.figure(figsize=[10, 6])
    ax  = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax  = LatlonPlot().create_map2(region, ax)

    modis_land = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
    cmap, norm, colors, txt = DefineCmaps().landcover()
    map = ax.pcolormesh(
        modis_land.lon, modis_land.lat, modis_land.eco_type
        , cmap=cmap, transform=ccrs.PlateCarree(),norm=norm
    )
    cbar = fig.colorbar(map)
    cbar.set_ticks(np.arange(len(colors)))
    cbar.set_ticklabels(txt)
    rectangle('Northern Africa itcz', ax)
    obspack(ax)
    plt.tight_layout()
    plt.show()
