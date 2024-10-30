import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre

class NIRvGPPPreprocess:
    def __init__(self, settings):
        self.path = settings['PATH']
        self.out_path = settings['OUT_PATH']
        self.sif_file = os.path.join(self.path, settings['FNAME'])
        self.transcom_file = settings['TRANSCOM_FILE']
        self.start = settings['START_DATE']
        self.end = settings['END_DATE']

        self.gpp_regrid = None
        self.gpp = xr.open_mfdataset('/mnt/data2/users/mhuang/NIRvGPP/*/*.nc',combine='nested', concat_dim='time')
        self.trans = None
        self.ecos_regrid = None
        self.trans_regrid = None
    def give_time(self):
        start_date = self.start
        end_date = self.end
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
        # date_list = date_range.strftime('%Y-%m').tolist()
        date_list = pd.date_range(start=start_date,
                                  periods=len(date_range), freq='MS')
        self.gpp['time'] = date_list
        return self
    def coords_adjust(self):
        self.gpp = self.gpp.rename({'longitude': 'lon',
                                    'latitude': 'lat'})
        self.gpp = self.gpp.transpose('lon', 'lat', 'time')
        return self

    def regrid_data(self):
        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-90, 90, 1.0)),
                "lon": (["lon"], np.arange(-180, 180, 1.0)),
            }
        )
        regrider = xesmf.Regridder(self.gpp, target_grid, method='nearest_s2d', periodic=True)
        self.gpp_regrid = regrider(self.gpp)
        regrider = xesmf.Regridder(ecos, target_grid, method='nearest_s2d', periodic=True)
        self.ecos_regrid = regrider(ecos)
        return self

    def merge_save_data(self):
        self.trans = xr.open_dataset(self.transcom_file)
        ensemble  = [
            self.gpp_regrid,
            self.trans.transcom_regions,
            self.trans.land_ecosystems,
            self.trans.country_id,
            self.ecos_regrid
        ]
        ensemble = xr.merge(ensemble)
        ensemble.to_netcdf(os.path.join(os.path.join(self.out_path, 'nirv_based_gpp_rf_1x1.nc'))) # 'GOME_sif.nc'
        print(os.path.join(self.out_path, 'nirv_based_gpp_rf_1x1.nc'))
        return self

settings = input_pre.nirv_based_gpp
x=NIRvGPPPreprocess(settings).give_time().coords_adjust().regrid_data().merge_save_data()
print(x.gpp)