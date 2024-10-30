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
        ter     = data.trendy['ra'].timeseries[self.group] + data.trendy['rh'].timeseries[self.group]
        gpp     = data.trendy['gpp'].timeseries[self.group]
        gosat   = data.gosat['nbp'].timeseries[np.append(data.gosat['nbp'].name,'mean')]
        fire    = data.fire['fire'].timeseries[fire]
        gos_nee = gosat.subtract(fire, axis=0)

        self.ax = MonthlyPlot(self.ax).co2_flux().ax
        self.ax = VisualLines(self.ax, time).inv_sat(gos_nee, range).ax
        self.ax = VisualLines(self.ax, time).trendy_nee(ter, gpp, self.group).ax
        self.ax = VisualLines(self.ax, time).trendy_gpp(gpp,self.group).ax
        self.ax = VisualLines(self.ax, time).trendy_ter(ter, self.group).ax
        self.ax = VisualLines(self.ax, time).fill_with_crosslin(
            ter[self.group].mean(axis=1), gpp[self.group].mean(axis=1)
            , (ter[self.group].mean(axis=1) > gpp[self.group].mean(axis=1)),
            'purple'
        ).ax
        self.ax = VisualLines(self.ax, time).fill_with_crosslin(
            ter[self.group].mean(axis=1), gpp[self.group].mean(axis=1)
            , (ter[self.group].mean(axis=1) < gpp[self.group].mean(axis=1)),
            'green'
        ).ax
        return self
    def season(self, time, fire):
        ter = data.trendy['ra'].season_cyc[self.group] + data.trendy['rh'].season_cyc[self.group]
        gpp = data.trendy['gpp'].season_cyc[self.group]
        gosat = data.gosat['nbp'].season_cyc[np.append(data.gosat['nbp'].name,'mean')]
        fire = data.fire['fire'].season_cyc[fire]
        gos_nee = gosat.subtract(fire, axis=0)
        ter = change_order(ter, order)
        gpp = change_order(gpp, order)
        gos_nee = change_order(gos_nee, order)

        self.ax = SeasonPlot(self.ax).co2_flux().ax
        self.ax = VisualLines(self.ax, time).inv_sat(gos_nee,True).ax
        self.ax = VisualLines(self.ax, time).trendy_nee(ter, gpp, self.group,True).ax
        self.ax = VisualLines(self.ax, time).trendy_gpp(gpp, self.group,True).ax
        self.ax = VisualLines(self.ax, time).trendy_ter(ter, self.group,True).ax
        self.ax = VisualLines(self.ax, time).fill_with_crosslin(
            ter[self.group].mean(axis=1), gpp[self.group].mean(axis=1)
            , (ter[self.group].mean(axis=1) > gpp[self.group].mean(axis=1)),
            'purple'
        ).ax
        self.ax = VisualLines(self.ax, time).fill_with_crosslin(
            ter[self.group].mean(axis=1), gpp[self.group].mean(axis=1)
            , (ter[self.group].mean(axis=1) < gpp[self.group].mean(axis=1)),
            'green'
        ).ax
        self.ax.set_xticks([3, 6, 9, 12])
        return self
def plt_mn_season(name_lists, fire):
    ter = data.trendy['ra'].season_cyc[name_lists] + data.trendy['rh'].season_cyc[name_lists]
    ter = ter.mean(axis=1)
    gpp = data.trendy['gpp'].season_cyc[name_lists].mean(axis=1)
    plot_mon, plot_sea = plots_design.mn_season().ini_fig()
    plot_mon = CompareNEE(plot_mon, name_lists).monthly(time, fire).ax
    plot_sea = CompareNEE(plot_sea, name_lists).season(month, fire).ax
    plot_sea.errorbar(13, ter.mean(), yerr=[[ter.mean() - ter.min()], [ter.max() - ter.mean()]], color='purple', capsize=3)
    plot_sea.errorbar(14, gpp.mean(), yerr=[[gpp.mean() - gpp.min()], [gpp.max() - gpp.mean()]], color='green', capsize=3)
    plot_mon.set_ylim(-500,2200)
    plots_design.mn_season().same_ylim(plot_mon, plot_sea)
    plots_design.mn_season().optimiz_fig(plot_mon, plot_sea)
    plt.show()
print(__name__)
if __name__.split('.')[-1] == 'plot_NEE':
    from settings import trendy_models as models
    fire  = 'gfed'
    time  = data.gosat['nbp'].dates['range']
    month = np.arange(1, 13, 1, dtype='int')

    good  = data.trendy['nbp'].good_name
    ok    = data.trendy['nbp'].ok_name
    bad   = data.trendy['nbp'].bad_name

    plt_mn_season(models, fire)
    """
    plt_mn_season(good, fire)
    plt_mn_season(ok, fire)
    plt_mn_season(bad, fire)"""