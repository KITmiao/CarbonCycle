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
def get_mean(value, period):
    start = period['start']
    end = period['end']
    field = value.sel(time=slice(start, end)).mean(dim=['time'], skipna=True)
    return field
def elev_spatial(ax):
    path = '/home/mhuang/data/trendy/v11'
    fname = 'GMTED2010_15n240_1000deg.nc'
    elev = xr.open_dataset(os.path.join(path, fname))
    contour = ax.contour(elev.longitude, elev.latitude, elev.elevation
                         , levels=10, colors='black', linewidths=0.5)
    """for i, segs in enumerate(contour.allsegs):
        for segment in segs:
            if len(segment) > 0:  # 检查 segment 是否为空
                # 获取每条等高线的中点位置
                x = segment[len(segment) // 2][0]
                y = segment[len(segment) // 2][1]
                if xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1]:
                    ax.text(x, y, f'{contour.levels[i]:.2f}', color='black', fontsize=5, ha='center')"""
def invers_spatial(fig, ax, value, obj, period):
    start = period['start']
    end = period['end']
    if ano:
        range = 1
        label = 'anomaly'
    else:
        range = 3
        label = 'mean'
    map = ax.pcolormesh(value.lon, value.lat, value, vmin=-range, vmax=range, cmap=plt.cm.seismic)
    cbar1 = fig.colorbar(map, ax=ax, extend='both', orientation='horizontal')
    cbar1.set_label('CO$_2$ flux (gC/m$^2$/day)')
    cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    ax.set_xlim(data.fire['fire'].region['lon_min'] - 3, data.fire['fire'].region['lon_max'] + 3)
    ax.set_ylim(data.fire['fire'].region['lat_min'] - 3, data.fire['fire'].region['lat_max'] + 3)
    if topo:
        elev_spatial(ax)
    ax.set_title(f'{obj.upper()} CO2 flux {label} from {start} to {end}')
    gl = ax.gridlines(draw_labels=True, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    return ax
def plts(value, names, *txt):
    for name in names:
        if txt:
            note = str(name) + str(txt)
        else:
            note = name
        fig = plt.figure(figsize=[6, 3])
        ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
        ax1 = invers_spatial(fig, ax1, value[name], note, spatial_period)
        ax1.coastlines()
        plt.show()
print(__name__)
if __name__.split('.')[-1] == 'latlon_inversion_insitu':
    from settings import spatial_period
    from settings import invs_anomaly_mod as ano
    from settings import topography_mod as topo

    season = dfn_season(define_season['start_month'], define_season['number_of_months'])
    gosat          = data.gosat['nbp'].spatial
    gosat_name     = data.gosat['nbp'].name
    gosat_all      = get_mean(gosat, spatial_period)
    gosat_sea      = get_season_mean(gosat, spatial_period, season)
    gosat_avg      = (gosat_all[gosat_name[0]] + gosat_all[gosat_name[1]])/2
    gosat_mean     = (gosat[gosat_name[0]] + gosat[gosat_name[1]])/2
    gosat_sea_avg  = get_season_mean(gosat_mean, spatial_period, season)

    insitu         = data.insitu['nbp'].spatial
    insitu_name    = data.insitu['nbp'].name
    insitu_all     = get_mean(insitu, spatial_period)
    insitu_sea     = get_season_mean(insitu, spatial_period, season)
    insitu_avg     = (insitu_all[insitu_name[0]] + insitu_all[insitu_name[1]] + insitu_all[insitu_name[2]]) / 3
    insitu_mean    = (insitu[insitu_name[0]] + insitu[insitu_name[1]] + insitu[insitu_name[2]]) / 3
    insitu_sea_avg = get_season_mean(insitu_mean, spatial_period, season)
    if ano:
        all_periods = {
            'start': '2009-01-01',
            'end': '2018-12-31'
        }
        clim_sea       = get_season_mean(gosat, all_periods, season)
        clim_all       = get_mean(gosat, all_periods)
        gosat_all      = gosat_all - clim_all
        gosat_sea      = gosat_sea - clim_sea
        gosat_avg      = (gosat_all[gosat_name[0]] + gosat_all[gosat_name[1]]) / 2
        gosat_mean     = (gosat[gosat_name[0]] + gosat[gosat_name[1]]) / 2
        gosat_sea_avg  = get_season_mean(gosat_mean, spatial_period, season)
        gosat_sea_avg  = gosat_sea_avg - (clim_sea[gosat_name[0]] + clim_sea[gosat_name[1]]) / 2

        clim_sea = get_season_mean(insitu, all_periods, season)
        clim_all = get_mean(insitu, all_periods)
        insitu_all     = insitu_all - clim_all
        insitu_sea     = insitu_sea - clim_sea
        insitu_avg     = (insitu_all[insitu_name[0]] + insitu_all[insitu_name[1]] + insitu_all[insitu_name[2]]) / 3
        insitu_mean    = (insitu[insitu_name[0]] + insitu[insitu_name[1]] + insitu[insitu_name[2]]) / 3
        insitu_sea_avg = get_season_mean(insitu_mean, spatial_period, season)
        insitu_sea_avg  = insitu_sea_avg - (clim_sea[insitu_name[0]] + clim_sea[insitu_name[1]] + clim_sea[insitu_name[2]]) / 3

        plts(insitu_all, insitu_name)
        plts(insitu_sea, insitu_name, season)
    else:
        plts(insitu_all, insitu_name)
        plts(insitu_sea, insitu_name, season)