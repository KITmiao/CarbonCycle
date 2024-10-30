import os, glob
import xarray as xr
import data_loader
import numpy as np
import xesmf
import dask
import input
import name_dic
import pandas as pd
import input_pre
from datetime import datetime

class TM5Preprocessing:
    def __init__(self, settings):
        self.path = settings['PATH_TO_TM5']
        self.tm5 = None

    def preprocess(self):
        data   = []
        years  = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        for year in years:
            for month in months:
                var = xr.open_mfdataset(os.path.join(self.path, year, month, '*.nc4'), group='glb300x200',
                                         concat_dim='None', combine='nested')
                ds  = xr.open_mfdataset(os.path.join(self.path, year, month, '*.nc4'),
                                         concat_dim='None', combine='nested')
                at = ds.at.values
                bt = ds.bt.values
                for i in range(len(var['None'])):
                    for j in range(len(var['times'])):
                        psurf = var['pressure'][i, j, :, :].values
                        for k in range(len(var['levels'])):
                            p = np.ones([90, 120]) * (at[i, k] - at[i, k + 1]) + psurf * (bt[i, k] - bt[i, k + 1])
                            la = np.array(p * var.mix[i, 0, j, k, :, :].values)
                            la = la[np.newaxis, ...]
                            if k == 0:
                                mix = la
                            if k != 0:
                                mix = np.append(mix, la, axis=0)
                        co2a = np.sum(mix, axis=0) / (
                                    (psurf * (bt[i, 0] - bt[i, -1])) + (np.ones((90, 120)) * (at[i, 0] - at[i, -1])))
                        if i == 0 and j == 0:
                            xco2 = co2a[np.newaxis, ...]
                        else:
                            xco2 = np.append(xco2, co2a[np.newaxis, ...], axis=0)

                xco2 = np.mean(xco2, axis=0)
                #var = var.mean(dim='levels')
                var = var.mean(dim='None')
                var = var.mean(dim='times')
                var = var.sel(levels=0)
                time= year+'-'+month
                time_date = datetime.strptime(time, '%Y-%m')
                print(time)
                var['tracer'] = time_date
                var['mix'][0,:,:] = np.zeros([90,120])
                var['mix'][0, :, :] = xco2
                """
                target_grid = xr.Dataset(
                    {
                        "lat": (["lat"], np.arange(-90, 90, 1.0)),
                        "lon": (["lon"], np.arange(-180, 180, 1.0)),
                    }
                )
                """
                target_grid = xr.Dataset(
                    {
                        "lat": (["lat"], np.arange(-89.75, 89.75+0.5, 0.5)),
                        "lon": (["lon"], np.arange(-179.75, 179.75+0.5, 0.5)),
                    }
                )
                regrider = xesmf.Regridder(var, target_grid, method='nearest_s2d', periodic=True)
                var = regrider(var)
                var['tracer'] = time_date
                var = var.rename({'tracers': 'time'})
                print(var.mix)
                var.to_netcdf(os.path.join('/home/mhuang/data/nontrendy/TM505x05', time+'.nc'))
        #time = data_loader.create_date('2009-01','2018-12-31')

setting = input_pre.co2con
TM5Preprocessing(setting).preprocess()


