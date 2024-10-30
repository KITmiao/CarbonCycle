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
print(__name__)
def plot_all_fire(ax,time,ds):
    ax = VisualLines(ax, time).gfed(ds).ax
    ax = VisualLines(ax, time).gfas(ds).ax
    ax = VisualLines(ax, time).finn(ds/10).ax
    return ax
def compare_monthly_invs(ax,time,*fire):
    ax = MonthlyPlot(ax).co2_flux().ax
    if fire:
        ax = VisualLines(ax, time).inv_sat(data.gosat['nbp'].timeseries, True).ax
        ax = VisualLines(ax, time).inv_insitu(data.insitu['nbp'].timeseries, True).ax
        ax = VisualLines(ax, time).gfed(data.fire['fire'].timeseries).ax
    else:
        ax = plot_all_fire(ax,time,data.fire['fire'].timeseries)
        ax = VisualLines(ax, time).inv_sat(data.gosat['nbp'].timeseries,True).ax
        ax = VisualLines(ax, time).inv_insitu(data.insitu['nbp'].timeseries,True).ax
    return ax
def compare_season_invs(ax,time,*fire):
    ax = SeasonPlot(ax).co2_flux().ax
    f  = change_order(data.fire['fire'].season_cyc, order)
    if fire:
        ax = VisualLines(ax, time).gfed(f).ax
    else:
        ax = plot_all_fire(ax, time, f)
    #ax = plot_all_fire(ax,time,change_order(data.fire['fire'].season_cyc, order))
    gosat = change_order(data.gosat['nbp'].season_cyc, order)
    insitu = change_order(data.insitu['nbp'].season_cyc, order)
    ax = VisualLines(ax, time).inv_sat(gosat, True).ax
    ax = VisualLines(ax, time).inv_insitu(insitu, True).ax
    ax.set_xticks([3, 6, 9, 12])
    return ax
def compare_monthly_diff(ax,time):
    ax = MonthlyPlot(ax).co2_flux().ax
    ax = plot_all_fire(ax, time, data.fire['fire'].timeseries)
    ax.plot(time, data.gosat['nbp'].timeseries['mean'] - data.insitu['nbp'].timeseries['mean'],
            color='k', label='difference')
    return ax
def compare_season_diff(ax,time):
    ax = SeasonPlot(ax).co2_flux().ax
    ax = plot_all_fire(ax, time, change_order(data.fire['fire'].season_cyc, order))
    gosat  = change_order(data.gosat['nbp'].season_cyc, order)
    insitu = change_order(data.insitu['nbp'].season_cyc, order)
    ax.plot(time, gosat['mean'] - insitu['mean'],
            color='k', label='difference')
    ax.set_xticks([3, 6, 9, 12])
    return ax
if __name__.split('.')[-1] == 'compare_fire':
    time = data.gosat['nbp'].dates['range']
    month = np.arange(1, 13, 1, dtype='int')

    plot_mon, plot_sea = plots_design.mn_season().ini_fig()
    plot_mon = compare_monthly_invs(plot_mon, time, 'GFED')
    plot_sea = compare_season_invs(plot_sea, month, 'GFED')
    plots_design.mn_season().same_ylim(plot_mon, plot_sea)
    plots_design.mn_season().optimiz_fig(plot_mon, plot_sea)
    plt.show()

    plot_mon, plot_sea = plots_design.mn_season().ini_fig()
    plot_mon = compare_monthly_invs(plot_mon, time)
    plot_sea = compare_season_invs(plot_sea, month)
    plots_design.mn_season().same_ylim(plot_mon, plot_sea)
    plots_design.mn_season().optimiz_fig(plot_mon, plot_sea)
    plt.show()

    plot_mon, plot_sea = plots_design.mn_season().ini_fig()
    plot_mon = compare_monthly_diff(plot_mon, time)
    plot_sea = compare_season_diff(plot_sea, month)
    plots_design.mn_season().same_ylim(plot_mon, plot_sea)
    plots_design.mn_season().optimiz_fig(plot_mon, plot_sea)
    plt.show()
