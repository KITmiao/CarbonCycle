import os
import glob
import xesmf
import numpy as np
import xarray as xr
from osgeo import gdal
from statistical_analysis import tif_to_nc
"""
path     = '/home/mhuang/data/trendy/v11'
tif_file = 'soc_0-5cm_mean_5000.tif'
nc_file  = 'soc_0-5cm_mean_5000.nc'
tif      = os.path.join(path, tif_file)
nc       = os.path.join(path, nc_file)
tif_to_nc(tif, nc)
path     = '/home/mhuang/data/trendy/v11'
tif_file = 'soc_15-30cm_mean_5000.tif'
nc_file  = 'soc_15-30cm_mean_5000.nc'
tif      = os.path.join(path, tif_file)
nc       = os.path.join(path, nc_file)
tif_to_nc(tif, nc)
path     = '/home/mhuang/data/trendy/v11'
tif_file = 'soc_30-60cm_mean_5000.tif'
nc_file  = 'soc_30-60cm_mean_5000.nc'
tif      = os.path.join(path, tif_file)
nc       = os.path.join(path, nc_file)
tif_to_nc(tif, nc)
path     = '/home/mhuang/data/trendy/v11'
tif_file = 'soc_60-100cm_mean_5000.tif'
nc_file  = 'soc_60-100cm_mean_5000.nc'
tif      = os.path.join(path, tif_file)
nc       = os.path.join(path, nc_file)
tif_to_nc(tif, nc)"""
def regrid(ds):
    grid = xr.Dataset(
        {
            "lat": (["lat"], np.arange(-90, 90, 1.0)),
            "lon": (["lon"], np.arange(-180, 180, 1.0)),
        }
    )
    regrider = xesmf.Regridder(ds, grid, method='bilinear', periodic=False)
    ds = regrider(ds)
    return ds
def change_coords(ds, xaxis, yaxis):
    x = ds[xaxis].values
    y = ds[yaxis].values
    ds.coords['lon'] = (xaxis, x)
    ds.coords['lat'] = (yaxis, y)
    return ds
soc1 = xr.open_dataset('/home/mhuang/data/trendy/v11/soc_0-5cm_mean_5000.nc')
soc1 = change_coords(soc1, 'x', 'y')
soc1 = regrid(soc1)
print('ok')
soc1.to_netcdf('/home/mhuang/data/trendy/v11/soc_0-5cm_mean_1x1.nc')
soc2 = xr.open_dataset('/home/mhuang/data/trendy/v11/soc_15-30cm_mean_5000.nc')
soc2 = regrid(soc2)
soc2.to_netcdf('/home/mhuang/data/trendy/v11/soc_15-30cm_mean_1x1.nc')
soc3 = xr.open_dataset('/home/mhuang/data/trendy/v11/soc_30-60cm_mean_5000.nc')
soc3 = regrid(soc3)
soc3.to_netcdf('/home/mhuang/data/trendy/v11/soc_30-60cm_mean_1x1.nc')
soc4 = xr.open_dataset('/home/mhuang/data/trendy/v11/soc_60-100cm_mean_5000.nc')
soc4 = regrid(soc4)
soc4.to_netcdf('/home/mhuang/data/trendy/v11/soc_60-100cm_mean_1x1.nc')