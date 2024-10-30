import data_loader
import name_dic
import numpy as np

import settings
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
import scipy.stats as stats
print(__name__)
def compare_monthly_invs(ax,time):
    ax = MonthlyPlot(ax).co2_flux().ax
    ax = VisualLines(ax, time).inv_sat(data.gosat['nbp'].timeseries, True).ax

    return ax
if __name__.split('.')[-1] == 'pc_with_PCFnbp':
    if settings.nbp_with_PCFpcs == 'PCF':
        from statistical.eof_pc_PCFssta import pcs,n
    if settings.nbp_with_PCFpcs == 'IDA':
        from statistical.eof_pc_IDAssta import pcs,n

    gosat = data.gosat['nbp'].timeseries#/data.gosat['nbp'].timeseries.std(axis=0, skipna=True)
    print(gosat)
    time = data.gosat['nbp'].dates['range']
    month = np.arange(1, 13, 1, dtype='int')
    # Group by 'month' and subtract the mean within each group for all columns except 'month'
    gosat_grouped = gosat.groupby('month')

    # Subtract the mean for each group (month) and return the anomalies
    ano = gosat_grouped.transform(lambda x: x - x.mean())

    for i in range(n):
        pc = pcs.loc['2009-01-01':'2018-12-31', pcs.columns[i]]
        if i == 0:
            sum = pc
        else:
            sum=sum+pc
        r, p = stats.pearsonr(gosat['mean'], pc)
        fig, ax = plt.subplots(figsize=(7,3))
        ax = MonthlyPlot(ax).ax
        ax = VisualLines(ax, time).inv_sat(gosat, 'range').ax
        ax.plot(time, pc, label=f'Pacific SSTa PC{i+1}')
        ax.legend(loc='best')
        if p < 0.05:
            ax.set_title(f'r={r}, p < 0.05')
        else:
            ax.set_title(f'r={r}, n.s.')

        plt.tight_layout()
        plt.show()
    r, p = stats.pearsonr(gosat['mean'], sum)
    fig, ax = plt.subplots(figsize=(7, 3))
    ax = MonthlyPlot(ax).ax
    ax = VisualLines(ax, time).inv_sat(gosat, 'range').ax
    ax.plot(time, sum, label=f'Pacific SSTa PC1+PC2')
    ax.legend(loc='best')
    if p < 0.05:
        ax.set_title(f'r={r}, p < 0.05')
    else:
        ax.set_title(f'r={r}, n.s.')

    plt.tight_layout()
    plt.show()

    fig, ax = plt.subplots(n+2, 1, figsize=(7, 1.5*(n+2)))
    ax[0] = MonthlyPlot(ax[0]).ax
    ax[0] = VisualLines(ax[0], time).inv_sat(data.gosat['nbp'].timeseries, 'range').ax
    ax[0].set_xlabel(None)
    ax[0].set_xticks([])
    ax[0].set_ylim([-200,350])
    ax[0].set_ylabel('Net CO${_2}$ flux\n(Tg/month)')
    ax[0].spines['bottom'].set_visible(False)
    ax[1] = MonthlyPlot(ax[1]).ax
    ax[1].plot(time, sum, label='PC1+PC2', c='k')
    ax[1].set_xlabel(None)
    ax[1].set_xticks([])
    ax[1].set_yticks([0])
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['bottom'].set_visible(False)
    ax[1].set_ylim([-6, 6])
    c = ['y', 'aqua', 'm', 'limegreen']
    for i in range(n):
        pc      = pcs.loc['2009-01-01':'2018-12-31', pcs.columns[i]]
        ax[i+2] = MonthlyPlot(ax[i+2]).ax
        ax[i+2].plot(time, pc, label=f'PC{i + 1}', c=c[i])
        ax[i+2].set_yticks([0])
        ax[i+2].spines['top'].set_visible(False)
        ax[i+2].set_ylim([-6, 6])
        if i != n-1:
            ax[i+2].set_xlabel(None)
            ax[i+2].set_xticks([])
            ax[i+2].spines['bottom'].set_visible(False)
    handles_list = []
    labels_list = []
    for i in range(n + 2):
        handles, labels = ax[i].get_legend_handles_labels()
        handles_list.extend(handles)
        labels_list.extend(labels)
    if handles_list:
        ax[0].legend(handles_list, labels_list, loc='upper right',ncol=4, frameon=False)
    plt.subplots_adjust(hspace=0)
    for i in [2, 3]:
        pos = ax[i].get_position()
        ax[i].set_position([pos.x0, pos.y0 + 0.02 * i, pos.width, pos.height])
    plt.show()

    fig, ax = plt.subplots(n + 2, 1, figsize=(7, 1.5 * (n + 2)))
    ax[0] = MonthlyPlot(ax[0]).ax
    ax[0] = VisualLines(ax[0], time).inv_sat(ano, 'range').ax
    ax[0].set_xlabel(None)
    ax[0].set_xticks([])
    ax[0].set_ylabel('Net CO${_2}$ flux\n(Tg/month)')
    ax[0].spines['bottom'].set_visible(False)
    ax[1] = MonthlyPlot(ax[1]).ax
    ax[1].plot(time, sum, label='PC1+PC2', c='k')
    ax[1].set_xlabel(None)
    ax[1].set_xticks([])
    ax[1].set_yticks([0])
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['bottom'].set_visible(False)
    ax[1].set_ylim([-6, 6])
    c = ['y', 'aqua', 'm', 'limegreen']
    for i in range(n):
        pc = pcs.loc['2009-01-01':'2018-12-31', pcs.columns[i]]
        ax[i + 2] = MonthlyPlot(ax[i + 2]).ax
        ax[i + 2].plot(time, pc, label=f'PC{i + 1}', c=c[i])
        ax[i + 2].set_yticks([0])
        ax[i + 2].spines['top'].set_visible(False)
        ax[i + 2].set_ylim([-6, 6])
        if i != n - 1:
            ax[i + 2].set_xlabel(None)
            ax[i + 2].set_xticks([])
            ax[i + 2].spines['bottom'].set_visible(False)
    handles_list = []
    labels_list = []
    for i in range(n + 2):
        handles, labels = ax[i].get_legend_handles_labels()
        handles_list.extend(handles)
        labels_list.extend(labels)
    if handles_list:
        ax[0].legend(handles_list, labels_list, loc='upper right', ncol=4, frameon=False)
    plt.subplots_adjust(hspace=0)
    for i in [2, 3]:
        pos = ax[i].get_position()
        ax[i].set_position([pos.x0, pos.y0 + 0.02 * i, pos.width, pos.height])
    plt.show()

