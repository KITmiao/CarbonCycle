import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre

class SIFPreprocess:
    def __init__(self, settings):
        self.path = settings['PATH_TO_SIF']
        self.out_path = settings['OUT_PATH']
        self.sif_file = os.path.join(self.path, settings['FNAME'])
        self.transcom_file = settings['TRANSCOM_FILE']
        self.start = settings['START_DATE']
        self.end = settings['END_DATE']
        self.outfile = settings['OUT_FNAME']

        self.sif_regrid = None
        self.sif = None
        self.trans = None
        self.ecos_regrid = None
        self.trans_regrid = None
        self.n  = None
    def monmean(self):
        self.sif = xr.open_mfdataset(os.path.join(self.path, '*.nc'))
        self.n   = self.sif.resample(DATE='1MS').count(dim='DATE')
        self.sif = self.sif.resample(DATE='1MS').mean(dim='DATE', skipna=True)
        self.sif = self.sif.rename({'LON': 'lon',
                                    'LAT': 'lat',
                                    'DATE': 'time',
                                    'SIF': 'GOME'})
        self.n = self.n.rename({'LON': 'lon',
                                    'LAT': 'lat',
                                    'DATE': 'time',
                                    'SIF': 'n'})
        self.sif = self.sif.sel(time=slice(self.start, self.end))
        self.n = self.n.sel(time=slice(self.start, self.end))
        start_date = self.start
        end_date = '2018-12-01'  # '2018-12-01'
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
        # date_list = date_range.strftime('%Y-%m').tolist()
        date_list = pd.date_range(start=start_date,
                                  periods=len(date_range), freq='MS')

        self.sif['time'] = date_list
        self.n['time'] = date_list
        return self
    def regrid_data(self):

        self.sif = xr.open_dataset(self.sif_file)

        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        print(self.sif['time'])
        target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-90, 90, 1.0)),
                "lon": (["lon"], np.arange(-180, 180, 1.0)),
            }
        )
        regrider = xesmf.Regridder(self.sif, target_grid, method='nearest_s2d', periodic=True)
        self.sif_regrid = regrider(self.sif)
        regrider = xesmf.Regridder(ecos, target_grid, method='nearest_s2d', periodic=True)
        self.ecos_regrid = regrider(ecos)
        #self.sif_regrid.to_netcdf(os.path.join(self.out_path, 'GOME_sif.nc'))
        return self

    def merge_save_data(self):
        self.trans = xr.open_dataset(self.transcom_file)
        ensemble  = [
            self.sif_regrid,
            self.trans.transcom_regions,
            self.trans.land_ecosystems,
            self.trans.country_id,
            self.ecos_regrid
        ]
        ensemble = xr.merge(ensemble)
        ensemble.to_netcdf(os.path.join(os.path.join(self.out_path, self.outfile))) # 'GOME_sif.nc'
        print(os.path.join(self.out_path, self.outfile))
        return self

    def merge_save_unregrid_data(self):
        self.trans = xr.open_dataset(self.transcom_file)
        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-89.75, 89.75, 0.5)),
                "lon": (["lon"], np.arange(-179.75, 179.75, 0.5)),
            }
        )
        regrider = xesmf.Regridder(ecos, target_grid, method='nearest_s2d', periodic=True)
        self.ecos_regrid = regrider(ecos)
        regrider = xesmf.Regridder(self.trans, target_grid, method='nearest_s2d', periodic=True)
        self.trans_regrid = regrider(self.trans)
        ensemble = [self.sif,
                    self.n,
                    self.ecos_regrid,
                    self.trans_regrid.transcom_regions]
        ensemble = xr.merge(ensemble)
        ensemble.to_netcdf(os.path.join(os.path.join(self.out_path, 'GOME_sif_0.5x0.5.nc')))
        print(os.path.join(self.out_path, 'GOME_sif_0.5x0.5.nc'))
        return self

if __name__ == '__main__':
    settings = input_pre.sif
    #SIFPreprocess(settings).monmean().regrid_data().merge_save_data()
    #SIFPreprocess(settings).monmean().merge_save_unregrid_data()
    settings = input_pre.sif_based_gpp
    SIFPreprocess(settings).regrid_data().merge_save_data()
"""
if __name__ == 'pre_gome_sif':
    settings = input_pre.sif
    SIFPreprocess(settings).regrid_data().merge_save_data()
"""