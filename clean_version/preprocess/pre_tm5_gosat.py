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
        self.path            = settings['PATH_TO_GOSAT_IS']
        self.rt_file         = os.path.join(self.path, settings['REMOTEC'])
        self.acos_file       = os.path.join(self.path, settings['ACOS'])
        self.prior_file      = os.path.join(self.path, settings['PRIOR'])
        self.out_path        = os.path.join(self.path, settings['OUT_PATH'])
        self.transcom_file   = settings['TRANSCOM_FILE']
        self.start           = settings['START_DATE']
        self.end             = settings['END_DATE']

        self.trans_regrid    = None
        self.rt              = None
        self.rt_nbp          = None
        self.acos            = None
        self.acos_nbp        = None
        self.prior           = None
        self.prior_nbp       = None
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
        self.rt    = xr.open_dataset(self.rt_file)
        self.acos  = xr.open_dataset(self.acos_file)
        self.prior = xr.open_dataset(self.prior_file)

        self.rt_nbp    = self.rt.CO2_flux_nee + self.rt.CO2_flux_fire
        self.acos_nbp  = self.acos.CO2_flux_nee + self.acos.CO2_flux_fire
        self.prior_nbp = self.prior.CO2_flux_nee + self.prior.CO2_flux_fire

        start_date           = '2009-01-01'
        end_date             = '2019-06-01'
        date_range           = pd.date_range(start=start_date, end=end_date, freq='MS')
        #date_range = pd.date_range(start=start_date, periods=126, freq='MS')
        date_list            = date_range.strftime('%Y-%m-%d').tolist()
        self.rt_nbp = xr.DataArray(self.rt_nbp, dims=['months', 'latitude', 'longitude'], name='RemoTeC')
        self.rt_nbp['months']   = date_range
        #print(self.rt_nbp['months'])
        self.rt_nbp = self.rt_nbp.rename({
            'months': 'time',
            'latitude': 'lat',
            'longitude': 'lon'
        })
        self.rt_nbp = self.rt_nbp.sel(time=slice(self.start, self.end))
        #print(slice(self.start, self.end))
        self.acos_nbp['months'] = date_range
        self.acos_nbp = xr.DataArray(self.acos_nbp, dims=['months', 'latitude', 'longitude'], name='ACOS')
        self.acos_nbp['months'] = date_range
        self.acos_nbp = self.acos_nbp.rename({
            'months': 'time',
            'latitude': 'lat',
            'longitude': 'lon'
        })
        self.acos_nbp = self.acos_nbp.sel(time=slice(self.start, self.end))
        self.prior_nbp['months'] = date_range
        self.prior_nbp = xr.DataArray(self.prior_nbp, dims=['months', 'latitude', 'longitude'], name='prior')
        self.prior_nbp = self.prior_nbp.rename({
            'months': 'time',
            'latitude': 'lat',
            'longitude': 'lon'
        })
        self.prior_nbp = self.prior_nbp.sel(time=slice(self.start, self.end))
        ensemble = [self.rt_nbp,
                    self.acos_nbp,
                    self.prior_nbp,
                    self.trans_regrid.transcom_regions,
                    self.trans_regrid.land_ecosystems,
                    self.trans_regrid.country_id,
                    self.ecos_regrid,
                    self.landsea_regrid]
        ensemble = xr.merge(ensemble)

        ensemble.to_netcdf(os.path.join(self.out_path, 'GOSAT_nbp.nc'))
        print(os.path.join(self.out_path, 'GOSAT_nbp.nc'))
        return self

    def get_mean(self):
        self.rt_nbp = xr.DataArray(self.rt_nbp, dims=['time', 'lat', 'lon'], name='nbp')
        self.rt_nbp.to_netcdf('/home/mhuang/ILAMB/ILAMB_sample/DATA/nbp/remotec/remotec.nc')
        import netCDF4 as nc

        with nc.Dataset('/home/mhuang/ILAMB/ILAMB_sample/DATA/nbp/remotec/remotec.nc', 'w') as file:
            file.createDimension('latitude', len(self.rt_nbp.lat))
            file.createDimension('longitude', len(self.rt_nbp.lon))
            file.createDimension('time', len(self.rt_nbp.time))

            latitude_variable = file.createVariable('latitude', 'f4', ('latitude',))
            latitude_variable.units = 'degrees_north'
            longitude_variable = file.createVariable('longitude', 'f4', ('longitude',))
            longitude_variable.units = 'degrees_east'
            time_variable = file.createVariable('time','u8', ('time',))
            D = file.createVariable("nbp", 'f4', ("time", 'latitude','longitude'))

            latitude_variable[:] = self.rt_nbp.lat
            longitude_variable[:] = self.rt_nbp.lon

            time_variable[:] = self.rt_nbp.time
            time_variable.units = "months since 2009-01"
            time_variable.calendar = "360_day"
            D[:] = self.rt_nbp
            #file.close()
        self.acos_nbp = xr.DataArray(self.acos_nbp, dims=['time', 'lat', 'lon']
                                     , coords={'time': self.acos_nbp.time, 'lat': self.acos_nbp.lat, 'lon': self.acos_nbp.lon}
                                     , name='nbp')
        self.acos_nbp.to_netcdf('/home/mhuang/ILAMB/ILAMB_sample/DATA/nbp/acos/acos.nc')
        with nc.Dataset('/home/mhuang/ILAMB/ILAMB_sample/DATA/nbp/acos/acos.nc', 'w') as file:

            file.createDimension('latitude', len(self.acos_nbp.lat))

            latitude_variable = file.createVariable('latitude', 'f4', ('latitude',))
            latitude_variable.units = 'degrees_north'

            latitude_variable[:] = self.acos_nbp.lat


if __name__ == '__main__':
    setting = input_pre.nbp
    x = TM5GosatPreprocess(setting).regrid_data()
    y = x.get_nbp()

"""
if __name__ == 'pre_tm5_gosat':
    setting = input_pre.nbp
    x = TM5GosatPreprocess(setting).regrid_data()
    y = x.get_nbp()

"""



