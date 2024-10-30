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
from statistical_analysis import custom_yrsum as cyrsum
from settings import order
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
from plots import plots_design
import numpy as np
print(__name__)
if __name__.split('.')[-1] == 'plot_IAV':
    from settings import trendy_models
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
    mn1 = '06'
    mn2 = '05'
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
    time   = pd.to_datetime(gosif['Time'])
    time2 = data.gosat['nbp'].dates['range']

    fig = plt.figure(figsize=(11, 3.5))
    ax = fig.add_subplot(111)
    ax = MonthlyPlot(ax).co2_flux().ax
    ax = VisualLines(ax, time2).inv_sat(data.gosat['nbp'].timeseries, True).ax
    ax = VisualLines(ax, time2).inv_insitu(data.insitu['nbp'].timeseries, True).ax
    ax = VisualLines(ax, time2).trendy_nbp(-data.trendy['nbp'].timeseries, trendy_models,  True).ax
    legend1 = ax.legend(loc='lower left', title="Monthly flux")
    ax.add_artist(legend1)
    cplt.bar(time, gosat.mean(axis=1).values, ax, 'r', label='Inverse model$_{+GOSAT}$')
    cplt.bar(time, insitu.mean(axis=1).values, ax, 'b', label='Inverse model$_{in-situ}$')
    cplt.bar(time, -trendy.nbp[trendy_models].mean(axis=1).values, ax, 'k', label='TRENDY')
    legend2 = ax.legend(handles=[plt.Line2D([0], [0], color='r', alpha=0.4, lw=4, label='Inverse model$_{+GOSAT}$'),
                                 plt.Line2D([0], [0], color='b', alpha=0.4, lw=4, label='Inverse model$_{in-situ}$')],
                        loc='lower right', title="Annual flux June — July")
    plt.tight_layout()
    plt.show()


