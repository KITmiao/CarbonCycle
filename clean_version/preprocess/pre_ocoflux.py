import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre
import pre_trendy
import matplotlib.pyplot as plt

class TM5GosatPreprocess:
    def __init__(self, settings):
        self.path            = settings['OCO']
        self.out_path        = os.path.join(self.path, settings['OUT_PATH'])
        self.transcom_file   = settings['TRANSCOM_FILE']
        self.start           = settings['START_DATE']
        self.end             = settings['END_DATE']

        self.trans_regrid    = None
        self.oco              = None
        self.oco_nbp          = None
        self.ecos_regrid     = None
        self.landsea_regrid  = None
    def regrid_data(self):
        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        landsea = xr.open_dataset('/mnt/data/users/mhuang/IMERG_land_sea_mask.nc')
        target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-90, 90, 1.0)),
                "lon": (["lon"], np.arange(-180, 180, 1.0)),
            }
        )
        trans_in = xr.open_dataset(self.transcom_file)
        regrider = xesmf.Regridder(trans_in, target_grid, method='nearest_s2d', periodic=True)
        self.trans_regrid = regrider(trans_in)
        regrider = xesmf.Regridder(ecos, target_grid, method='nearest_s2d', periodic=True)
        self.ecos_regrid = regrider(ecos)
        regrider = xesmf.Regridder(landsea, target_grid, method='nearest_s2d', periodic=True)
        self.landsea_regrid = regrider(landsea)
        return self

    def get_nbp(self):
        self.oco    = xr.open_dataset(self.path)
        self.oco_nbp    = self.oco.CO2_flux_nbe
        start_date           = '2014-09-01'
        end_date             = '2021-03-31'
        date_range           = pd.date_range(start=start_date, end=end_date, freq='MS')
        #date_range = pd.date_range(start=start_date, periods=126, freq='MS')
        date_list            = date_range.strftime('%Y-%m-%d').tolist()
        self.oco_nbp = xr.DataArray(self.oco_nbp, dims=['months', 'latitude', 'longitude'], name='OCO')
        self.oco_nbp['months']   = date_range
        #print(self.rt_nbp['months'])
        self.oco_nbp = self.oco_nbp.rename({
            'months': 'time',
            'latitude': 'lat',
            'longitude': 'lon'
        })
        self.oco_nbp = self.oco_nbp.sel(time=slice(self.start, self.end))
        ensemble = [self.oco_nbp,
                    self.trans_regrid.transcom_regions,
                    self.trans_regrid.land_ecosystems,
                    self.trans_regrid.country_id,
                    self.ecos_regrid,
                    self.landsea_regrid]
        ensemble = xr.merge(ensemble)

        ensemble.to_netcdf(os.path.join(self.out_path, 'OCO_nbp.nc'))
        print(os.path.join(self.out_path, 'OCO_nbp.nc'))

if __name__ == '__main__':
    setting = input_pre.nbp
    x = TM5GosatPreprocess(setting).regrid_data()
    y = x.get_nbp()