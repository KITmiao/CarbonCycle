import os, glob
import xarray as xr
import numpy as np
import xesmf
import dask
import input
import name_dic
import pandas as pd
import input_pre
import pandas as pd


def CreateDF(DS, DS2, DS3):
    d = {'CO2': DS.xco2.values,
         'CO2_error': DS.xco2_uncertainty.values,
         'lat': DS.latitude.values,
         'lon': DS.longitude.values,
         'Year': DS.date.values[:, 0],
         'Month': DS.date.values[:, 1],
         'Day': DS.date.values[:, 2],
         'Hour': DS.date.values[:, 3],
         'Min': DS.date.values[:, 4],
         'Sec': DS.date.values[:, 5],
         'CO2_uncorr': DS2.xco2_raw.values,
         'quality': DS.xco2_quality_flag.values,
         'glint': DS3.glint_angle.values,
         'land_frac': DS3.land_fraction,
         'DWS': DS2.dws.values,
         'delGrad': DS2.co2_grad_del.values,
         'psurf': DS2.psurf.values,
         'dpfrac': DS2.dpfrac.values,
         'albedo_sco2': DS2.albedo_sco2.values,
         'gain': DS3.gain.values}
    df = pd.DataFrame(data=d)


class ACOSPreprocess:
    def __init__(self, settings1, settings2):
        self.in_path = settings1['PATH_TO_ACOS']
        self.out_path = settings1['OUT_PATH']
        self.lon_min  = name_dic.transcom[settings2['region']]['lon_min']
        self.lon_max = name_dic.transcom[settings2['region']]['lon_max']
        self.lat_min = name_dic.transcom[settings2['region']]['lat_min']
        self.lat_max = name_dic.transcom[settings2['region']]['lat_max']
        #self.trans_file = settings['TRANSCOM_FILE']

    def CreateDataFrameACOS(self):
        file_paths = [os.path.join(self.in_path, filename) for filename in os.listdir(self.in_path) if
                      filename.endswith('.nc4')]

        datasets = []
        last_sounding_id = 0

        for path in file_paths:
            print(path)
            ds = xr.open_dataset(path, chunks={'sounding_id': 'auto'})
            ds = ds.where((ds.longitude >= self.lon_min)
            & (ds.longitude <= self.lon_max)
            & (ds.latitude >= self.lat_min)
            & (ds.latitude <= self.lat_max))

            # Adjust 'sounding_id' to avoid conflicts
            ds['sounding_id'] = ds['sounding_id'] + last_sounding_id
            last_sounding_id = ds['sounding_id'][-1]

            datasets.append(ds)
        # Save the merged dataset to a new NetCDF4 file
        print('concating')
        with dask.config.set(scheduler='threads'):  # Use the threaded scheduler for parallelism
            concatenated = xr.concat(datasets, dim='sounding_id', join='outer')
        print(concatenated)
        d = {'CO2': concatenated.xco2.values,
             'CO2_error': concatenated.xco2_uncertainty.values,
             'Lat': concatenated.latitude.values,
             'Long': concatenated.longitude.values,
             'Year': concatenated.date.values[:, 0],
             'Month': concatenated.date.values[:, 1],
             'Day': concatenated.date.values[:, 2]}
        df = pd.DataFrame(data=d)
        df.to_csv(self.out_path+'/acos.csv')
"""
        print('saving')
        concatenated.to_netcdf(self.out_path+'/acos.nc4')
        # Close the datasets
        for ds in datasets:
            ds.close()
"""
setting1 = input_pre.co2con
setting2 = input.setting
ACOSPreprocess(setting1, setting2).CreateDataFrameACOS()