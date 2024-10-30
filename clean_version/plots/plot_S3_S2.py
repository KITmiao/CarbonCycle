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
def check_model(model):
    luc = data.trendy['fLuc'].timeseries[model]
    cls = -S3nbp[model] + S2nbp[model]
    fig, ax = plt.subplots(figsize=(10, 3))
    ax = MonthlyPlot(ax).co2_flux().ax
    ax.plot(time, cls, label='S3 NBP -S2 NBP')
    ax.plot(time, luc, label='fLuc', linestyle='--')
    ax.set_title(model)
    ax.legend()
    plt.show()
    fig, ax = plt.subplots(figsize=(10, 3))
    ax = MonthlyPlot(ax).co2_flux().ax
    ax.plot(time, -S3nbp[model], label='S3 NBP')
    ax.plot(time, -S2nbp[model], label='S2 NBP')
    ax.set_title(model)
    ax.legend()
    plt.show()
if __name__.split('.')[-1] == 'plot_S3_S2':
    pass
if __name__ == '__main__':
    S2set = {
    'region': 'Northern Africa',
    'good_models':['CABLE-POP','ISAM','ISBA-CTRIP','JULES','JSBACH','LPJ','LPX-Bern','ORCHIDEE','SDGVM'],
    'ok_models':['CLASSIC','DLEM','IBIS','YIBs','OCN'],
    'start_date':'2009-01-01',
    'end_date':'2018-12-31',
    'year':['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'],
    'path':'/home/mhuang/data/trendy/v11',
    'nbp':'nbpS2__ensemble.nc',
    }
    time  = data.gosat['nbp'].dates['range']
    S2nbp = ProcessTRENDY(S2set, 'nbp').timeseries
    S3nbp = data.trendy['nbp'].timeseries
    check_model('CLASSIC')
    check_model('CABLE-POP')
    check_model('OCN')
    check_model('CLM5.0')
    check_model('JSBACH')
    check_model('SDGVM')
    check_model('ORCHIDEE')

