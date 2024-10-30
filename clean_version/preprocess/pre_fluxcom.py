import fnmatch
import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre

class FluxcomXPreprocess:
    def __init__(self, settings):
        self.in_path = settings['PATH_TO_FLUXCOM_X']
        self.out_path = settings['OUT_PATH']
        self.start_date = settings['START_DATE']
        self.end_date = settings['END_DATE']
        self.trans_file = settings['TRANSCOM_FILE']

        self.target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-89.5, 90.5, 1.0), {"units": "degrees_north"}),
                "lon": (["lon"], np.arange(-179.5, 180.5, 1.0), {"units": "degrees_east"}),
            }
        )

        self.nee = None
        self.nee_regrid = None
        self.gpp = None
        self.gpp_regrid = None

    def regrid_nee(self):
        nee = []
        years= ['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']
        for root, dirs, files in os.walk(self.in_path):
            for i in range(len(years)):
                for fname in files:
                    year = years[i]
                    pat = 'NEE_'+year+'*.nc'
                    if fnmatch.fnmatch(fname, pat):
                        #print(year)
                        f = os.path.join(root, fname)
                        nee.append(xr.open_dataset(f))

        #print(nee)
        nee = xr.concat(nee, dim='time')
        #print(nee.time)
        self.nee = nee.sel(time=slice(self.start_date, self.end_date))
        regrider = xesmf.Regridder(self.nee, self.target_grid, method='nearest_s2d', periodic=False)
        self.nee_regrid = regrider(self.nee)
        return self

    def regrid_gpp(self):
        gpp = []
        years= ['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']
        for root, dirs, files in os.walk(self.in_path):
            for i in range(len(years)):
                for fname in files:
                    year = years[i]
                    pat = 'GPP_' + year + '*.nc'
                    if fnmatch.fnmatch(fname, pat):
                        f = os.path.join(root, fname)
                        gpp.append(xr.open_dataset(f))

        gpp = xr.concat(gpp, dim='time')
        self.gpp = gpp.sel(time=slice(self.start_date, self.end_date))
        regrider = xesmf.Regridder(self.gpp, self.target_grid, method='nearest_s2d', periodic=False)
        self.gpp_regrid = regrider(self.gpp)
        return self

    def merge_data(self):
        trans = xr.open_dataset(self.trans_file)
        fluxcom = [
            self.nee_regrid,
            self.gpp_regrid,
            trans.transcom_regions,
            trans.land_ecosystems,
            trans.country_id
        ]
        fluxcom = xr.merge(fluxcom)
        fluxcom.to_netcdf(os.path.join(self.out_path, 'FLUXCOM_X.nc'))
        print(os.path.join(self.out_path, 'FLUXCOM_X.nc'))

class FluxcomPreprocess:
    def __init__(self, settings):
        self.in_path = settings['PATH_TO_FLUXCOM']
        self.out_path = settings['OUT_PATH']
        self.start_date = settings['START_DATE']
        self.end_date = settings['END_DATE']
        self.trans_file = settings['TRANSCOM_FILE']

        self.target_grid = xr.Dataset(
                {
                    "lat": (["lat"], np.arange(-89.5, 90.5, 1.0), {"units": "degrees_north"}),
                    "lon": (["lon"], np.arange(-179.5, 180.5, 1.0), {"units": "degrees_east"}),
                }
            )

        self.nee = None
        self.nee_regrid = None
        self.ter = None
        self.ter_regrid = None

    def regrid_nee(self):
        nee = xr.open_mfdataset(os.path.join(self.in_path, 'NEE*.nc'))
        self.nee = nee.sel(time=slice(self.start_date, self.end_date))
        self.nee = self.nee.resample(time='1M').mean()
        date_range = pd.date_range(start=self.start_date, end=self.end_date, freq='MS')
        self.nee['time'] = date_range
        regrider = xesmf.Regridder(self.nee, self.target_grid, method='nearest_s2d', periodic=False)
        self.nee_regrid = regrider(self.nee)
        return self

    def regrid_ter(self):
        ter = xr.open_mfdataset(os.path.join(self.in_path, 'TER*.nc'))
        self.ter = ter.sel(time=slice(self.start_date, self.end_date))
        self.ter = self.ter.resample(time='1M').mean()
        date_range = pd.date_range(start=self.start_date, end=self.end_date, freq='MS')
        self.ter['time'] = date_range
        regrider = xesmf.Regridder(self.ter, self.target_grid, method='nearest_s2d', periodic=False)
        self.ter_regrid = regrider(self.ter)
        return self

    def merge_data(self):
        print('merging data...')
        trans = xr.open_dataset(self.trans_file)
        fluxcom = [
            self.nee_regrid.NEE,
            self.ter_regrid.TER,
            trans.transcom_regions,
            trans.land_ecosystems,
            trans.country_id
        ]
        fluxcom = xr.merge(fluxcom)
        fluxcom.to_netcdf(os.path.join(self.out_path, 'FLUXCOM.nc'))
        print(os.path.join(self.out_path, 'FLUXCOM.nc'))

if __name__ == '__main__':
    setting = input_pre.transcom
    #FluxcomXPreprocess(setting).regrid_nee().regrid_gpp().merge_data()
    FluxcomPreprocess(setting).regrid_nee().regrid_ter().merge_data()
"""
if __name__ == 'pre_fluxcom':
    setting = input_pre.transcom
    #FluxcomXPreprocess(setting).regrid_nee().regrid_gpp().merge_data()
    FluxcomPreprocess(setting).regrid_nee().regrid_ter().merge_data()
"""
