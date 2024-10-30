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
def elev_spatial(ax):
    path = '/home/mhuang/data/trendy/v11'
    fname = 'GMTED2010_15n240_1000deg.nc'
    elev = xr.open_dataset(os.path.join(path, fname))
    contour = ax.contour(elev.longitude, elev.latitude, elev.elevation
                         , levels=10, colors='black', linewidths=0.5)
def trendy_spatial(fig, ax, value, obj, period):
    start = period['start']
    end = period['end']
    if ano:
        range = 1
        label = 'anomaly'
    else:
        range = 3
        label = 'mean'
    map = ax.pcolormesh(value.lon, value.lat, value
                        , vmin=-range, vmax=range, cmap=plt.cm.seismic
                        )
    cbar1 = fig.colorbar(map, ax=ax, extend='both', orientation='horizontal')
    cbar1.set_label('CO$_2$ flux (gC/m$^2$/day)')
    cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    ax.set_xlim(data.fire['fire'].region['lon_min'] - 3, data.fire['fire'].region['lon_max'] + 3)
    ax.set_ylim(data.fire['fire'].region['lat_min'] - 3, data.fire['fire'].region['lat_max'] + 3)
    if topo:
        elev_spatial(ax)
    ax.coastlines()
    ax.set_title(f'{obj.upper()} CO2 flux {label} from {start} to {end}')
    gl = ax.gridlines(draw_labels=True, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    return ax
print(__name__)
if __name__.split('.')[-1] == 'latlon_trendy_nbp':
    from settings import spatial_period
    from settings import invs_anomaly_mod as ano
    from settings import topography_mod as topo
    from settings import trendy_season_mod as season_mod
    from settings import trendy_models as models
    season = dfn_season(define_season['start_month'], define_season['number_of_months'])

    p_mean  = - get_mean(data.trendy['nbp'].spatial, spatial_period) * 86400 * 1000
    s_mean  = - get_season_mean(data.trendy['nbp'].spatial, spatial_period, season) * 86400 * 1000
    if season_mod:
        for model in models:
            fig = plt.figure(figsize=[6, 3])
            ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
            trendy_spatial(fig, ax1, s_mean[model], model + str(season), spatial_period)
            if len(models) >= 9:
                savepath = '/home/mhuang/output/NBP_map/'
                plt.savefig(os.path.join(savepath, model + str(season) + '.png'))
            else:
                plt.show()
    else:
        for model in models:
            fig = plt.figure(figsize=[6, 3])
            ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
            trendy_spatial(fig, ax1, p_mean[model], model, spatial_period)
            if len(models) >= 9:
                savepath = '/home/mhuang/output/NBP_map/'
                plt.savefig(os.path.join(savepath, model + str(season) + '.png'))
            else:
                plt.show()




