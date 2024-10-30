import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre
import rioxarray
import glob
from osgeo import gdal

def regrid(ds):
    grid = xr.Dataset(
        {
            "lat": (["lat"], np.arange(-90, 90, 1.0)),
            "lon": (["lon"], np.arange(-180, 180, 1.0)),
        }
    )
    regrider = xesmf.Regridder(ds, grid, method='nearest_s2d', periodic=True)
    ds = regrider(ds)
    return ds
class PreSatEstFlux:
    def __init__(self,setting):
        self.infile = setting['IN_FILE']
        self.oufile = setting['OUT_FILE']
        self.transcom_file = setting['TRANSCOM_FILE']
        self.indata  = xr.open_dataset(self.infile)
    def regrid_data(self):
        self.oudata = regrid(self.indata)
        self.trans = xr.open_dataset(self.transcom_file)
        ensemble = [
            self.oudata,
            self.trans.transcom_regions,
        ]
        ensemble = xr.merge(ensemble)
        ensemble.to_netcdf(self.oufile)
        print(self.oufile)
        return self
setting = input_pre.Koning2019
PreSatEstFlux(setting).regrid_data()
