import os
import xarray as xr
import numpy as np
from statistical_analysis import asc_to_nc
from osgeo import gdal

path          = '/home/mhuang/data/trendy/v11'
asc           = 'FAO_soc.asc'
nc            = 'FAO_soc.nc'
asc_file      = os.path.join(path, asc)
nc_file       = os.path.join(path, nc)

# Use GDAL to open ASC file
dataset = gdal.Open(asc_file)
band = dataset.GetRasterBand(1)
data = band.ReadAsArray()

# Get geotransform parameters (xllcorner, yllcorner, cellsize)
transform = dataset.GetGeoTransform()

# Create a coordinate array based on the xllcorner and yllcorner and the cellsize
x_coords = np.arange(transform[0], transform[0] + (dataset.RasterXSize * transform[1]), transform[1])
y_coords = np.arange(transform[3], transform[3] + (dataset.RasterYSize * transform[5]), transform[5])

# Create an xarray Dataset and store the data
ds = xr.Dataset(
    {"data": (["y", "x"], data)},
    coords={
        "x": x_coords,
        "y": y_coords,
    },
)

# Save to NetCDF format
ds.to_netcdf(nc_file)

print(f"ASC file converted to NetCDF: {nc_file}")

