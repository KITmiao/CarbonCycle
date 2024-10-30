import pandas as pd
import custom_matplotlib as cplt
import name_dic
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
from read_pkl import data, data2
from monthly_plots import MonthlyPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
from statistical_analysis import change_order
from statistical_analysis import get_season_mean
from statistical_analysis import simple_moving_average as sma
from statistical_analysis import custom_yrsum as cyrsum
from settings import order
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
from plots import plots_design
import numpy as np
print(__name__)
def plot_all_fire(ax,time,ds):
    ax = VisualLines(ax, time).gfed(ds).ax
    ax = VisualLines(ax, time).gfas(ds).ax
    ax = VisualLines(ax, time).finn(ds/10).ax
    return ax
def compare_monthly_invs(ax,time,value1,value2):
    ax = MonthlyPlot(ax).co2_flux().ax
    ax = VisualLines(ax, time).inv_sat(value1, True).ax
    ax = VisualLines(ax, time).inv_insitu(value2, True).ax
    return ax
def compare_season_invs(ax,time,value1,value2):
    ax = SeasonPlot(ax).co2_flux().ax
    f  = change_order(data.fire['fire'].season_cyc, order)
    #ax = plot_all_fire(ax,time,change_order(data.fire['fire'].season_cyc, order))
    gosat = change_order(data.gosat['nbp'].season_cyc-data2.gosat['nbp'].season_cyc, order)
    insitu = change_order(data.insitu['nbp'].season_cyc-data2.insitu['nbp'].season_cyc, order)
    ax = VisualLines(ax, time).inv_sat(gosat, True).ax
    ax = VisualLines(ax, time).inv_insitu(insitu, True).ax
    ax.set_xticks([3, 6, 9, 12])
    return ax

if __name__.split('.')[-1] == 'plot_2region_diff':
    class GosFlux:
        def __init__(self, flux):
            self.RemoTeC = flux['RemoTeC']
            self.ACOS    = flux['ACOS']
            self.mean    = flux.mean(axis=1, skipna=True)
            self.std     = flux.std(axis=1, skipna=True)
    class InsFlux:
        def __init__(self, flux):
            self.RemoTeC = flux['RemoTeC']
            self.ACOS    = flux['ACOS']
            self.mean    = flux.mean(axis=1, skipna=True)
            self.std     = flux.std(axis=1, skipna=True)
    class Region:
        def __init__(self, flux1, flux2):
            self.flux1 = flux1
            self.flux2 = flux2
    time  = data.gosat['nbp'].dates['range']
    rtime = time[6:-5]
    month = np.arange(1, 13, 1, dtype='int')
    from settings import spatial_period
    mn1 = spatial_period['start'][5:7]
    mn2 = spatial_period['end'][5:7]

    gosat  = data.gosat['nbp'].timeseries - data2.gosat['nbp'].timeseries
    insitu = data.insitu['nbp'].timeseries - data2.insitu['nbp'].timeseries
    value1 = data.gosat['nbp'].timeseries
    #value1 = value1.loc[(value1['time'] >= '2009-04-01') & (value1['time'] <= '2018-12-31')]
    value2 = data2.gosat['nbp'].timeseries
    clim1  = data.gosat['nbp'].season_cyc
    clim2  = data2.gosat['nbp'].season_cyc
    ano1   = pd.DataFrame()
    ano1['RemoTeC'] = value1.apply(lambda row: row['RemoTeC'] - clim1.loc[row['month'], 'RemoTeC'], axis=1)
    ano1['ACOS'] = value1.apply(lambda row: row['ACOS'] - clim1.loc[row['month'], 'ACOS'], axis=1)
    ano2 = pd.DataFrame()
    ano2['RemoTeC'] = value2.apply(lambda row: row['RemoTeC'] - clim2.loc[row['month'], 'RemoTeC'], axis=1)
    ano2['ACOS'] = value2.apply(lambda row: row['ACOS'] - clim2.loc[row['month'], 'ACOS'], axis=1)
    dif  = ano1-ano2
    ano1 = GosFlux(ano1)
    ano2 = GosFlux(ano2)
    dif  = GosFlux(dif)
    fig = plt.figure(figsize=(11, 3.5))
    ax  = fig.add_subplot(111)
    ax  = MonthlyPlot(ax).co2_flux().ax
    dif_sum = cyrsum(dif.mean,mn1,mn2)
    print(dif_sum)
    ax.plot(time, dif.mean * 1e9,label='dif',marker='.')
    time2 = pd.to_datetime(dif_sum['Time'])
    print(dif_sum['Sum'].values)
    cplt.bar(time2.values, dif_sum['Sum'].values * 1e9,ax,'b')
    ax.set_ylabel('$\Delta$CO$_2$ flux (g month$_{-1}$ m$_{-2}$)')
    #ax.set_ylim(-0.05, 0.05)
    fig = plt.figure(figsize=(11, 3.5))
    ax = fig.add_subplot(111)
    ax = MonthlyPlot(ax).co2_flux().ax
    ax.plot(time, ano1.mean * 1e11,label='west')
    ax.set_ylim(-2.5, 2.5)
    fig = plt.figure(figsize=(11, 3.5))
    ax = fig.add_subplot(111)
    ax = MonthlyPlot(ax).co2_flux().ax
    ax.plot(time, ano2.mean * 1e11, label='east')
    ax.set_ylim(-2.5,2.5)
    plt.show()
    """
    print(dif.mean.values)
    rtime = time[3:-2]
    gosat_rm = sma(dif.mean, 6)
    fig = plt.figure(figsize=(11, 3.5))
    ax = fig.add_subplot(111)
    ax = MonthlyPlot(ax).co2_flux().ax
    ax.plot(time, dif.mean, label='dif')
    ax.plot(rtime, gosat_rm, label='dif')
    ax.legend()
    plt.show()
    """