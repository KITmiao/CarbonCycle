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
from latlon_plot import LatlonPlot
from statistical_analysis import pearson_map
from statistical_analysis import get_anno
import pandas as pd
from plots.plots_design import ScatterPlots as sp
print(__name__)
if __name__.split('.')[-1] == 'scatter_meteo_gpp':
    from settings import spatial_period
    from settings import define_season
    from settings import gpp_anomaly_mod as ano
    all_periods = {
        'start': '2009-04-01',
        'end': '2018-12-31'
    }
    season = dfn_season(define_season['start_month'], define_season['number_of_months'])

    tp   = data.era5.spatial['tp'] * 1000 * 30
    t2m  = data.era5.spatial['t2m'] - 273.15  # unit to ℃
    gpp  = data.est['sifgpp'].spatial['GOSIF']*(0.01/30)

    prec  = []
    temp  = []
    gosa  = []
    for i in season:
        p    = get_season_mean(tp, spatial_period, [i]).values.flatten()
        t    = get_season_mean(t2m, spatial_period, [i]).values.flatten()
        co2  = get_season_mean(gpp, spatial_period, [i]).values.flatten()
        prec = np.append(prec, p)
        temp = np.append(temp, t)
        gosa = np.append(gosa, co2)
    """    
    tp   = get_season_mean(tp, spatial_period, season).values.flatten()
    t2m  = get_season_mean(t2m, spatial_period, season).values.flatten()
    nbp  = get_season_mean(nbp, spatial_period, season).values.flatten()"""
    vmin = 0
    vmax = 10
    df    = pd.DataFrame({'x':prec, 'y':temp, 'z':gosa})
    if ano:
        vmin = -1
        vmax = -vmin
        prec = []
        temp = []
        gosa = []
        for i in season:
            p = get_season_mean(tp, all_periods, [i]).values.flatten()
            t = get_season_mean(t2m, all_periods, [i]).values.flatten()
            co2 = get_season_mean(gpp, all_periods, [i]).values.flatten()
            prec = np.append(prec, p)
            temp = np.append(temp, t)
            gosa = np.append(gosa, co2)
        df_clim = pd.DataFrame({'x':prec, 'y':temp, 'z':gosa})
        df      = df - df_clim
    df    = df.dropna(axis=0)
    splot = sp().mat_map()
    fig   = splot.fig
    ax    = splot.ax
    m     = ax.scatter(df['x'], df['y'], c=df['z'], s=10, alpha=0.7
                       , vmin=vmin, vmax=vmax, cmap='viridis_r'
                       )
    ax.set_xlim(-200, 200)
    ax.set_ylim(-4, 4)
    plt.colorbar(m)
    plt.show()