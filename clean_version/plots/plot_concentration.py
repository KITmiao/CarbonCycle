import data_loader
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
from statistical_analysis import colum_filter
from settings import order
from read_pkl import data
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
from plots import plots_design
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
class PlotCon:
    def __init__(self, remotec, acos, tm5, carbontracker, cams):
        self.remotec = remotec
        self.acos    = acos
        self.tm5     = tm5
        self.ct      = carbontracker
        self.cams    = cams

        self.go = pd.DataFrame(columns=['remotec','acos'])
        self.go['remotec'] = self.remotec[-117:]
        self.go['acos'] = self.acos[-117:]
        self.ins = pd.DataFrame(columns=['tm5','carbontracker','cams'])
        self.ins['tm5'] = self.tm5
        self.ins['cams'] = self.cams
        self.ins['carbontracker'] = self.ct

        self.gosat   = self.go.mean(axis=1)
        self.gosat_lb= self.go.min(axis=1)
        self.gosat_ub= self.go.max(axis=1)
        self.insitu  = self.ins.mean(axis=1)
        self.insitu_lb = self.ins.min(axis=1)
        self.insitu_ub = self.ins.max(axis=1)
    def detrend(self):
        dates              = data_loader.create_date('2009-04-01', '2018-12-31')
        self.go['month']   = dates['range'].strftime('%m').tolist()
        self.go['month']   = self.go['month'].astype(int)
        self.go['remotec'] = data_loader.detrend_go(self.go['remotec'])
        self.go['acos']    = data_loader.detrend_go(self.go['acos'])
        self.ins['month']  = dates['range'].strftime('%m').tolist()
        self.ins['month']  = self.ins['month'].astype(int)
        self.ins['tm5']    = data_loader.detrend_go(self.ins['tm5'])
        self.ins['cams']   = data_loader.detrend_go(self.ins['cams'])
        self.ins['carbontracker'] = data_loader.detrend_go(self.ins['carbontracker'])
        return self
    def plot_concentration(self, ax, time):
        go = self.go[['remotec','acos']]
        ins = self.ins[['tm5', 'cams', 'carbontracker']]
        #time = data_loader.create_date('2009-04-01', '2018-12-31')['range']
        ax.plot(time, (go['remotec']+go['acos'])/2, color='firebrick', marker='.', label='GOSAT')
        ax.fill_between(time, go['remotec'], go['acos'], color='red', alpha=0.3)
        ax.plot(time, (ins['tm5']+ins['cams']+ins['carbontracker'])/3, color='royalblue', marker='.', label='Inverse model$_{in-situ}$')
        ax.fill_between(time, ins.min(axis=1), ins.max(axis=1), color='royalblue', alpha=0.3)
        """
        for years in ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']:
            ax.axvline(pd.to_datetime(f'{years}-01-01'),
                        color='gray', linestyle='-', linewidth=0.8, alpha=0.5)
        ax.set_xlabel('year')
        ax.set_ylabel('Detrended CO$_2$ (ppm)', labelpad=-5)
        ax.set_xlim(pd.Timestamp('2009-01-01'), pd.Timestamp('2018-12-31'))
        """
        #ax.legend(loc='upper right')
        #ax.set_ylim([-1.7,1.7])
print(__name__)
if __name__.split('.')[-1] == 'plot_concentration':
    from settings import setting
    settings = setting
    mask = data.trendy['nbp']
    dates = data_loader.create_date('2009-04-01', '2018-12-31')
    month = np.arange(1, 13, 1, dtype='int')
    GOS = data_loader.load_gosat_con(remofile=settings['REMOTEC'], acosfile=settings['ACOS'], dates=dates)
    REMOTEC = GOS['RemoTeC']
    ACOS = GOS['ACOS']
    transcom = xr.open_dataset('/home/mhuang/data/regions_regrid.nc')
    TM5 = \
    data_loader.load_tm5_4dvar_con(path=settings['TM5-4DVAR'], transcom_region=name_dic.transcom[settings['region']],
                                   trans=transcom)['xco2_monmean']
    CT = data_loader.load_carbontracker_con(path=settings['CarbonTracker'],
                                            transcom_region=name_dic.transcom[settings['region']], trans=transcom)[
        'xco2_monmean']
    CAMS = data_loader.load_cams_con(path=settings['CAMS'], transcom_region=name_dic.transcom[settings['region']],
                                     trans=transcom)['xco2_monmean'] * 1e6
    plotcon = PlotCon(
        remotec=REMOTEC,
        acos=ACOS,
        tm5=TM5,
        carbontracker=CT,
        cams=CAMS
    ).detrend()

    ax_mon, ax_sea = plots_design.mn_season().ini_fig()
    ax_mon         = MonthlyPlot(ax_mon).co2_conc().ax
    ax_sea         = SeasonPlot(ax_sea).co2_conc().ax
    plotcon.plot_concentration(ax=ax_mon, time=dates['range'])
    plotcon.go = data_loader.get_season_cycle(plotcon.go, ['remotec', 'acos'])
    plotcon.ins = data_loader.get_season_cycle(plotcon.ins, ['tm5', 'cams', 'carbontracker'])
    plotcon.plot_concentration(ax=ax_sea, time=month)
    plots_design.mn_season().same_ylim(ax_mon, ax_sea)
    plots_design.mn_season().optimiz_fig(ax_mon, ax_sea)
    ax_sea.set_xticks([3, 6, 9, 12])
    ax_mon.legend(loc='upper right')
    plt.show()