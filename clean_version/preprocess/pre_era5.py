import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre
import pre_trendy
import matplotlib.pyplot as plt

class ERA5Preprocess:
    def __init__(self, settings):
        self.in_path_wind  = settings['PATH_TO_WIND']
        self.in_path_tp    = settings['PATH_TO_TP']
        self.in_path_t2m   = settings['PATH_TO_T2M']
        self.in_path_e     = settings['PATH_TO_E']
        self.in_path_swc   = settings['PATH_TO_SWC']
        self.in_path_sst   = settings['PATH_TO_SST']
        self.out_path      = settings['OUT_PATH']
        self.start_date    = settings['START_DATE']
        self.end_date      = settings['END_DATE']
        self.trans_file    = settings['TRANSCOM_FILE']
        self.fname_wind    = settings['FNAME_WIND']
        self.fname_tp      = settings['FNAME_TP']
        self.fname_e       = settings['FNAME_E']
        self.fname_t2m     = settings['FNAME_T2M']
        self.fname_swc     = settings['FNAME_SWC']
        self.fname_sst     = settings['FNAME_SST']

        self.target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-90, 90, 1.0)),
                "lon": (["lon"], np.arange(-180, 180, 1.0)),
            }
        )
        """
        self.target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-89.75, 89.75+0.5, 0.5)),
                "lon": (["lon"], np.arange(-179.75, 179.75+0.5, 0.5)),
            }
        )
        """
        """
        self.target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-89.5, 90.5, 1.0), {"units": "degrees_north"}),
                "lon": (["lon"], np.arange(-179.5, 180.5, 1.0), {"units": "degrees_east"}),
            }
        )"""
        self.wind        = None
        self.wind_regrid = None
        self.tp          = None
        self.tp_regrid   = None
        self.t2m         = None
        self.t2m_regrid  = None
        self.e           = None
        self.e_regrid    = None
        self.swc         = None
        self.swc_regrid  = None
        self.sst         = None
        self.sst_regrid  = None
        self.ecos_regrid = None
    def regrid_wind(self):
        self.wind = xr.open_dataset(os.path.join(self.in_path_wind, self.fname_wind))
        self.wind = self.wind.sel(time=slice(self.start_date, self.end_date), expver=1)
        regrider = xesmf.Regridder(self.wind, self.target_grid, method='bilinear', periodic=True)
        self.wind_regrid = regrider(self.wind)
        return self
    def regrid_tp(self):
        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        self.tp = xr.open_dataset(os.path.join(self.in_path_tp, self.fname_tp))
        self.tp = self.tp.sel(time=slice(self.start_date, self.end_date))
        regrider = xesmf.Regridder(self.tp, self.target_grid, method='bilinear', periodic=True)
        self.tp_regrid = regrider(self.tp)
        regrider = xesmf.Regridder(ecos, self.target_grid, method='nearest_s2d', periodic=True)
        self.ecos_regrid = regrider(ecos)
        #print(self.tp_regrid)
        return self

    def regrid_t2m(self):
        self.t2m = xr.open_dataset(os.path.join(self.in_path_t2m, self.fname_t2m))
        self.t2m = self.t2m.sel(time=slice(self.start_date, self.end_date))
        regrider = xesmf.Regridder(self.t2m, self.target_grid, method='bilinear', periodic=True)
        self.t2m_regrid = regrider(self.t2m)
        return self

    def regrid_e(self):
        self.e = xr.open_dataset(os.path.join(self.in_path_e, self.fname_e))
        self.e = self.e.sel(time=slice(self.start_date, self.end_date))
        regrider = xesmf.Regridder(self.e, self.target_grid, method='bilinear', periodic=True)
        self.e_regrid = regrider(self.e)
        return self
    def regrid_swc(self):
        self.swc = xr.open_dataset(os.path.join(self.in_path_swc, self.fname_swc))
        self.swc = self.swc.sel(time=slice(self.start_date, self.end_date))
        regrider = xesmf.Regridder(self.swc, self.target_grid, method='bilinear', periodic=True)
        self.swc_regrid = regrider(self.swc)
        return self
    def regrid_sst(self):
        self.sst = xr.open_dataset(os.path.join(self.in_path_sst, self.fname_sst))
        self.sst = self.sst.sel(time=slice(self.start_date, self.end_date))
        regrider = xesmf.Regridder(self.sst, self.target_grid, method='bilinear', periodic=True)
        self.sst_regrid = regrider(self.sst)
        return self
    def merge_data(self):
        trans = xr.open_dataset(self.trans_file)
        era5 = [
            self.tp_regrid,
            self.t2m_regrid,
            self.e_regrid,
            self.swc_regrid,
            self.wind_regrid,
            self.sst_regrid,
            trans.transcom_regions,
            trans.land_ecosystems,
            trans.country_id,
            self.ecos_regrid
        ]
        era5 = xr.merge(era5)
        era5.to_netcdf(os.path.join(self.out_path, 'ERA51x1.nc'))
        print(os.path.join(self.out_path, 'ERA51x1.nc'))

if __name__ == '__main__':
    setting = input_pre.era5
    ERA5Preprocess(setting).regrid_wind().regrid_tp().regrid_t2m().regrid_e().regrid_swc().regrid_sst().merge_data()
"""
if __name__ == 'pre_era5':
    setting = input_pre.era5
    ERA5Preprocess(setting).regrid_tp().merge_data()"""