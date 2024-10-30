"""
Note: Models need manual setting

v9:
    DLEM NBP does not have monthly time step,
    use nbp = ra + rh + fFire + fLuc - gpp
    CABLE-POP v9 does not have NBP, so use v11 instead
    JULES doesn't have ra, use ra = gpp - npp

v11
    Function read_data have problem with TRENDY v11 VISIT-NIES
    pandas._libs.tslibs.parsing.DateParseError: Unknown datetime string format, unable to parse:  AD 0-Jan-1st (double)
"""

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
S='S2_'
def read_data(path, var, start_date, end_date, out_path):
    """
    Read variable from TRENDYS
    :param path: path to the TRENDYs
    :param var:  variable to read
    :return:     ensemble of a certain TRENDY variable
    """
    member_name = []
    i           = 0
    name        = var
    for root, dirs, files in os.walk(path):
        for fname in files:
            if var == 'npp' and fname == 'JULES-ES-1p0_S3_npp_nlim.nc':
                target_path = os.path.join(root, fname)
                member_name.append(os.path.basename(os.path.dirname(target_path)))
                print("Found:", target_path)
                data = xr.open_dataset(target_path, engine='netcdf4', decode_times=True)
                data['time'] = pd.date_range(start=data.indexes['time'].to_datetimeindex()[0],
                                             periods=len(data['time']), freq='MS')
                data_rename = data.rename_vars({'npp_nlim': 'npp'})
                data_sel = data_rename.sel(time=slice(pd.Timestamp(start_date), pd.Timestamp(end_date)))
                data_sel.to_netcdf(os.path.join(out_path, var, 'JULES-ES-1p0_S3_npp.nc'))
                print(len(data_sel['time']))

            #pat = '*_S3_' + var + '.nc'
            pat = '*_' + S + name + '.nc'
            var = name + S
            if (fnmatch.fnmatch(fname, pat=pat)
                and fname != 'DLEM_S3_nbp.nc'
                #and fname.split('_')[0] != 'VISIT-NIES'
            ):
                target_path = os.path.join(root, fname)
                member_name.append(os.path.basename(os.path.dirname(target_path)))
                print("Found:", target_path)
                i = i + 1

                if fname.split('_')[0] == 'ORCHIDEEv3':
                    data                 = xr.open_dataset(target_path, engine='netcdf4', decode_times=True)
                    data['time_counter'] = pd.date_range(start=data.indexes['time_counter'].to_datetimeindex()[0],
                                                         periods=len(data['time_counter']), freq='MS')
                    #data = data.rename({'time_counter': 'time'})
                    data_sel = data.sel(time_counter=slice(pd.Timestamp(start_date), pd.Timestamp(end_date)))
                    data_sel.to_netcdf(os.path.join(out_path, var, fname))
                    print(len(data_sel['time_counter']))

                elif fname.split('_')[0] == 'ISBA-CTRIP':

                    data                  = xr.open_dataset(target_path, engine='netcdf4', decode_times=False)
                    units, reference_date = data.time_counter.attrs['units'].split('since')
                    data['time_counter']  = pd.date_range(start=reference_date, periods=data.sizes['time_counter'],
                                                          freq='MS')
                    #data = data.rename({'time_counter': 'time'})
                    data_sel              = data.sel(time_counter=slice(pd.Timestamp(start_date), pd.Timestamp(end_date)))
                    data_sel.to_netcdf(os.path.join(out_path, var, fname))
                    print(len(data_sel['time_counter']))
                    """
                    data = nc.open_data(target_path)
                    data = data.to_xarray()
                    data_sel  = data.sel(time=slice(start_date, end_date))
                    data_sel['time'] = pd.date_range(start=start_date, end=end_date, freq='MS')
                    data_sel.to_netcdf(os.path.join(out_path, var, fname))
"""
                elif (fname.split('_')[0] == 'VISIT'
                      #or fname.split('_')[0] == 'IBIS'
                      or fname.split('_')[0] == 'JSBACH'
                      or fname.split('_')[0] == 'YIBs'
                      or fname.split('_')[0] == 'DLEM'
                      or fname.split('_')[0] == 'CABLE-POP'
                      or fname.split('_')[0] == 'ISAM'
                      or fname.split('_')[0] == 'VISIT-NIES'
                      #or fname.split('_')[0] == 'CLM5.0'
                ) :
                    """
                    data        = xr.open_dataset(target_path, engine='netcdf4', decode_times=False)
                    units, reference_date = data.time.attrs['units'].split('since')
                    data['time'] = pd.date_range(start=reference_date, periods=data.sizes['time'], freq='M')
                    data_sel = data.sel(time=slice(pd.Timestamp(start_date), pd.Timestamp(end_date)))
                    data_sel.to_netcdf(os.path.join(out_path, var, fname))
                    """
                    data = nc.open_data(target_path)
                    data = data.to_xarray()
                    data_sel = data.sel(time=slice(start_date, end_date))
                    data_sel['time'] = pd.date_range(start=start_date,
                                                end=end_date, freq='MS')
                    data_sel.to_netcdf(os.path.join(out_path, var, fname))
                    print(len(data_sel['time']))

                elif fname.split('_')[0] == 'IBIS':
                    data = xr.open_dataset(target_path, engine='netcdf4', decode_times=False)
                    units, reference_date = data.time.attrs['units'].split('since')
                    data['time'] = pd.date_range(start=reference_date, periods=data.sizes['time'], freq='MS')
                    data_sel = data.sel(time=slice(pd.Timestamp(start_date), pd.Timestamp(end_date)))
                    data_sel.to_netcdf(os.path.join(out_path, var, fname))
                    print(len(data_sel['time']))

                elif fname.split('_')[0] == 'CLM5.0':
                    data = nc.open_data(target_path)
                    data = data.to_xarray()
                    data_sel = data.sel(time=slice(start_date, end_date))
                    data_sel['time'] = pd.date_range(start=start_date,
                                                     end=end_date, freq='MS')
                    data_sel.to_netcdf(os.path.join(out_path, var, fname))
                    print(len(data_sel['time']))

                else:
                    data        = xr.open_dataset(target_path, engine='netcdf4', decode_times=True)
                    data['time'] = pd.date_range(start=data.indexes['time'].to_datetimeindex()[0],
                                                 periods=len(data['time']), freq='MS')
                    data_sel = data.sel(time=slice(pd.Timestamp(start_date), pd.Timestamp(end_date)))
                    data_sel.to_netcdf(os.path.join(out_path, var, fname))
                    print(len(data_sel['time']))

