import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre
import rioxarray
import glob
from osgeo import gdal
def tif_to_nc(inpath,outpath):
    filepath = inpath
    file_paths = glob.glob(os.path.join(filepath,'*.tif'))
    output_dir = outpath
    for fp in file_paths:
        print(f"Reading file: {fp}")
        file_name = os.path.splitext(os.path.basename(fp))[0]
        output_path = os.path.join(output_dir, f"{file_name}.nc")
        print(output_path)
        gdal.Translate(output_path, fp, format='netCDF')
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
class PreGOSIF:
    def __init__(self,setting):
        self.target_grid = setting['TARGET_GRID']
        self.out_path    = setting['OUT_PATH']
        self.out_fname   = setting['OUT_FNAME']
        self.data        = xr.open_mfdataset(
            os.path.join(setting['NC_PATH'],'*.nc')
            , combine='nested', concat_dim='time'
        )

        start_date = '2000-03-01'
        end_date = '2023-12-31'
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
        date_list = date_range.strftime('%Y-%m').tolist()
        date_list = pd.date_range(start=start_date,
                                      periods=len(date_range), freq='MS')
        self.data['time'] = date_list
        self.data         = self.data.sel(time=slice(setting['START_DATE'],setting['END_DATE']))
        self.data = self.data.rename({'Band1':'GOSIF'})
        self.data = self.data.transpose('lon', 'lat', 'time')

        self.transcom_file = setting['TRANSCOM_FILE']
        self.data_regrid = None
    def to_nc(self):
        tif_to_nc(setting['TIF_PATH'], setting['NC_PATH'])
    def open_with_dim(self):
        self.data = xr.open_mfdataset(
            os.path.join(setting['TIMEDIM_PATH'], '*.nc')
            , combine='nested', concat_dim='time'
        )
        print(self.data.time)
        start_date = '2000-03-01'
        end_date = '2023-12-31'
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
        date_list = date_range.strftime('%Y-%m').tolist()
        print(len(date_list))
        date_list = pd.date_range(start=start_date,
                                  periods=len(date_range), freq='MS')
        self.data['time'] = date_list
        self.data = self.data.sel(time=slice(setting['START_DATE'], setting['END_DATE']))
        self.data = self.data.rename({'Band1': 'GOSIF'})
        self.data = self.data.transpose('lon', 'lat', 'time')
        return self
    def regrid_data(self):
        self.data_regrid = regrid(self.data)
        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        regrider = xesmf.Regridder(self.data, self.target_grid, method='nearest_s2d', periodic=True)
        self.data_regrid = regrider(self.data)
        regrider = xesmf.Regridder(ecos, self.target_grid, method='nearest_s2d', periodic=True)
        self.ecos_regrid = regrider(ecos)
        return self
    def merge_save_data(self):
        self.trans = xr.open_dataset(self.transcom_file)
        ensemble = [
            self.data_regrid,
            self.trans.transcom_regions,
            self.trans.land_ecosystems,
            self.trans.country_id,
            self.ecos_regrid
        ]
        ensemble = xr.merge(ensemble)
        ensemble.to_netcdf(os.path.join(os.path.join(self.out_path, self.out_fname)))  # 'GOME_sif.nc'
        print(os.path.join(self.out_path, self.out_fname))
        return self

if __name__ == '__main__':
    setting = input_pre.gosif
    PreGOSIF(setting=setting).open_with_dim().regrid_data().merge_save_data()