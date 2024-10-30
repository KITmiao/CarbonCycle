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
from plots import plots_design
import data_loader
class PlotPrecip():
    def __init__(self,ax):
        self.ax = ax
    def monthly(self, time, rain):
        self.ax = MonthlyPlot(self.ax).rain().ax
        self.ax = VisualLines(self.ax, time).precipitation(rain, None).ax
        self.ax.set_ylim(0, rain.max()+70)
        return self
    def season(self, time, value, obj):
        value = change_order(value, order)
        self.ax = SeasonPlot(self.ax).rain().ax
        self.ax = VisualLines(self.ax, time).precipitation(value[obj], None).ax
        self.ax.set_xticks([3, 6, 9, 12])
        return self
class PlotTemp():
    def __init__(self,ax):
        self.ax = ax
    def monthly(self, time, temp):
        self.ax = MonthlyPlot(self.ax).remove_hline().temp().ax
        self.ax = VisualLines(self.ax, time).temp(temp, None).ax
        return self
    def season(self, time, value, obj):
        value = change_order(value, order)
        self.ax = SeasonPlot(self.ax).remove_hline().temp().ax
        self.ax = VisualLines(self.ax, time).temp(value[obj], None).ax
        self.ax.set_xticks([3, 6, 9, 12])
        return self
print(__name__)
if __name__.split('.')[-1] == 'plot_meteo':
    time = data.era5.dates['range']
    month = np.arange(1, 13, 1, dtype='int')
    data.era5.timeseries['tp']  = data.era5.timeseries['tp'] * 1000 * data.era5.timeseries['days'] # unit to mm month-1
    data.era5.timeseries['t2m']  = data.era5.timeseries['t2m'] - 273.15 # unit to ℃
    tp    = data.era5.timeseries['tp']
    t2m   = data.era5.timeseries['t2m']
    season= data_loader.get_season_cycle(data.era5.timeseries, ['tp', 't2m'])

    plot_mon, plot_sea = plots_design.mn_season().ini_fig()
    plot_mon  = PlotPrecip(plot_mon).monthly(time, tp).ax
    plot_sea  = PlotPrecip(plot_sea).season(month, season, 'tp').ax
    plots_design.mn_season().same_ylim(plot_mon, plot_sea)
    plots_design.mn_season().optimiz_fig(plot_mon, plot_sea)

    t2m_mon   = plot_mon.twinx()
    t2m_sea   = plot_sea.twinx()
    t2m_mon   = PlotTemp(t2m_mon).monthly(time, t2m).ax
    t2m_sea   = PlotTemp(t2m_sea).season(month, season, ['t2m']).ax
    plots_design.mn_season().ytick_color(t2m_sea,'right', 'r')
    plots_design.mn_season().optimiz_fig(t2m_sea, t2m_mon)
    plt.show()