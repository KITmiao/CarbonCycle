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

data = xr.open_dataset('/home/mhuang/data/nontrendy/CT2022.nc')
target_grid = xr.Dataset(
                    {
                        "lat": (["lat"], np.arange(-90, 90, 1.0)),
                        "lon": (["lon"], np.arange(-180, 180, 1.0)),
                    }
                )
regrider = xesmf.Regridder(data, target_grid, method='nearest_s2d', periodic=True)
co2 = regrider(data)
co2.to_netcdf('/home/mhuang/data/nontrendy/CT2022_regrid.nc')