def regrid_data(in_path, var, out_path):
    """
    regrid the data to 1x1 resolution
    :param in_path: path of input data
    :param var: variable to regrid
    :param out_path: path of output data
    :return:
    """
    var=var+S
    #target_grid = xesmf.util.grid_2d(-180,180,1,-90,90,1)
    #target_grid = xesmf.util.grid_global(1, 1, cf=False, lon1=180)
    target_grid = xr.Dataset(
        {
            "lat": (["lat"], np.arange(-90, 90, 1.0)),
            "lon": (["lon"], np.arange(-180, 180, 1.0)),
        }
    )
    #print(target_grid.x)

    for filename in os.listdir(os.path.join(in_path, var)):
        file_in   = os.path.join(in_path, var, filename)
        print('regriding : ', file_in)
        data_in   = xr.open_dataset(file_in, engine='netcdf4')
        regrider  = xesmf.Regridder(data_in, target_grid, method='nearest_s2d', periodic=False)
        data_out  = regrider(data_in)

        dir       = var + '_regrid'
        #print('regrid to : ', os.path.join(out_path, dir, filename))
        data_out.to_netcdf(os.path.join(out_path, dir, filename))

    regrid_path = os.path.join(out_path, dir)
    return regrid_path

def merge_data(in_path, var, modis_eco, transcom_file, out_path):
    """
    merge a certain variable from TRENDY members into a single file
    :param data:           data to be merged
    :param transcom_file:  location of the transcom file
    :param out_file:       location of the merged file
    :return:
    """
    ensemble = []
    members  = []
    for filename in os.listdir(os.path.join(in_path)):
        member = filename.split('_')[0]
        file        = os.path.join(in_path, filename)
        data        = xr.open_dataset(file, engine='netcdf4', decode_times=False)
        print(file)
        if filename == 'ISAM_S3_lai.nc':
            data_rename = data.rename({'LAI': member})
        elif filename == 'CABLE-POP_S3_fLuc.nc':
            data_rename = data.rename({'fLUC':member})
        else:
            data_rename = data.rename({var:member})
        if 'time_counter' in data_rename.dims:
            data_rename = data_rename.rename({'time_counter':'time'})
        ensemble.append(data_rename)
        # get the name of trendy model from filename
        members.append(member)

    transcom = xr.open_dataset(transcom_file)
    ensemble.append(transcom.transcom_regions)
    ensemble.append(transcom.land_ecosystems)
    ensemble.append(transcom.country_id)
    ensemble.append(modis_eco)
    ensemble = xr.merge(ensemble)
    fname = var + S + '_ensemble.nc'
    ensemble.to_netcdf(os.path.join(out_path, fname))

