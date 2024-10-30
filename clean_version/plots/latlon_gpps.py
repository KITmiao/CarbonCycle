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
from statistical_analysis import get_season_mean
from statistical_analysis import dfn_season
from settings import order
from read_pkl import data
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
from plots.plots_design import DefineCmaps
from plots.plots_design import elev_spatial
from settings import spatial_period
from settings import define_season
def gpp_spatial(fig, ax, value, obj, period):
    start = period['start']
    end = period['end']
    if ano:
        vmin, vmax = -1, 1
        cmap       = 'BrBG'
        label      = 'anomaly'
    else:
        vmin, vmax = 0, 12
        cmap       = 'Greens'
        label      = 'mean'
    map = ax.pcolormesh(value.lon, value.lat, value, cmap=cmap, vmin=vmin, vmax=vmax)
    cbar1 = fig.colorbar(map, ax=ax, extend='both', orientation='horizontal')
    cbar1.set_label('GPP (gC/m2/day)')
    cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    ax.set_xlim(data.fire['fire'].region['lon_min'] - 3, data.fire['fire'].region['lon_max'] + 3)
    ax.set_ylim(data.fire['fire'].region['lat_min'] - 3, data.fire['fire'].region['lat_max'] + 3)
    ax.set_title(f'{obj.upper()} gpp {label} from {start} to {end}')
    if topo:
        elev_spatial(ax)
    gl = ax.gridlines(draw_labels=True, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    return ax
def plts(value, obj):
    fig = plt.figure(figsize=[6, 3])
    ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax1 = gpp_spatial(fig, ax1, value, obj, spatial_period)
    ax1.coastlines()

print(__name__)
if __name__.split('.')[-1] == 'latlon_gpps':
    from settings import topography_mod as topo
    from settings import gpp_anomaly_mod as ano
    season = dfn_season(define_season['start_month'], define_season['number_of_months'])

    nirv   = data.est['nirvgpp'].spatial
    nirv   = get_mean(nirv*0.001, spatial_period)
    sif    = data.est['sifgpp'].spatial
    sif    = get_mean(sif*(0.01/30), spatial_period)
    trendy = data.trendy['gpp'].spatial
    trendy = get_mean(trendy, spatial_period)
    if ano:
        all_periods = {
            'start': '2009-01-01',
            'end': '2018-12-31'
        }
        nirv        = data.est['nirvgpp'].spatial
        nirv_clim   = get_mean(nirv*0.001, all_periods)
        nirv        = get_mean(nirv * 0.001, spatial_period)
        sif         = data.est['sifgpp'].spatial
        sif_clim    = get_mean(sif*(0.01/30), all_periods)
        sif         = get_mean(sif * (0.01 / 30), spatial_period)
        trendy      = data.trendy['gpp'].spatial
        trendy_clim = get_mean(trendy, all_periods)
        trendy      = get_mean(trendy, spatial_period)
        nirv        = nirv - nirv_clim
        sif         = sif - sif_clim
        trendy      = trendy - trendy_clim

    plts(nirv['GPP'], 'NIRv')
    plts(sif['GOSIF'], 'SIF')
    plt.show()

    nirv = data.est['nirvgpp'].spatial
    nirv = get_season_mean(nirv * 0.001, spatial_period, season)
    sif = data.est['sifgpp'].spatial
    sif = get_season_mean(sif * (0.01 / 30), spatial_period, season)
    trendy = data.trendy['gpp'].spatial
    trendy = get_season_mean(trendy, spatial_period, season)
    if ano:
        all_periods = {
            'start': '2009-01-01',
            'end': '2018-12-31'
        }
        nirv        = data.est['nirvgpp'].spatial
        nirv_clim   = get_season_mean(nirv * 0.001, all_periods, season)
        nirv        = get_season_mean(nirv * 0.001, spatial_period, season)
        sif         = data.est['sifgpp'].spatial
        sif_clim    = get_season_mean(sif * (0.01 / 30), all_periods, season)
        sif         = get_season_mean(sif * (0.01 / 30), spatial_period, season)
        trendy      = data.trendy['gpp'].spatial
        trendy_clim = get_season_mean(trendy, all_periods, season)
        trendy      = get_season_mean(trendy, spatial_period, season)
        nirv        = nirv - nirv_clim
        sif         = sif - sif_clim
        trendy      = trendy - trendy_clim
    plts(nirv['GPP'], 'NIRv' + str(season))
    plts(sif['GOSIF'], 'SIF' + str(season))
    plt.show()

