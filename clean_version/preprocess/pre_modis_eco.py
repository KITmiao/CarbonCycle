import xarray as xr
import h5py
import os
import numpy as np
import matplotlib.pyplot as plt

path = '/mnt/data/users/eschoema/LandCover/MODIS_MCD12Q1'
file = 'MCD12C1.A2015001.061.2022166123617_Majority_Land_Cover_Type_3.nc'
fname=os.path.join(path,file)
print(fname)
data=xr.open_dataset(fname)
print(data['__xarray_dataarray_variable__'])
lat = np.arange(-90, 90, 0.05)
lon = np.arange(-180, 180, 0.05)
data['dim_1'] = lon
data['dim_0'] = -lat
#data['__xarray_dataarray_variable__'] = np.flip(data['__xarray_dataarray_variable__'], axis=1)
data = data.rename({
            'dim_0': 'lat',
            'dim_1': 'lon',
            '__xarray_dataarray_variable__': 'eco_type'
        })
print(data)
data = data.reindex(lat=list(reversed(data.lat)))
plt.pcolormesh(data['lon'], data['lat'], data['eco_type'])
plt.show()
data.to_netcdf('/home/mhuang/data/otherdata/modis_ecotype.nc')