def get_DLEMnbp(ra_path, rh_path, gpp_path, nbp_path):
    """
    ra = xr.open_dataset(os.path.join(ra_path, 'DLEM_S3_ra.nc'))
    rh = xr.open_dataset(os.path.join(rh_path, 'DLEM_S3_rh.nc'))
    gpp = xr.open_dataset(os.path.join(gpp_path, 'DLEM_S3_gpp.nc'))
    nbp  = -(ra.ra + rh.rh - gpp.gpp)
    nbp.to_netcdf('/home/mhuang/data/DLEM_S3_nbp.nc')
    nbp  = xr.open_dataset('/home/mhuang/data/DLEM_S3_nbp.nc')
    nbp_rename = nbp.rename_vars({'__xarray_dataarray_variable__':'nbp'})
    nbp_rename.to_netcdf(os.path.join(nbp_path, 'DLEM_S3_nbp.nc'))"""

    ra = xr.open_dataset(os.path.join(ra_path, 'DLEM_'+S+'ra.nc'))
    rh = xr.open_dataset(os.path.join(rh_path, 'DLEM_'+S+'rh.nc'))
    gpp = xr.open_dataset(os.path.join(gpp_path, 'DLEM_'+S+'gpp.nc'))
    nbp = -(ra.ra + rh.rh - gpp.gpp)
    nbp.to_netcdf('/home/mhuang/data/DLEM_'+S+'nbp.nc')
    nbp = xr.open_dataset('/home/mhuang/data/DLEM_'+S+'nbp.nc')
    nbp_rename = nbp.rename_vars({'__xarray_dataarray_variable__': 'nbp'})
    nbp_rename.to_netcdf(os.path.join(nbp_path, 'DLEM_'+S+'nbp.nc'))

def get_JULESES1p0ra(gpp_path, npp_path, ra_path):
    gpp = xr.open_dataset(os.path.join(gpp_path, 'JULES-ES-1p0_S3_gpp.nc'))
    npp = xr.open_dataset(os.path.join(npp_path, 'JULES-ES-1p0_S3_npp.nc'))
    ra  = gpp.gpp - npp.npp
    ra.to_netcdf('/home/mhuang/data/JULES-ES-1p0_S3_ra.nc')
    ra  = xr.open_dataset('/home/mhuang/data/JULES-ES-1p0_S3_ra.nc')
    ra_rename=ra.rename_vars({'__xarray_dataarray_variable__':'ra'})
    ra_rename.to_netcdf(os.path.join(ra_path, 'JULES-ES-1p0_S3_ra.nc'))

class TrendyPreprocess:
    def __init__(self, settings):
        self.in_path     = settings['TRENDY_PATH']
        self.out_file    = settings['OUT_PATH']
        self.var         = settings['VAR']
        self.start_date  = settings['START_DATE']
        self.end_date    = settings['END_DATE']
        self.target_file = settings['TRANSCOM_FILE']
        self.ecos_regrid = None

    def preprocess(self):
        target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-90, 90, 1.0)),
                "lon": (["lon"], np.arange(-180, 180, 1.0)),
            }
        )
        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        regrider = xesmf.Regridder(ecos, target_grid, method='nearest_s2d', periodic=False)
        self.ecos_regrid = regrider(ecos)

        read_data(self.in_path, self.var, self.start_date, self.end_date, self.out_file)
        regrid_path = regrid_data(self.out_file, self.var, self.out_file)
        print(regrid_path)
        merge_data(regrid_path, self.var, self.ecos_regrid, self.target_file, self.out_file)

