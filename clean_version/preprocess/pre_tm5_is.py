import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre

class TM5InsituPreprocess:
    def __init__(self, settings):
        self.tm5_fn = os.path.join(settings['PATH_TO_IS'], settings['TM5'])
        self.ct_fn  = os.path.join(settings['PATH_TO_IS'], settings['CarbonTracker'])
        self.cams_fn= os.path.join(settings['PATH_TO_IS'], settings['CAMS'])

        self.tm5 = xr.open_dataset(self.tm5_fn)
        self.tm5 = self.tm5.rename({'months': 'time'})
        self.ct  = xr.open_dataset(self.ct_fn)
        self.cams = xr.open_dataset(self.cams_fn)
        self.tran = xr.open_dataset(settings['TRANSCOM_FILE'])

        self.ct_b4_fn = os.path.join(settings['PATH_TO_IS'], settings['CarbonTracker_b4_pri'])
        self.ct_w4_fn = os.path.join(settings['PATH_TO_IS'], settings['CarbonTracker_w4_pri'])
        self.ct_bc_fn = os.path.join(settings['PATH_TO_IS'], settings['CarbonTracker_bc_pri'])
        self.ct_wc_fn = os.path.join(settings['PATH_TO_IS'], settings['CarbonTracker_wc_pri'])

        self.ct_b4    = xr.open_dataset(self.ct_b4_fn)
        self.ct_w4    = xr.open_dataset(self.ct_w4_fn)
        self.ct_bc    = xr.open_dataset(self.ct_bc_fn)
        self.ct_wc    = xr.open_dataset(self.ct_wc_fn)
        self.tm5_pri  = xr.open_dataset(settings['TM5_pri'])
        self.tm5_pri  = self.tm5_pri.rename({'months': 'time'})

        self.out_path = settings['OUT_PATH']
        self.transcom_file = settings['TRANSCOM_FILE']
        self.start = settings['START_DATE']
        self.end = settings['END_DATE']

        self.tran_regrid     = None
        self.cams_nbp        = None
        self.cams_pri        = None
        self.ct_nbp          = None
        self.ct_4_pri        = None
        self.ct_c_pri        = None
        self.tm5_nbp         = None
        self.tm5_nbp_pri     = None
        self.cams_nbp_regrid = None
        self.ct_nbp_regrid   = None
        self.tm5_nbp_regrid  = None
        self.cams_pri_regrid = None
        self.ct_4_regrid     = None
        self.ct_c_regrid     = None
        self.tm5_nbp_pri_regrid  = None
        self.target_grid     = None
        self.ecos_regrid     = None

    def get_nbp(self):
        self.cams_nbp = self.cams['flux_apos_bio'].sel(time=slice(self.start, self.end))
        self.cams_pri = self.cams['flux_apri_bio'].sel(time=slice(self.start, self.end))
        self.ct_nbp   = (self.ct['bio_flux_opt'].sel(time=slice(self.start, self.end)) +
                         self.ct['fire_flux_imp'].sel(time=slice(self.start, self.end)))
        self.ct_4_pri = (self.ct_b4['b4'].sel(time=slice(self.start, self.end)) +
                         self.ct_w4['w4'].sel(time=slice(self.start, self.end)))
        self.ct_c_pri = (self.ct_bc['bc'].sel(time=slice(self.start, self.end)) +
                         self.ct_wc['wc'].sel(time=slice(self.start, self.end)))
        time = pd.date_range(start=self.start, end=self.end, freq='MS')
        #time = time.strftime('%Y-%m').tolist()
        self.cams_nbp['time']   = time
        self.cams_pri['time']   = time
        self.ct_nbp['time']     = time
        self.ct_4_pri['time']   = time
        self.ct_c_pri['time']   = time
        start_date = '2009-01-01'
        end_date = '2019-06-01'
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
        date_list = date_range.strftime('%Y-%m').tolist()
        self.tm5['time'] = date_range
        self.tm5_pri['time'] = date_range
        self.tm5_nbp  = (self.tm5['CO2_flux_nee'].sel(time=slice(self.start, self.end))
                         + self.tm5['CO2_flux_fire'].sel(time=slice(self.start, self.end)))
        self.tm5_nbp_pri  = (self.tm5_pri['CO2_flux_nee'].sel(time=slice(self.start, self.end))
                         + self.tm5_pri['CO2_flux_fire'].sel(time=slice(self.start, self.end)))

        #self.cams_nbp = xr.DataArray(self.cams_nbp, dims=['time', 'latitude', 'longitude'], name='CAMS')
        #self.ct_nbp = xr.DataArray(self.ct_nbp, dims=['time', 'latitude', 'longitude'], name='CarbonTracker')
        #self.tm5_nbp = xr.DataArray(self.tm5_nbp, dims=['time', 'latitude', 'longitude'], name='TM5-4DVAR')
        return self

    def regrid_data(self):
        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        self.target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-90, 90, 1.0)),
                "lon": (["lon"], np.arange(-180, 180, 1.0)),
            }
        )
        regrider = xesmf.Regridder(self.tran, self.target_grid, method='nearest_s2d', periodic=False)
        self.trans_regrid = regrider(self.tran)
        regrider = xesmf.Regridder(self.cams_nbp, self.target_grid, method='nearest_s2d', periodic=False)
        self.cams_nbp_regrid = regrider(self.cams_nbp)
        regrider = xesmf.Regridder(self.cams_pri, self.target_grid, method='nearest_s2d', periodic=False)
        self.cams_pri_regrid = regrider(self.cams_pri)
        regrider = xesmf.Regridder(self.ct_nbp, self.target_grid, method='nearest_s2d', periodic=False)
        self.ct_nbp_regrid = regrider(self.ct_nbp)
        regrider = xesmf.Regridder(self.ct_4_pri, self.target_grid, method='nearest_s2d', periodic=False)
        self.ct_4_regrid = regrider(self.ct_4_pri)
        regrider = xesmf.Regridder(self.ct_c_pri, self.target_grid, method='nearest_s2d', periodic=False)
        self.ct_c_regrid = regrider(self.ct_c_pri)
        regrider = xesmf.Regridder(self.tm5_nbp, self.target_grid, method='nearest_s2d', periodic=False)
        self.tm5_nbp_regrid = regrider(self.tm5_nbp)
        regrider = xesmf.Regridder(self.tm5_nbp_pri, self.target_grid, method='nearest_s2d', periodic=False)
        self.tm5_nbp_pri_regrid = regrider(self.tm5_nbp_pri)
        regrider = xesmf.Regridder(ecos, self.target_grid, method='nearest_s2d', periodic=False)
        self.ecos_regrid = regrider(ecos)
        return self

    def merge_data(self):
        self.cams_nbp_regrid = xr.DataArray(self.cams_nbp_regrid
                                            , dims=['time', 'lat', 'lon']
                                            , name='CAMS')
        self.cams_pri_regrid = xr.DataArray(self.cams_pri_regrid
                                            , dims=['time', 'lat', 'lon']
                                            , name='CAMS_prior'
        )
        self.ct_nbp_regrid = xr.DataArray(self.ct_nbp_regrid, dims=['time', 'lat', 'lon'], name='CarbonTracker')

        self.ct_4_regrid = xr.DataArray(self.ct_4_regrid, dims=['time', 'lat', 'lon'], name='CT_pri_4p1s')

        self.ct_c_regrid = xr.DataArray(self.ct_c_regrid, dims=['time', 'lat', 'lon'], name='CT_pri_cms')
        self.tm5_nbp = xr.DataArray(self.tm5_nbp, dims=['time', 'lat', 'lon']
                                    , coords = {'time': self.tm5_nbp['time'],
                                                       'lat': self.target_grid['lat'],
                                                       'lon': self.target_grid['lon']}
                                    , name='TM5-4DVAR')
        self.tm5_nbp_pri = xr.DataArray(self.tm5_nbp_pri, dims=['time', 'lat', 'lon']
                                    , coords={'time': self.tm5_nbp_pri['time'],
                                              'lat': self.target_grid['lat'],
                                              'lon': self.target_grid['lon']}
                                    , name='TM5-4DVAR_prior')
        ensemble = [
            self.cams_nbp_regrid,
            self.cams_pri_regrid,
            self.ct_nbp_regrid,
            self.ct_c_regrid,
            self.ct_4_regrid,
            self.tm5_nbp,
            self.tm5_nbp_pri,
            self.trans_regrid.transcom_regions,
            self.trans_regrid.land_ecosystems,
            self.trans_regrid.country_id,
            self.ecos_regrid
        ]
        ensemble = xr.merge(ensemble)
        ensemble.to_netcdf(os.path.join(self.out_path, 'IS_nbp.nc'))
        print(os.path.join(self.out_path, 'IS_nbp.nc'))

if __name__ == '__main__':
    setting = input_pre.is_nbp
    x=TM5InsituPreprocess(setting).get_nbp().regrid_data().merge_data()
    #print(x.)
"""
if __name__ == 'pre_tm5_is':
    setting = input_pre.is_nbp
    x = TM5InsituPreprocess(setting).get_nbp().regrid_data().merge_data()
"""