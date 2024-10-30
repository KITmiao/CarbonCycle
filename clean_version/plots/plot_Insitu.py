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
print(__name__)
if __name__.split('.')[-1] == 'plot_Insitu':
    time = data.gosat['nbp'].dates['range']
    pris = data.gosat['prior'].timeseries
    ins  = data.insitu['nbp'].timeseries
    gos  = data.gosat['nbp'].timeseries

    fig, ax = plt.subplots(figsize=(10, 3))
    ax = MonthlyPlot(ax).co2_flux().ax
    ax = VisualLines(ax, time).tm5_4dvar_insitu(ins).ax
    ax = VisualLines(ax, time).cams(ins).ax
    ax = VisualLines(ax, time).ct(ins).ax
    plt.legend(ncol=3)
    plt.show()