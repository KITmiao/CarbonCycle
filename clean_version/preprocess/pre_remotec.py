import os, glob
import xarray as xr
import numpy as np
import xesmf
import dask
import input
import name_dic
import pandas as pd
import input_pre

def CreateDF(DS):
    d = {'CO2': DS.xco2.values,
         'CO2_prior': DS.co2_column_apriori.values,
         'lat':DS.latitude.values,
         'lon':DS.longitude.values,
         'Year':DS.year.values,
         'Month':DS.month.values,
         'Day':DS.day.values,
         'Hour':DS.hour.values,
         'Min':DS.minute.values,
         'Sec':DS.second.values,
         'land_flag':DS.flag_landtype.values,
         'gain':[x.decode('UTF-8') for x in DS.gain.values]
         }
    df = pd.DataFrame(data=d)

    return df

def createRemoTeC(filepath, lonmin, lonmax, latmin, latmax):
    for num, filepath in enumerate(glob.glob(filepath + "/GOSAT/NetCDF_files_withCH4/*.nc")):
        DS = xr.open_mfdataset(filepath,combine='by_coords',use_cftime=None)

        if num == 0:
            # create Dataframe
            df3 = CreateDF(DS)
            df = df3[(df3.lon >= lonmin)
                     & (df3.lon <= lonmax)
                     & (df3.lat >= latmin)
                     & (df3.lat <= latmax)]
        else:
            # create Dataframe
            df3 = CreateDF(DS)
            df2 = df3[(df3.lon >= lonmin)
                      & (df3.lon <= lonmax)
                      & (df3.lat >= latmin)
                      & (df3.lat <= latmax)]
            df = pd.concat([df, df2], ignore_index=True)


    print("finished reading data")
    print(df)
    df.to_csv(path_or_buf='/home/mhuang/data/trendy/v11/remotec_NAf.csv', index=False, header=True)

class ProcessRemoTeC:
    def __init__(self, setting, region):
        self.path = setting['path']
        self.lonmin = name_dic.transcom[region]['lon_min']
        self.lonmax = name_dic.transcom[region]['lon_max']
        self.latmin = name_dic.transcom[region]['lat_min']
        self.latmax = name_dic.transcom[region]['lat_max']
    def process(self):
        createRemoTeC(self.path, self.lonmin, self.lonmax, self.latmin, self.latmax)

setting = input_pre.co2con
ProcessRemoTeC(setting, 'Northern Africa').process()