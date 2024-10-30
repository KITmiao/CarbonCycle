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
class CompareNEE:
    def __init__(self, ax, group_list):
        self.ax    = ax
        self.group = group_list
    def monthly(self, time, fire):
        nbp     = -data.trendy['nbp'].timeseries[self.group]
        gosat   = data.gosat['nbp'].timeseries[np.append(data.gosat['nbp'].name,'mean')]
        fire    = data.fire['fire'].timeseries[fire]
        gos_nee = gosat

        self.ax = MonthlyPlot(self.ax).co2_flux().ax
        self.ax = VisualLines(self.ax, time).inv_sat(gos_nee, True).ax
        self.ax = VisualLines(self.ax, time).trendy_nbp(nbp, self.group,True).ax
        return self
    def season(self, time, fire):
        nbp = -data.trendy['nbp'].season_cyc[self.group]
        gosat = data.gosat['nbp'].season_cyc[np.append(data.gosat['nbp'].name,'mean')]
        fire = data.fire['fire'].season_cyc[fire]
        gos_nee = gosat
        nbp = change_order(nbp, order)
        gos_nee = change_order(gos_nee, order)

        self.ax = SeasonPlot(self.ax).co2_flux().ax
        self.ax = VisualLines(self.ax, time).inv_sat(gos_nee,True).ax
        self.ax = VisualLines(self.ax, time).trendy_nbp(nbp, self.group,True).ax
        self.ax.set_xticks([3, 6, 9, 12])
        return self
def plt_mn_season(name_lists, fire):
    nbp = -data.trendy['nbp'].season_cyc[name_lists].mean(axis=1)
    gosat = data.gosat['nbp'].season_cyc[np.append(data.gosat['nbp'].name, 'mean')]
    plot_mon, plot_sea = plots_design.mn_season().ini_fig()
    plot_mon = CompareNEE(plot_mon, name_lists).monthly(time, fire).ax
    plot_sea = CompareNEE(plot_sea, name_lists).season(month, fire).ax
    plot_sea.errorbar(13, nbp.mean(),yerr=[[nbp.mean() - nbp.min()], [nbp.max() - nbp.mean()]],color='k',capsize=3)
    plot_sea.errorbar(14, gosat['mean'].mean(), yerr=[[gosat['mean'].mean() - gosat['mean'].min()], [gosat['mean'].max() - gosat['mean'].mean()]], color='firebrick', capsize=3)
    plot_mon.set_ylim(-500,500)
    plots_design.mn_season().same_ylim(plot_mon, plot_sea)
    plots_design.mn_season().optimiz_fig(plot_mon, plot_sea)
    plt.show()
print(__name__)
if __name__.split('.')[-1] == 'plot_NBP':
    from settings import trendy_models as models
    fire  = 'gfed'
    time  = data.gosat['nbp'].dates['range']
    month = np.arange(1, 13, 1, dtype='int')

    good  = data.trendy['nbp'].good_name
    ok    = data.trendy['nbp'].ok_name
    bad   = data.trendy['nbp'].bad_name

    plt_mn_season(models, fire)