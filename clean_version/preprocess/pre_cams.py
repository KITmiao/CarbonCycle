import os.path
import pandas as pd
import xarray as xr
import input_pre
import xarray as xr
import numpy as np
from datetime import datetime
import input_pre
import xesmf


class CAMSPreprocessing:
    def __init__(self, setting):
        self.path = setting['PATH_TO_CAMS']
        self.out_path = setting['OUT_PATH']
        self.cams = None
        self.xco2 = []
    def read_data(self):
        self.cams = xr.open_mfdataset(self.path + '/cams73_v21r1_co2_col_surface*.nc', combine='nested', concat_dim='time')
        for yr, yr_v in self.cams.groupby('time.year'):
            for mn, mn_v in yr_v.groupby('time.month'):
                xco2 = mn_v.XCO2.mean(dim='time', skipna=True)
                time = str(yr) + '-' + str(f"{int(mn):02d}")
                time_coord = pd.to_datetime([time])
                co2 = xco2.expand_dims({'time':time_coord})


                target_grid = xr.Dataset(
                    {
                        "lat": (["lat"], np.arange(-90, 90, 1.0)),
                        "lon": (["lon"], np.arange(-180, 180, 1.0)),
                    }
                )
                regrider = xesmf.Regridder(co2, target_grid, method='nearest_s2d', periodic=True)
                co2 = regrider(co2)
                print(co2)
                co2.name = 'XCO2'
                co2.to_netcdf(os.path.join('/home/mhuang/data/nontrendy/CAMS', time+'.nc'))
                print(time)


        return self

setting = input_pre.co2con
x=CAMSPreprocessing(setting).read_data()
print(x.xco2)
