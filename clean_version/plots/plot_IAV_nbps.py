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
from read_pkl import data
from monthly_plots import MonthlyPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
from statistical_analysis import change_order
from statistical_analysis import get_season_mean
from statistical_analysis import simple_moving_average as sma
from statistical_analysis import custom_yrsum2 as cyrsum
from settings import order
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
from plots import plots_design
import numpy as np
print(__name__)
if __name__.split('.')[-1] == 'plot_IAV_nbps':
    from settings import trendy_models, all_models
    def dif_times(mn):
        return [f'2009-{mn}', f'2010-{mn}', f'2011-{mn}', f'2012-{mn}', f'2013-{mn}', f'2014-{mn}', f'2015-{mn}', f'2016-{mn}', f'2017-{mn}', f'2018-{mn}']
    def yrmean(data, names):
        df = pd.DataFrame(columns=names)
        for model in names:
            df[model] = cyrsum(data[model], mn1, mn2)['Sum']
        return df
    class TRENDY:
        def __init__(self,nbp,gpp,ra,rh,fire,luc):
            self.nbp  = nbp
            self.gpp  = gpp
            self.ra   = ra
            self.rh   = rh
            self.fire = fire
            self.luc  = luc
    class SatGPP:
        def __init__(self, gosif, nirv):
            self.gosif = gosif
            self.nirv  = nirv
    mn1 = '01'
    mn2 = '12'
    nbp    = data.trendy['nbp'].timeseries
    nbp    = yrmean(nbp, name_dic.trendy_names_v11)
    gpp    = data.trendy['gpp'].timeseries
    gpp    = yrmean(gpp, name_dic.trendy_names_v11)
    ra     = data.trendy['ra'].timeseries
    ra     = yrmean(ra, name_dic.trendy_names_v11)
    rh     = data.trendy['rh'].timeseries
    rh     = yrmean(rh, name_dic.trendy_names_v11)
    fire   = data.trendy['fFire'].timeseries
    fire   = yrmean(fire, name_dic.trendy_names_v11)
    luc    = data.trendy['fLuc'].timeseries
    luc    = yrmean(luc, name_dic.trendy_names_v11)
    trendy = TRENDY(nbp,gpp,ra,rh,fire,luc)
    nirv   = data.est['nirvgpp'].timeseries['GPP']
    nirv   = cyrsum(nirv, mn1, mn2)
    gosif  = data.est['sifgpp'].timeseries['GOSIF']
    gosif  = cyrsum(gosif, mn1, mn2)
    satgpp = SatGPP(gosif,nirv)
    gosat  = data.gosat['nbp'].timeseries
    gosat  = yrmean(gosat, name_dic.tm5gosat_names)
    insitu = data.insitu['nbp'].timeseries
    insitu = yrmean(insitu, name_dic.tm5is_names)
    fire   = data.fire['fire'].timeseries
    fire   = yrmean(fire, name_dic.fire_names)
    time_gos   = pd.to_datetime(dif_times('01'))
    time_ins   = pd.to_datetime(dif_times('04'))
    time_trendy_all= pd.to_datetime(dif_times('07'))
    time_trendy_sel = pd.to_datetime(dif_times('10'))

    fig = plt.figure(figsize=(11, 3.5))
    ax = fig.add_subplot(111)
    ax = MonthlyPlot(ax).co2_flux().ax
    ax.bar(time_gos, gosat.mean(axis=1).values[0:10], width=70, color='r', align='edge',alpha=0.8)
    ax.errorbar(pd.to_datetime(dif_times('02')), gosat.mean(axis=1).values[0:10],
                yerr=(gosat.max(axis=1).values[0:10]-gosat.min(axis=1).values[0:10])/2, fmt='none',
                ecolor='black',
                capsize=3)
    ax.bar(time_ins, insitu.mean(axis=1).values[0:10], width=70, color='b', align='edge',alpha=0.8)
    ax.errorbar(pd.to_datetime(dif_times('05')), insitu.mean(axis=1).values[0:10],
                yerr=(insitu.max(axis=1).values[0:10] - insitu.min(axis=1).values[0:10]) / 2, fmt='none', ecolor='black',
                capsize=3)
    ax.bar(time_trendy_all, -trendy.nbp[all_models].mean(axis=1).values[0:10], width=70, color='w' ,edgecolor='k', align='edge',alpha=0.8)
    ax.errorbar(pd.to_datetime(dif_times('08')), -trendy.nbp[all_models].mean(axis=1).values[0:10],
                yerr=trendy.nbp[all_models].std(axis=1).values[0:10], fmt='none',
                ecolor='black',
                capsize=3)
    ax.bar(time_trendy_sel, -trendy.nbp[trendy_models].mean(axis=1).values[0:10], width=70, color='grey', align='edge',alpha=0.8)
    ax.errorbar(pd.to_datetime(dif_times('11')), -trendy.nbp[trendy_models].mean(axis=1).values[0:10],
                yerr=trendy.nbp[trendy_models].std(axis=1).values[0:10], fmt='none',
                ecolor='black',
                capsize=3)
    plt.show()


