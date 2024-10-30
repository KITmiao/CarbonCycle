import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre

class PreprocessLAI:
    def __init__(self, settings):
        self.path = settings['PATH_TO_MODIS']
        self.path_evi = settings['PATH_TO_MODIS_EVI']
        self.out_path = settings['OUT_PATH']
        self.transcom_file = settings['TRANSCOM_FILE']
        self.start = settings['START_DATE']
        self.end = settings['END_DATE']

        self.lai_regrid = None
        self.lai = None
        self.evi_regrid = None
        self.evi = None
        self.trans = None
        self.ecos_regrid = None

        self.fpar = None
        self.ndvi = None
        self.ndvi_regrid = None


    def read_data(self):
        print('reading MODIS...')
        pattern = os.path.join(self.path, '**/*.nc')
        self.lai = xr.open_mfdataset(pattern, combine='nested', concat_dim='time', engine='netcdf4')
        self.lai = self.lai.sel(time=slice(self.start, self.end))
        self.lai = self.lai.resample(time='1M').mean(dim='time')

        date_range = pd.date_range(start=self.start, end=self.end, freq='MS')
        date_list = date_range.strftime('%Y-%m').tolist()
        self.lai['time'] = date_range
        self.fpar = xr.Dataset({
                'fpar': self.lai.fpar,
                'lai': self.lai.lai
                            })

        print(self.fpar)

        pattern = os.path.join(self.path_evi, '**/*.nc')
        self.evi = xr.open_mfdataset(pattern, combine='nested', concat_dim='time', engine='netcdf4')
        self.evi = self.evi.sel(time=slice(self.start, self.end))
        self.evi = self.evi.resample(time='1M').mean(dim='time')

        self.evi['time'] = date_range
        self.ndvi = xr.Dataset({
            'ndvi': self.evi.ndvi,
            'evi': self.evi.evi
        })

        print(self.ndvi)
        return self

    def regrid_data(self):
        print('regriding MODIS...')
        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-90, 90, 1.0)),
                "lon": (["lon"], np.arange(-180, 180, 1.0)),
            }
        )
        """
        target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-90, 90, 2.0)),
                "lon": (["lon"], np.arange(-180, 180, 3.0)),
            }
        )
        """
        regrider = xesmf.Regridder(self.lai, target_grid, method='nearest_s2d', periodic=True)
        self.lai_regrid = regrider(self.lai)
        regrider = xesmf.Regridder(self.evi, target_grid, method='nearest_s2d', periodic=True)
        self.evi_regrid = regrider(self.evi)
        trans_in = xr.open_dataset(self.transcom_file)
        regrider = xesmf.Regridder(trans_in, target_grid, method='nearest_s2d', periodic=True)
        self.trans_regrid = regrider(trans_in)
        regrider = xesmf.Regridder(ecos, target_grid, method='nearest_s2d', periodic=True)
        self.ecos_regrid = regrider(ecos)
        return self

    def merge_data(self):
        print('merging MODIS...')
        #self.trans = xr.open_dataset(self.transcom_file)
        ensemble = [
            self.lai_regrid,
            self.evi_regrid,
            self.trans_regrid.transcom_regions,
            self.trans_regrid.land_ecosystems,
            self.trans_regrid.country_id,
            self.ecos_regrid
        ]
        ensemble = xr.merge(ensemble)
        ensemble.to_netcdf(os.path.join(os.path.join(self.out_path, 'MODIS_lai.nc')))
        print(os.path.join(self.out_path, 'MODIS_lai.nc'))
        return self

    def merge_unregrid_data(self):
        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-89.75, 89.75, 0.5)),
                "lon": (["lon"], np.arange(-179.75, 179.75, 0.5)),
            }
        )
        print('regridding eco_type...')
        regrider = xesmf.Regridder(ecos, target_grid, method='nearest_s2d', periodic=True)
        self.ecos_regrid = regrider(ecos)
        regrider = xesmf.Regridder(self.ndvi, target_grid, method='nearest_s2d', periodic=True)
        self.ndvi_regrid = regrider(self.ndvi)
        ensemble = [
            self.fpar,
            self.ndvi_regrid,
            self.ecos_regrid
        ]
        print('merging MODIS...')
        ensemble = xr.merge(ensemble)
        print('saving MODIS...')
        ensemble.to_netcdf(os.path.join(os.path.join(self.out_path, 'MODIS_lai_0.5x0.5.nc')))
        print(os.path.join(self.out_path, 'MODIS_lai_0.5x0.5.nc'))
        return self

if __name__ == '__main__':
    setting = input_pre.lai
    #Pre = PreprocessLAI(setting).read_data().regrid_data().merge_data()
    Pre = PreprocessLAI(setting).read_data().merge_unregrid_data()
    #print(Pre.lai_regrid.time)
