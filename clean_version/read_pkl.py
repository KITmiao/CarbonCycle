import os
import input
import dill as pickle
"""from data_processor import (
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
    ProcessAll
)"""
from settings import setting
from settings import path
print(__name__)
if __name__ == 'read_pkl' or __name__ == 'read_pkl':
    region = setting['region'].replace(" ", "_")
    fname = os.path.join(path, region + ".pkl")
    with open(fname, "rb") as file:
        data = pickle.load(file)
    from settings import setting_region2
    if setting_region2:
        region = setting_region2['region'].replace(" ", "_")
        fname = os.path.join(path, region + ".pkl")
        with open(fname, "rb") as file:
            data2 = pickle.load(file)

    from settings import setting_region3
    if setting_region3:
        region = setting_region3['region'].replace(" ", "_")
        fname = os.path.join(path, region + ".pkl")
        with open(fname, "rb") as file:
            data3 = pickle.load(file)