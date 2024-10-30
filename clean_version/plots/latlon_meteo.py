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
from statistical_analysis import dfn_season
from statistical_analysis import get_season_mean
from settings import define_season
from settings import order
from read_pkl import data
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
from plots.plots_design import DefineCmaps
import os
import xarray as xr
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
def meteo_spatial(fig, ax, value, obj, period, cmap, vmin, vmax):
    start = period['start']
    end = period['end']
    map = ax.pcolormesh(value.lon, value.lat, value, cmap=cmap, vmin=vmin, vmax=vmax)
    cbar1 = fig.colorbar(map, ax=ax, extend='both', orientation='horizontal')
    ax.set_xlim(data.fire['fire'].region['lon_min'] - 3, data.fire['fire'].region['lon_max'] + 3)
    ax.set_ylim(data.fire['fire'].region['lat_min'] - 3, data.fire['fire'].region['lat_max'] + 3)
    if topo:
        elev_spatial(ax)
    ax.set_title(f'mean {obj.upper()} from {start} to {end}')
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
if __name__.split('.')[-1] == 'latlon_meteo':
    from settings import spatial_period
    from settings import temperature_spatial_value_range as t_range
    from settings import precipitation_spatial_value_range as p_range
    from settings import wind_field_arrow_density as n
    from settings import wind_field_arrow_length as l
    from settings import meteo_anomaly_mod as ano
    from settings import topography_mod as topo

    season = dfn_season(define_season['start_month'], define_season['number_of_months'])
    tp = data.era5.spatial['tp']*1000
    t2m = data.era5.spatial['t2m'] - 273.15
    Blues = DefineCmaps().white_to_blue()
    Reds  = DefineCmaps().white_to_red()

    meteo_tp = get_mean(tp, spatial_period)
    meteo_t2m = get_mean(t2m, spatial_period)
    print(meteo_tp.sel(lat=10,lon=20))
    meteo     = get_mean(data.era5.spatial, spatial_period)
    plot1, cbar1 = plts(meteo_tp, 'tp', Blues, p_range)
    plot2, cbar2 = plts(meteo_t2m, 't2m', Reds, t_range)
    cbar1.set_label('precipitation (mm/day)')
    cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    cbar2.set_label('temperature (\u00B0C)')
    cbar2.ax.set_position([0.26, 0.2, 0.5, 0.04])
    c = plot1.quiver(meteo.lon[::n], meteo.lat[::n], meteo.u10[::n,::n], meteo.v10[::n,::n]
                 , transform=ccrs.PlateCarree(), scale=l, headwidth=7)
    plot1.quiverkey(c, 0.9, -0.23, 10, label='10 m/s', labelpos='E', coordinates='axes')
    plt.show()

    meteo_tp = get_season_mean(tp, spatial_period, season)
    meteo_t2m = get_season_mean(t2m, spatial_period, season)
    meteo = get_season_mean(data.era5.spatial, spatial_period, season)
    if ano:
        all_periods = {
            'start': '2009-01-01',
            'end': '2018-12-31'
        }
        clim      = get_season_mean(data.era5.spatial, all_periods, season)
        meteo_ano = meteo - clim
        plot1, cbar1 = plts(meteo_tp, 'tp' + str(season), plt.cm.RdBu, [-2,2])
        plot2, cbar2 = plts(meteo_t2m, 't2m' + str(season), plt.cm.bwr, [-2,2])
        cbar1.set_label('precipitation (mm/day)')
        cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
        cbar2.set_label('temperature (\u00B0C)')
        cbar2.ax.set_position([0.26, 0.2, 0.5, 0.04])
        c = plot1.quiver(meteo.lon[::n], meteo.lat[::n], meteo.u10[::n, ::n], meteo.v10[::n, ::n]
                         , transform=ccrs.PlateCarree(), scale=l, headwidth=7)
        plot1.quiverkey(c, 0.9, -0.23, 10, label='10 m/s', labelpos='E', coordinates='axes')
        plt.show()
    else:
        plot1, cbar1 = plts(meteo_tp, 'tp'+str(season), Blues, p_range)
        plot2, cbar2 = plts(meteo_t2m, 't2m'+str(season), Reds, t_range)
        cbar1.set_label('precipitation (mm/day)')
        cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
        cbar2.set_label('temperature (\u00B0C)')
        cbar2.ax.set_position([0.26, 0.2, 0.5, 0.04])
        c = plot1.quiver(meteo.lon[::n], meteo.lat[::n], meteo.u10[::n, ::n], meteo.v10[::n, ::n]
                         , transform=ccrs.PlateCarree(), scale=l, headwidth=7)
        plot1.quiverkey(c, 0.9, -0.23, 10, label='10 m/s', labelpos='E', coordinates='axes')
        plt.show()

