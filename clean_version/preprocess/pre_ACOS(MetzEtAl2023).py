from forplot import plot_station
import input_pre
import data_processor
import xarray as xr
import name_dic
import glob
import pandas as pd

datapath = '/mnt/data/users/eschoema'

def CreateDF(DS,DS2,DS3):
    d = {'CO2': DS.xco2.values,
         'CO2_error': DS.xco2_uncertainty.values,
         'lat':DS.latitude.values,
         'lon':DS.longitude.values,
         'Year':DS.date.values[:,0],
         'Month':DS.date.values[:,1],
         'Day':DS.date.values[:,2],
         'Hour':DS.date.values[:,3],
         'Min':DS.date.values[:,4],
         'Sec':DS.date.values[:,5],
         'CO2_uncorr': DS2.xco2_raw.values,
         'quality': DS.xco2_quality_flag.values,
         'glint': DS3.glint_angle.values,
         'land_frac': DS3.land_fraction,
         'DWS':DS2.dws.values,
         'delGrad':DS2.co2_grad_del.values,
         'psurf':DS2.psurf.values,
         'dpfrac':DS2.dpfrac.values,
         'albedo_sco2':DS2.albedo_sco2.values,
         'gain':DS3.gain.values}
    df = pd.DataFrame(data=d)

    return df

def createACOS(filepath, lonmin, lonmax, latmin, latmax):
    for num, filepath in enumerate(glob.glob(filepath + "/ACOS/ACOS_L2_Lite_FP.9r/*.nc4")):
        DS = xr.open_mfdataset(filepath,combine='by_coords',use_cftime=None)
        DS2 = xr.open_mfdataset(filepath,group = 'Retrieval',combine='by_coords',use_cftime=None)
        DS3 = xr.open_mfdataset(filepath,group = 'Sounding',combine='by_coords',use_cftime=None)

        if num == 0:
            # create Dataframe
            df3 = CreateDF(DS, DS2, DS3)
            df = df3[(df3.lon >= lonmin)
                     & (df3.lon <= lonmax)
                     & (df3.lat >= latmin)
                     & (df3.lat <= latmax)]
        else:
            # create Dataframe
            df3 = CreateDF(DS, DS2, DS3)
            df2 = df3[(df3.lon >= lonmin)
                      & (df3.lon <= lonmax)
                      & (df3.lat >= latmin)
                      & (df3.lat <= latmax)]
            df = pd.concat([df, df2], ignore_index=True)


    print("finished reading data")
    print(df)
    df.to_csv(path_or_buf='/home/mhuang/data/trendy/v11/acos_NAf.csv', index=False, header=True)

class ProcessACOS:
    def __init__(self, setting, region):
        self.path = setting['path']
        self.lonmin = name_dic.transcom[region]['lon_min']
        self.lonmax = name_dic.transcom[region]['lon_max']
        self.latmin = name_dic.transcom[region]['lat_min']
        self.latmax = name_dic.transcom[region]['lat_max']
    def process(self):
        createACOS(self.path, self.lonmin, self.lonmax, self.latmin, self.latmax)

setting = input_pre.co2con
ProcessACOS(setting, 'Northern Africa').process()