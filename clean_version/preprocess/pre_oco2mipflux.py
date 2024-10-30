import os
import numpy as np
import matplotlib.pyplot as plt
import xesmf
import cftime
import pandas as pd
import fnmatch
import subprocess
import xarray as xr
import input_pre
import nctoolkit as nc
import data_loader

def read_data(path, var, start_date, end_date, out_path):
    ds = []
    target_grid = xr.Dataset(
        {
            "lat": (["lat"], np.arange(-90, 90, 1.0)),
            "lon": (["lon"], np.arange(-180, 180, 1.0)),
        }
    )
    i = 0
    for root, dirs, files in os.walk(path):
        for fname in files:

            if fnmatch.fnmatch(fname, '*.nc4') and fname != 'EnsMean_gridded_fluxes_LNLGIS.nc4' and fname != 'EnsStd_gridded_fluxes_LNLGIS.nc4':
                target_path = os.path.join(root, fname)
                data = xr.open_dataset(target_path, engine='netcdf4', decode_times=True)
                data['time'] = pd.date_range(start=start_date,
                                                 end=end_date, freq='MS')
                #data_rename = data.rename({'n_months': 'time'})
                data_rename = data.rename({'latitude': 'lat', 'longitude': 'lon'})
                regrider = xesmf.Regridder(data_rename, target_grid, method='nearest_s2d', periodic=True)
                data_rename = regrider(data_rename)
                data_rename = xr.DataArray(data_rename.land, dims=['time', 'lat', 'lon'], name=(fname.split('_')[0]))
                ds.append(data_rename)
                print(fname)

            if fname == 'EnsMean_gridded_fluxes_LNLGIS.nc4' or fname == 'EnsStd_gridded_fluxes_LNLGIS.nc4':
                target_path = os.path.join(root, fname)
                data        = xr.open_dataset(target_path, engine='netcdf4', decode_times=True)
                data['n_months'] = pd.date_range(start=start_date,
                                                 end=end_date, freq='MS')
                data_rename = data.rename({'n_months': 'time'})
                data_rename = data_rename.rename({'latitude': 'lat', 'longitude': 'lon'})
                regrider = xesmf.Regridder(data_rename, target_grid, method='nearest_s2d', periodic=True)
                data_rename = regrider(data_rename)
                data_rename = xr.DataArray(data_rename.land, dims=['time', 'lat', 'lon'], name=(fname.split('_')[0]))
                ds.append(data_rename)
                print(fname)
    ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
    landsea = xr.open_dataset('/mnt/data/users/mhuang/IMERG_land_sea_mask.nc')
    trans_in = xr.open_dataset('/home/mhuang/data/regions_regrid.nc')
    regrider = xesmf.Regridder(trans_in, target_grid, method='nearest_s2d', periodic=True)
    trans_regrid = regrider(trans_in)
    print(trans_regrid)
    regrider = xesmf.Regridder(ecos, target_grid, method='nearest_s2d', periodic=True)
    ecos_regrid = regrider(ecos)
    print(ecos_regrid)
    regrider = xesmf.Regridder(landsea, target_grid, method='nearest_s2d', periodic=True)
    landsea_regrid = regrider(landsea)
    print(landsea_regrid)

    ds.append(trans_regrid)
    ds.append(ecos_regrid)
    ds.append(landsea_regrid)
    ds = xr.merge(ds)
    print(ds)
    ds.to_netcdf('/home/mhuang/data/trendy/v11/oco2mip_regrid.nc')

settings = input_pre.nbp
transcom_file   = settings['TRANSCOM_FILE']
start_date = "2015-01-01"
end_date = "2020-12-31"
path = '/mnt/data/users/eschoema/OCO-2_v10_MIP/LNLGIS'
read_data(path,1,start_date,end_date,1)