class TM5GosatPreprocess:
    def __init__(self, settings):
        self.path            = settings['PATH_TO_GOSAT_IS']
        self.rt_file         = os.path.join(self.path, settings['REMOTEC'])
        self.acos_file       = os.path.join(self.path, settings['ACOS'])
        self.out_path        = os.path.join(self.path, settings['OUT_PATH'])
        self.transcom_file   = settings['TRANSCOM_FILE']
        self.start           = settings['START_DATE']
        self.end             = settings['END_DATE']

        self.trans_regrid    = None
        self.rt              = None
        self.rt_nbp          = None
        self.acos            = None
        self.acos_nbp        = None

    def regrid_data(self):
        target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-90, 90, 1.0)),
                "lon": (["lon"], np.arange(-180, 180, 1.0)),
            }
        )
        trans_in = xr.open_dataset(self.transcom_file)
        regrider = xesmf.Regridder(trans_in, target_grid, method='nearest_s2d', periodic=False)
        self.trans_regrid = regrider(trans_in)
        return self

    def get_nbp(self):
        self.rt = xr.open_dataset(self.rt_file)
        self.acos = xr.open_dataset(self.acos_file)
        self.rt_nbp   = self.rt.CO2_flux_nee + self.rt.CO2_flux_fire
        self.acos_nbp   = self.acos.CO2_flux_nee + self.acos.CO2_flux_fire
        start_date           = '2009-01-01'
        end_date             = '2019-06-01'
        date_range           = pd.date_range(start=start_date, end=end_date, freq='MS')
        date_list            = date_range.strftime('%Y-%m').tolist()
        self.rt_nbp = xr.DataArray(self.rt_nbp, dims=['months', 'latitude', 'longitude'], name='RemoTeC')
        self.rt_nbp['months']   = date_range
        self.rt_nbp = self.rt_nbp.rename({
            'months': 'time',
            'latitude': 'lat',
            'longitude': 'lon'
        })
        self.rt_nbp = self.rt_nbp.sel(time=slice(self.start, self.end))
        self.acos_nbp['months'] = date_range
        self.acos_nbp = xr.DataArray(self.acos_nbp, dims=['months', 'latitude', 'longitude'], name='ACOS')
        self.acos_nbp['months'] = date_range
        self.acos_nbp = self.acos_nbp.rename({
            'months': 'time',
            'latitude': 'lat',
            'longitude': 'lon'
        })
        self.acos_nbp = self.acos_nbp.sel(time=slice(self.start, self.end))
        ensemble = [self.rt_nbp,
                    self.acos_nbp,
                    self.trans_regrid.transcom_regions,
                    self.trans_regrid.land_ecosystems,
                    self.trans_regrid.country_id]
        ensemble = xr.merge(ensemble)

        ensemble.to_netcdf(os.path.join(self.out_path, 'GOSAT_nbp.nc'))
        print(os.path.join(self.out_path, 'GOSAT_nbp.nc'))
        return self


if __name__ == '__main__':
    #target_grid = xesmf.util.grid_global(1, 1, cf=False, lon1=180)
    target_grid = xr.Dataset(
        {
            "lat": (["lat"], np.arange(-90, 90, 1.0)),
            "lon": (["lon"], np.arange(-180, 180, 1.0)),
        }
    )
    data_in = xr.open_dataset('/home/eschoema/regions.nc')
    regrider = xesmf.Regridder(data_in, target_grid, method='nearest_s2d', periodic=False)
    data_out = regrider(data_in)
    data_out.to_netcdf('/home/mhuang/data/regions_regrid.nc')

    #settings = input_pre.lai
    #TrendyPreprocess(settings).preprocess()
    # preprocess fLuc
    #settings = input_pre.fLuc
    #TrendyPreprocess(settings).preprocess()
    # preprocess fFire
    #settings = input_pre.fFire
    #TrendyPreprocess(settings).preprocess()
    # preprocess npp
    #settings = input_pre.npp
    #TrendyPreprocess(settings).preprocess()
    # preprocess gpp
    #settings = input_pre.gpp
    #TrendyPreprocess(settings).preprocess()
    # preprocess rh
    #settings = input_pre.rh
    #TrendyPreprocess(settings).preprocess()
    # preprocess ra
    """
    settings = input_pre.ra
    if os.path.basename(settings['OUT_PATH'].split('/')[-1]) == 'v9':
        gpp_path = os.path.join(input_pre.gpp['OUT_PATH'], input_pre.gpp['VAR'])
        npp_path = os.path.join(input_pre.npp['OUT_PATH'], input_pre.npp['VAR'])
        ra_path  = os.path.join(input_pre.ra['OUT_PATH'], input_pre.ra['VAR'])
        get_JULESES1p0ra(gpp_path, npp_path, ra_path)
    TrendyPreprocess(settings).preprocess()
    # preprocess nbp
    settings = input_pre.nbp
    """

    """
    if os.path.basename(settings['OUT_PATH'].split('/')[-1]) == 'v9':
        ra_path = os.path.join(input_pre.ra['OUT_PATH'], input_pre.ra['VAR'])
        rh_path = os.path.join(input_pre.rh['OUT_PATH'], input_pre.rh['VAR'])
        gpp_path = os.path.join(input_pre.gpp['OUT_PATH'], input_pre.gpp['VAR'])
        nbp_path = os.path.join(input_pre.nbp['OUT_PATH'], input_pre.nbp['VAR'])
        get_DLEMnbp(ra_path, rh_path, gpp_path, nbp_path)
        """
    """
    ra_path = os.path.join(input_pre.ra['OUT_PATH'], input_pre.ra['VAR'])
    rh_path = os.path.join(input_pre.rh['OUT_PATH'], input_pre.rh['VAR'])
    gpp_path = os.path.join(input_pre.gpp['OUT_PATH'], input_pre.gpp['VAR'])
    nbp_path = os.path.join(input_pre.nbp['OUT_PATH'], input_pre.nbp['VAR'])
    get_DLEMnbp(ra_path, rh_path, gpp_path, nbp_path)
    TrendyPreprocess(settings).preprocess()
    """
    settings = input_pre.nbp
    TrendyPreprocess(settings).preprocess()









