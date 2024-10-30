import pandas as pd
import xarray as xr
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
from statistical_analysis import change_order
from settings import order
from read_pkl import data
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
def lat_or_lon_mean(value, names, direction):
    """
    :param value:
    :param names:
    :param direction: 'lon' or 'lat'
    :return:
    """
    for i, model in enumerate(names):
        if direction == 'lon':
            individual_mean = value[model].mean(dim=direction, skipna=True).T
        else:
            individual_mean = value[model].mean(dim=direction, skipna=True)
        if i == 0:
            sum = individual_mean
        else:
            sum = sum + individual_mean
    mean = sum / len(names)
    return mean
def color_for_obs():
    colors = plt.cm.rainbow(np.linspace(0, 1, 256))
    colors[0] = np.array([1, 1, 1, 1])
    custom_cmap = ListedColormap(colors)
    return custom_cmap
def count_gosat_obs(lat_range,remotec,acos,ls_type):
    lats_bnd = np.arange(lat_range[0], lat_range[1], 1.0)
    lats = np.arange(lat_range[0] + 0.5, lat_range[1] + 0.5, 1.0)
    years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    num_remotec = np.zeros([len(lats), 120])
    num_acos = np.zeros([len(lats), 120])
    j = 0
    for yr in years:
        for mn in months:
            if j != 120:
                # print(yr, mn, j)
                ds = remotec[
                    (remotec['Year'] == yr)
                    & (remotec['Month'] == mn)
                    ]
                # print(yr,mn,ds['lat'])
                i = 0
                for lat_bnd in lats_bnd:
                    lat_min = lat_bnd
                    lat_max = lat_bnd + 1
                    if ls_type == 'all':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            ]
                    if ls_type == 'water':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            & (ds['land_flag'] == 1)
                            ]
                    if ls_type == 'land':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            & (ds['land_flag'] == 0)
                            ]

                    num_remotec[i, j] = len(ds2['CO2'])
                    i = i + 1
                j += 1
    j = 0
    for yr in years:
        for mn in months:
            if j != 120:
                #print(yr, mn, j)
                ds = acos[
                    (acos['Year'] == yr)
                    & (acos['Month'] == mn)
                    ]
                # print(yr,mn,ds['lat'])
                i = 0
                for lat_bnd in lats_bnd:
                    lat_min = lat_bnd
                    lat_max = lat_bnd + 1
                    if ls_type == 'all':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            ]
                    if ls_type == 'water':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            & (ds.land_frac <= 5)
                            ]
                    if ls_type == 'land':
                        ds2 = ds[
                            (ds.lat > lat_min)
                            & (ds.lat <= lat_max)
                            & (ds.land_frac >= 90)
                            & (ds['quality'] == 0)
                            ]

                    num_acos[i, j] = len(ds2['CO2'])
                    i = i + 1
                j = j + 1
                #print(yr, mn, j)
    return num_remotec, num_acos, lats
class Hovmoller:
    def __init__(self, fig, ax, ds):
        self.ds     = ds
        self.fig    = fig
        self.ax     = ax
        self.map    = None
    def lon(self,value):
        self.map  = self.ax.pcolormesh(self.ds.time, self.ds.lat, value, vmin=-4, vmax=4, cmap=plt.cm.seismic)
        self.ax.set_ylim(data.gosat['nbp'].region['lat_min'], data.gosat['nbp'].region['lat_max'])
        cbar = self.fig.colorbar(self.map, ax=self.ax, extend='both')
        cbar.set_label('CO$_2$ flux\n(gC/m$^2$/day)')
        return self
def hovmoller_gosat_vs_insitu_nbp():
    gosat = lat_or_lon_mean(data.gosat['nbp'].spatial, data.gosat['nbp'].name, 'lon')
    insit = lat_or_lon_mean(data.insitu['nbp'].spatial, data.insitu['nbp'].name, 'lon')
    fig = plt.figure(figsize=(10, 6))
    ins = fig.add_subplot(311)
    sat = fig.add_subplot(312)
    ins = Hovmoller(fig, ins, data.insitu['nbp'].spatial).lon(insit).ax
    ins.set_title('A. Inverse model$_{in-situ}$', fontweight='bold')
    sat = Hovmoller(fig, sat, data.gosat['nbp'].spatial).lon(gosat).ax
    sat.set_title('B. Inverse model$_{+GOSAT}$', fontweight='bold')
    plt.tight_layout()
