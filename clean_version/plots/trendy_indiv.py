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
if __name__ == 'trendy_indiv' or __name__ == 'plots.trendy_indiv':
    from settings import trendy_models as models
    time    = data.gosat['nbp'].dates['range']
    fig, ax = plt.subplots(figsize=(10, 3))
    ax = MonthlyPlot(ax).co2_flux().ax
    ax = VisualLines(ax,time).inv_sat(
        data.gosat['nbp'].timeseries,
        True
    ).ax
    ax = VisualLines(ax,time).inv_insitu(
        data.insitu['nbp'].timeseries,
        True
    ).ax
    plt.legend()
    plt.show()
    for model in models:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax = MonthlyPlot(ax).co2_flux().ax
        ax = VisualLines(ax,time).inv_sat(
            data.gosat['nbp'].timeseries,
            True
        ).ax
        ax = VisualLines(ax,time).inv_insitu(
            data.insitu['nbp'].timeseries,
            True
        ).ax
        ax.plot(data.trendy['nbp'].dates['range'], -data.trendy['nbp'].timeseries[model],
                label=model, color='k')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    pass

