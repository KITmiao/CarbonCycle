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
if __name__ == 'plot_trendy_nbp_compo' or __name__ == 'plots.plot_trendy_nbp_compo':
    from settings import trendy_models as models
    time    = data.gosat['nbp'].dates['range']
    nbp     = -data.trendy['nbp'].timeseries
    gpp     = data.trendy['gpp'].timeseries
    fLuc    = data.trendy['fLuc'].timeseries.fillna(0)
    fFire   = data.trendy['fFire'].timeseries.fillna(0)
    ra      = data.trendy['ra'].timeseries
    rh      = data.trendy['rh'].timeseries
    print(fLuc.keys())
    for model in models:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax = MonthlyPlot(ax).co2_flux().ax
        nee = gpp - ra - rh - fFire - fLuc
        ax.plot(data.trendy['nbp'].dates['range'], fLuc[model],
                label=model + ' fLuc', color='purple')
        """
        ax.plot(data.trendy['nbp'].dates['range'], fFire[model],
                label=model + ' fFire', color='r')
        """
        ax.plot(data.trendy['nbp'].dates['range'], nbp[model] + nee[model],
                label=model + ' dif', color='k')
        """
        ax.plot(data.trendy['nbp'].dates['range'], nbp[model],
                label=model+'NBP', color='k')
        ax.plot(data.trendy['nbp'].dates['range'], -nee[model],
                label='GPP-TER-fDisturb', color='r', linestyle='--')"""
        plt.legend()
        plt.show()

if __name__ == '__main__':
    pass