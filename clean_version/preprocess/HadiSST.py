import xarray as xr
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
from settings import Pacific_range as Pr
import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre
import pre_trendy
import matplotlib.pyplot as plt
time1 = '1910-01-01'
time2 = '2022-12-31'
sst = xr.open_dataset('/home/mhuang/data/nontrendy/HadISST_sst_0_360.nc').sel(time=slice(time1,time2))
sst_modified = sst['sst']
# 使用 where 函数替换 -1000 为 -1.8，确保操作在 DataArray 上
sst_modified = sst_modified.where(sst_modified != -1000, -1.8)

# 将修改后的 DataArray 赋值回原来的 Dataset 中
sst['sst'] = sst_modified

sst2 = xr.open_dataset('/home/mhuang/data/nontrendy/sst.mon.mean.nc').sel(time=slice(time1,time2))
sst = sst.rename({'longitude': 'lon', 'latitude': 'lat', 'sst':'HadI'})
sst2 = sst2.rename({'sst':'COBE'})
sst = sst.assign_coords(lon=sst2['lon'].values)
sst = sst.assign_coords(lat=sst2['lat'].values)
sst = sst.assign_coords(time=sst2['time'].values)
sst_en = [
    sst,
    sst2
]
sst_en = xr.merge(sst_en)
sst_en.to_netcdf(os.path.join('/home/mhuang/data/trendy/v11', 'sst.nc'))
print(sst_en)


sst = xr.open_dataset(os.path.join('/home/mhuang/data/trendy/v11', 'sst.nc')).sel(
        lat=slice(Pr[0], Pr[1]),
        lon=slice(Pr[2], Pr[3])
    )
mean = sst.mean(dim=['lat','lon'])
fig = plt.figure(figsize=[12, 3])
ax = fig.add_subplot(111)
ax.plot(mean.time, mean.HadI)
ax.plot(mean.time, mean.COBE)
plt.show()

fig = plt.figure(figsize=[12, 3])
ax = fig.add_subplot(111)
ax.pcolormesh(sst.lon, sst.lat, sst.COBE[0,:,:])
plt.show()

fig = plt.figure(figsize=[12, 3])
ax = fig.add_subplot(111)
ax.pcolormesh(sst.lon, sst.lat, sst.HadI[0,:,:])
plt.show()