def hovmoller_tm5_gosat_nbps():
    remotec = lat_or_lon_mean(data.gosat['nbp'].spatial, ['RemoTeC'], 'lon')
    acos = lat_or_lon_mean(data.gosat['nbp'].spatial, ['ACOS'], 'lon')
    fig = plt.figure(figsize=(10, 6))
    rem = fig.add_subplot(311)
    aco = fig.add_subplot(312)
    rem = Hovmoller(fig, rem, data.gosat['nbp'].spatial).lon(remotec).ax
    rem.set_title('A. Inverse model$_{+RemoTeC}$', fontweight='bold')
    aco = Hovmoller(fig, aco, data.insitu['nbp'].spatial).lon(acos).ax
    aco.set_title('B. Inverse model$_{+ACOS}$', fontweight='bold')
    plt.tight_layout()
def hovmoller_gosat_obs(ls_type):
    lat_range = [data.gosat['nbp'].region['lat_min'], data.gosat['nbp'].region['lat_max']]
    remotec   = data.concentration['REMOTEC']
    acos      = data.concentration['ACOS']
    remo_no, acos_no, lats = count_gosat_obs(lat_range, remotec, acos, ls_type)
    from data_loader import create_date
    time = create_date('2009-01-01', '2018-12-31')['range']

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax1.set_title('A. RemoTeC sample number', fontweight='bold')
    ax1.set_ylabel('latitude')
    ax2.set_title('B. ACOS sample number', fontweight='bold')
    ax2.set_ylabel('latitude')
    ax2.set_xlabel('time')
    custom_cmap = color_for_obs()
    map1 = ax1.pcolormesh(time, lats, remo_no, vmin=1, vmax=40, cmap=custom_cmap)
    map2 = ax2.pcolormesh(time, lats, acos_no, vmin=1, vmax=100, cmap=custom_cmap)
    #ax1.set_xlim(pd.Timestamp('2009-01-01'), pd.Timestamp('2018-12-31'))
    #ax2.set_xlim(pd.Timestamp('2009-01-01'), pd.Timestamp('2018-12-31'))
    cbar1 = fig.colorbar(map1, ax=ax1, extend='both')
    cbar2 = fig.colorbar(map2, ax=ax2, extend='both')
    cbar1.set_label('RemoTeC\nN obs.')
    cbar2.set_label('ACOS\nN obs.')
    plt.tight_layout()
def hovmoller_invers_nbps():
    tm5 = lat_or_lon_mean(data.insitu['nbp'].spatial, ['TM5-4DVAR'], 'lon')
    CAMS = lat_or_lon_mean(data.insitu['nbp'].spatial, ['CAMS'], 'lon')
    carb = lat_or_lon_mean(data.insitu['nbp'].spatial, ['CarbonTracker'], 'lon')
    fig = plt.figure(figsize=(10, 6))
    tm = fig.add_subplot(311)
    ca = fig.add_subplot(312)
    ct = fig.add_subplot(313)
    tm = Hovmoller(fig, tm, data.gosat['nbp'].spatial).lon(tm5).ax
    tm.set_title('A. TM5-4DVAR$_{in-situ}$', fontweight='bold')
    ca = Hovmoller(fig, ca, data.insitu['nbp'].spatial).lon(CAMS).ax
    ca.set_title('B. CAMS$_{in-situ}$', fontweight='bold')
    ct = Hovmoller(fig, ct, data.insitu['nbp'].spatial).lon(carb).ax
    ct.set_title('C. CarbonTracker$_{in-situ}$', fontweight='bold')
    plt.tight_layout()
def hovmoller_fire_emit():
    gfed = lat_or_lon_mean(data.fire['fire'].spatial, ['gfed'], 'lon')
    gfas = lat_or_lon_mean(data.fire['fire'].spatial, ['gfas'], 'lon')
    finn = lat_or_lon_mean(data.fire['fire'].spatial, ['finn'], 'lon')
    fig = plt.figure(figsize=(10, 6))
    GFED = fig.add_subplot(311)
    GFAS = fig.add_subplot(312)
    FINN = fig.add_subplot(313)
    GFED = Hovmoller(fig, GFED, data.gosat['nbp'].spatial).lon(gfed).ax
    GFED.set_title('A. GFED', fontweight='bold')
    GFAS = Hovmoller(fig, GFAS, data.insitu['nbp'].spatial).lon(gfas).ax
    GFAS.set_title('B. GFAS', fontweight='bold')
    FINN = Hovmoller(fig, FINN, data.insitu['nbp'].spatial).lon(finn).ax
    FINN.set_title('C. FINN', fontweight='bold')
    plt.tight_layout()
print(__name__)
if __name__.split('.')[-1] == 'hovmoller':
    hovmoller_gosat_vs_insitu_nbp()
    hovmoller_tm5_gosat_nbps()
    hovmoller_gosat_obs('land')
    hovmoller_invers_nbps()
    hovmoller_fire_emit()
    plt.show()


