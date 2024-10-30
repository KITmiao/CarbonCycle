import os
import time as tt
import pandas as pd
from distributed.dashboard.components.shared import Processing

import input
import name_dic
import data_loader
import concurrent.futures
from functools import partial
import multiprocessing
import xarray as xr
class ProcessTRENDY:
    def __init__(self,settings,var):
        self.setting       = settings
        self.start_date     = settings['start_date']
        self.end_date       = settings['end_date']
        self.dates          = data_loader.create_date(self.start_date, self.end_date)
        self.year           = list(set(date.split('-')[0] for date in self.dates['list'])) #settings['year']
        #self.year           = settings['year']
        self.path           = settings['path']
        if settings['path'].split('/')[-1] == 'v9':
            self.name       = name_dic.trendy_names
        elif settings['path'].split('/')[-1] == 'v11':
            self.name       = name_dic.trendy_names_v11
        self.good_name      = settings['good_models']
        self.ok_name        = settings['ok_models']
        self.bad_name       = [x for x in self.name if x not in self.good_name and x not in self.ok_name]
        self.region         = name_dic.transcom[settings['region']]
        self.area           = self.region['area']

        self.fname          = settings[var]

        nbp_fname             = os.path.join(self.path, self.fname)
        nbp_spatial, nbp_time = data_loader.load_data(nbp_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial          = nbp_spatial
        if var != 'lai':
            self.timeseries       = data_loader.convert_trendy_unit(nbp_time, self.area)
        else:
            self.timeseries = nbp_time
        self.good_timeser     = self.timeseries[self.good_name].mean(axis=1)
        self.good_timeser_std = self.timeseries[self.good_name].std(axis=1)
        self.ok_timeser       = self.timeseries[self.ok_name].mean(axis=1)
        self.ok_timeser_std   = self.timeseries[self.ok_name].std(axis=1)
        self.bad_timeser      = self.timeseries[self.bad_name].mean(axis=1)
        self.bad_timeser_std  = self.timeseries[self.bad_name].std(axis=1)
        self.season_cyc       = data_loader.get_season_cycle(self.timeseries, self.name)
        self.good_season      = data_loader.get_season_cycle(self.timeseries, self.good_name)
        self.ok_season        = data_loader.get_season_cycle(self.timeseries, self.ok_name)
        self.bad_season       = data_loader.get_season_cycle(self.timeseries, self.bad_name)
        print('TRENDY ', var, ' done')
class ProcessOCO:
    def __init__(self,settings):
        self.start_date     = '2014-09-01'
        self.end_date       = '2018-12-31'
        self.dates          = data_loader.create_date(self.start_date, self.end_date)
        self.year           = settings['year']
        self.name           = name_dic.tm5oco_names
        self.region         = name_dic.transcom[settings['region']]
        self.area           = self.region['area']
        self.path           = '/home/mhuang/data/trendy/v11'
        self.fname          = 'OCO_nbp.nc'

        tm5gosat_fname        = os.path.join(self.path, self.fname)
        nbp_spatial, nbp_time = data_loader.load_data(tm5gosat_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial          = nbp_spatial
        self.timeseries       = data_loader.convert_tm5gosat_unit(nbp_time, self.area)
        self.season_cyc       = data_loader.get_season_cycle(self.timeseries, self.name)
        print('TM5 OCO done')
class ProcessOCO2MIP:
    def __init__(self,settings):
        self.start_date     = '2015-01-01'
        self.end_date       = '2018-12-31'
        self.dates          = data_loader.create_date(self.start_date, self.end_date)
        self.year           = settings['year']
        self.name           = name_dic.oco2mip_names
        self.region         = name_dic.transcom[settings['region']]
        self.area           = self.region['area']
        self.path           = '/home/mhuang/data/trendy/v11'
        self.fname          = 'oco2mip_regrid.nc'

        tm5gosat_fname        = os.path.join(self.path, self.fname)
        nbp_spatial, nbp_time = data_loader.load_data(tm5gosat_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial          = nbp_spatial
        self.timeseries       = data_loader.convert_oco2mip_unit(nbp_time, self.area)
        self.season_cyc       = data_loader.get_season_cycle(self.timeseries, self.name)
        print('OCO2 MIP done')
class ProcessTM5GOSAT:
    def __init__(self,settings):
        self.start_date     = settings['start_date']
        self.end_date       = settings['end_date']
        self.dates          = data_loader.create_date(self.start_date, self.end_date)
        self.year           = settings['year']
        self.name           = name_dic.tm5gosat_names
        self.region         = name_dic.transcom[settings['region']]
        self.area           = self.region['area']
        self.path           = settings['path']
        self.fname          = settings['TM5GOSAT_fname']

        tm5gosat_fname        = os.path.join(self.path, self.fname)
        nbp_spatial, nbp_time = data_loader.load_data(tm5gosat_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial          = nbp_spatial
        self.timeseries       = data_loader.convert_tm5gosat_unit(nbp_time, self.area)
        self.season_cyc       = data_loader.get_season_cycle(self.timeseries, self.name)
        print('TM5 GOSAT done')
class ProcessTM5IS:
    def __init__(self, settings):
        self.start_date    = settings['start_date']
        self.end_date      = settings['end_date']
        self.dates         = data_loader.create_date(self.start_date, self.end_date)
        self.year          = settings['year']
        self.name          = name_dic.tm5is_names
        self.region        = name_dic.transcom[settings['region']]
        self.area          = self.region['area']
        self.path          = settings['path']
        self.fname         = settings['TM5insitu_fname']

        tm5is_fname           = os.path.join(self.path, self.fname)
        nbp_spatial, nbp_time = data_loader.load_data(tm5is_fname, self.name, self.start_date, self.end_date, self.region)
        nbp_spatial['TM5-4DVAR']     = nbp_spatial['TM5-4DVAR']
        nbp_spatial['CarbonTracker'] = nbp_spatial['CarbonTracker'] * 86400 * (1000/44)
        nbp_spatial['CAMS']          = nbp_spatial['CAMS'] * (1/30) * 1000
        self.spatial          = nbp_spatial
        self.timeseries       = data_loader.convert_tm5is_unit(nbp_time, self.area)
        self.season_cyc       = data_loader.get_season_cycle(self.timeseries, self.name)
        print('TM5 IS done')
class ProcessTM5Prior:
    def __init__(self, settings):
        self.start_date = settings['start_date']
        self.end_date = settings['end_date']
        self.dates = data_loader.create_date(self.start_date, self.end_date)
        self.year = settings['year']
        self.name = name_dic.prior_names
        self.region = name_dic.transcom[settings['region']]
        self.area = self.region['area']
        self.path = settings['path']
        self.fname = settings['TM5insitu_fname']

        tm5is_fname = os.path.join(self.path, self.fname)
        nbp_spatial, nbp_time = data_loader.load_data(tm5is_fname, self.name, self.start_date,self.end_date, self.region)
        self.spatial = nbp_spatial
        self.timeseries = data_loader.convert_tm5prior_unit(nbp_time, self.area)
        self.season_cyc = data_loader.get_season_cycle(self.timeseries, self.name)
class ProcessFire:
    def __init__(self, settings):
        self.start_date  = settings['start_date']
        self.end_date    = settings['end_date']
        self.dates       = data_loader.create_date(self.start_date, self.end_date)
        self.year        = settings['year']
        self.name        = name_dic.fire_names
        self.region      = name_dic.transcom[settings['region']]
        self.area        = self.region['area']
        self.path        = settings['path']
        self.fname       = settings['firedataset_fname']

        fire_fname              = os.path.join(self.path, self.fname)
        fire_spatial, fire_time = data_loader.load_data(fire_fname, self.name, self.start_date, self.end_date, self.region)
        fire_spatial['gfed']    = fire_spatial['gfed'] * (1/30)
        fire_spatial['gfas'] = fire_spatial['gfas'] * 86400 * 1000 * (12 / 44)
        fire_spatial['finn'] = fire_spatial['finn'] * 86400 * 1000 * (12 / 44)
        self.spatial            = fire_spatial
        self.timeseries         = data_loader.convert_firedataset_unit(fire_time, self.area)
        self.season_cyc         = data_loader.get_season_cycle(self.timeseries, self.name)
        print('Fire dataset done')
class ProcessSIF:
    def __init__(self, settings):
        self.start_date         = settings['start_date']
        self.end_date           = settings['end_date']
        self.dates              = data_loader.create_date(self.start_date, self.end_date)
        self.year               = settings['year']
        self.name               = name_dic.sif_names
        self.region             = name_dic.transcom[settings['region']]
        #self.region['lon_min']  = self.region['lon_min'] + 180
        #self.region['lon_max']  = self.region['lon_max'] + 180
        self.area               = self.region['area']
        self.path               = settings['path']
        self.fname              = settings['SIF_fname']

        sif_fname              = os.path.join(self.path, self.fname)
        sif_spatial, sif_time = data_loader.load_data(sif_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial            = sif_spatial
        self.timeseries         = sif_time
        #self.timeseries         = data_loader.convert_sif_unit(sif_time, self.area)
        self.season_cyc         = data_loader.get_season_cycle(self.timeseries, self.name)
class ProcessSIFbaseGPP:
    def __init__(self, settings):
        self.start_date         = settings['start_date']
        self.end_date           = settings['end_date']
        self.dates              = data_loader.create_date(self.start_date, self.end_date)
        self.year               = settings['year']
        self.name               = name_dic.est_GPP
        self.region             = name_dic.transcom[settings['region']]
        #self.region['lon_min']  = self.region['lon_min'] + 180
        #self.region['lon_max']  = self.region['lon_max'] + 180
        self.area               = self.region['area']
        self.path               = settings['path']
        self.fname              = settings['est_GPP']

        sif_fname              = os.path.join(self.path, self.fname)
        sif_spatial, sif_time = data_loader.load_data(sif_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial            = sif_spatial
        self.timeseries         = sif_time
        self.timeseries         = data_loader.convert_sif_unit(sif_time, self.area)
        self.season_cyc         = data_loader.get_season_cycle(self.timeseries, self.name)
class ProcessFluxcom:
    def __init__(self, settings):
        self.start_date = settings['start_date']
        self.end_date = settings['end_date']
        self.dates = data_loader.create_date(self.start_date, self.end_date)
        self.year = settings['year']
        self.name = name_dic.fluxcom_vars
        self.region = name_dic.transcom[settings['region']]
        self.area = self.region['area']
        self.path = settings['path']
        self.fname = settings['FLUXCOM_fname']

        flux_fname = os.path.join(self.path, self.fname)
        flux_spatial, flux_time = data_loader.load_data(flux_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial = flux_spatial
        self.timeseries = flux_time
        self.timeseries         = data_loader.convert_fluxcom_unit(flux_time, self.area)
        self.season_cyc = data_loader.get_season_cycle(self.timeseries, self.name)
        print('FLUXCOM done')
class ProcessFluxcomX:
    def __init__(self, settings):
        self.start_date = settings['start_date']
        self.end_date = settings['end_date']
        self.dates = data_loader.create_date(self.start_date, self.end_date)
        self.year = settings['year']
        self.name = name_dic.fluxcom_x_vars
        self.region = name_dic.transcom[settings['region']]
        self.area = self.region['area']
        self.path = settings['path']
        self.fname = settings['FLUXCOM_X_fname']

        flux_fname = os.path.join(self.path, self.fname)
        flux_spatial, flux_time = data_loader.load_data(flux_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial = flux_spatial
        self.timeseries = flux_time
        self.timeseries = data_loader.convert_fluxcom_unit(flux_time, self.area)
        self.season_cyc = data_loader.get_season_cycle(self.timeseries, self.name)
        print('FLUXCOM_X done')
class ProcessERA5:
    def __init__(self, settings):
        self.start_date = settings['start_date']
        self.end_date = settings['end_date']
        self.dates = data_loader.create_date(self.start_date, self.end_date)
        self.year = settings['year']
        self.name = name_dic.ERA5_vars
        self.region = name_dic.transcom[settings['region']]
        self.area = self.region['area']
        self.path = settings['path']
        self.fname = settings['ERA5_fname']

        flux_fname = os.path.join(self.path, self.fname)
        flux_spatial, flux_time = data_loader.load_data(flux_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial = flux_spatial
        self.timeseries = flux_time
        #self.timeseries = data_loader.convert_fluxcom_unit(flux_time, self.area)
        self.season_cyc = data_loader.get_season_cycle(self.timeseries, self.name)
        print('ERA5 done')
class ProcessLai:
    def __init__(self, settings):
        self.start_date = settings['start_date']
        self.end_date = settings['end_date']
        self.dates = data_loader.create_date(self.start_date, self.end_date)
        self.year = settings['year']
        self.name = name_dic.MODIS_vars
        self.region = name_dic.transcom[settings['region']]
        self.area = self.region['area']
        self.path = settings['path']
        self.fname = settings['MODIS_fname']

        modis_fname = os.path.join(self.path, self.fname)
        modis_spatial, modis_time = data_loader.load_data(modis_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial = modis_spatial
        self.timeseries = modis_time
        self.season_cyc = data_loader.get_season_cycle(self.timeseries, self.name)
        print('LAI done')
class ProcessNIRvGPP:
    def __init__(self, settings):
        self.start_date = settings['start_date']
        self.end_date = '2017-12-31'
        self.dates = data_loader.create_date(self.start_date, self.end_date)
        self.year = settings['year']
        self.name = ['GPP']
        self.region = name_dic.transcom[settings['region']]
        self.area = self.region['area']
        self.path = settings['path']
        self.fname = settings['NIRvGPP']

        modis_fname = os.path.join(self.path, self.fname)
        modis_spatial, modis_time = data_loader.load_data(modis_fname, self.name, self.start_date, self.end_date, self.region)
        self.spatial = modis_spatial
        modis_time['GPP'] = modis_time['GPP'] * modis_time['days'] * self.area * 1e-12 * 0.001
        self.timeseries = modis_time
        self.season_cyc = data_loader.get_season_cycle(self.timeseries, ['GPP'])
        print('NIRvGPP done')
def process_trendy_nbp(setting):
    nbp = ProcessTRENDY(setting, 'nbp')
    return nbp
def process_trendy_ra(setting):
    ra = ProcessTRENDY(setting, 'ra')
    return ra
def process_trendy_rh(setting):
    rh = ProcessTRENDY(setting, 'rh')
    return rh
def process_trendy_gpp(setting):
    gpp = ProcessTRENDY(setting, 'gpp')
    return gpp
def process_trendy_fLuc(setting):
    fLuc = ProcessTRENDY(setting, 'fLuc')
    return fLuc
def process_trendy_fFire(setting):
    fFire = ProcessTRENDY(setting, 'fFire')
    return fFire
def process_trendy_lai(setting):
    lai = ProcessTRENDY(setting, 'lai')
    return lai
def process_data(func, setting):
    return func(setting)
class ProcessAll:
    def __init__(self, setting):
        self.var = ['fLuc','fFire','nbp','ra','rh','gpp']
        self.setting = setting
        self.trendy = {
            'nbp':None, 'ra':None, 'rh':None, 'gpp':None, 'fLuc':None, 'fFire':None, 'lai':None
        }
        self.insitu = {
            'nbp':None
        }
        self.gosat  = {
            'nbp':None, 'prior':None
        }
        self.oco = {
            'nbp': None
        }
        self.gome   = {
            'sif':None
        }
        #self.modis  = {
        #    'lai':None,
        #}
        self.modis = None
        self.fire   = {
            'fire':None
        }
        self.era5   = None
        self.fluxcom = {
            'gpp':None
        }
        self.fluxcom_x = {
            'gpp':None
        }
        self.oco2mip = {
            'nbp':None
        }
        self.est = {
            'sifgpp':None,
            'nirvgpp':None
        }
        self.concentration = {
            'REMOTEC':None,
            'ACOS':None
        }

    def excicute(self):
        functions = [process_trendy_nbp,
                     process_trendy_ra,
                     process_trendy_rh,
                     process_trendy_gpp,
                     process_trendy_fLuc,
                     process_trendy_fFire,
                     process_trendy_lai,
                     ProcessTM5GOSAT,
                     ProcessTM5IS,
                     ProcessFire,
                     ProcessFluxcom,
                     ProcessFluxcomX,
                     ProcessTM5Prior,
                     ProcessLai,
                     ProcessSIF,
                     ProcessERA5,
                     ProcessOCO,
                     ProcessOCO2MIP,
                     ProcessSIFbaseGPP,
                     ProcessNIRvGPP]
        with multiprocessing.Pool(processes=len(functions), ) as pool:
            results = [pool.apply_async(process_data, args=(func, self.setting)) for func in functions]
            pool.close()
            pool.join()
        print('process finish')
        results = [res.get() for res in results]

        self.trendy['nbp']    = results[0]
        self.trendy['ra']     = results[1]
        self.trendy['rh']     = results[2]
        self.trendy['gpp']    = results[3]
        self.trendy['fLuc']   = results[4]
        self.trendy['fFire']  = results[5]
        self.trendy['lai']    = results[6]
        self.gosat['nbp']     = results[7]
        self.insitu['nbp']    = results[8]
        self.fire['fire']     = results[9]
        self.fluxcom['gpp']   = results[10]
        self.fluxcom_x['gpp'] = results[11]
        self.gosat['prior']   = results[12]
        self.modis            = results[13]
        self.gome['sif']      = results[14]
        self.era5             = results[15]
        self.oco['nbp']       = results[16]
        self.oco2mip['nbp']   = results[17]
        self.est['sifgpp']    = results[18]
        self.est['nirvgpp']   = results[19]
        self.concentration['REMOTEC'] = pd.read_csv(self.setting['REMOTEC'])
        self.concentration['ACOS']    = pd.read_csv(self.setting['ACOS'])
        return self
class Process_lev2:
    def __init__(self,data,obj,ref,ref_value):
        self.start_date = data.start_date
        self.end_date = data.end_date
        self.dates = data_loader.create_date(self.start_date, self.end_date)
        self.year = data.year
        self.region = data.region
        self.region['name'] = data.region['name'] + '_' + ref+str(ref_value)
        if obj == 'trendyv11':
            self.name = name_dic.trendy_names_v11
            self.good_name = data.good_name
            self.bad_name = data.bad_name
        elif obj == 'tm5gosat':
            self.name = name_dic.tm5gosat_names
        elif obj == 'tm5is':
            self.name = name_dic.tm5is_names
        elif obj == 'gosatprior':
            self.name = name_dic.tm5_prior
        elif obj == 'lai':
            self.name = name_dic.MODIS_vars
        elif obj == 'sif':
            self.name = name_dic.sif_names
        elif obj == 'firedataset':
            self.name = name_dic.fire_names
        elif obj == 'era5':
            self.name = name_dic.ERA5_vars


        #self.region = name_dic.transcom[data.region]
        #self.area = self.region['area']

        spatial, time = data_loader.load_data_lev2(data.spatial, self.name, self.dates, ref,ref_value)
        self.spatial = spatial
        if obj == 'trendyv11':
            time = data_loader.convert_trendy_unit(time, 1e6)
        elif obj == 'tm5gosat':
            time = data_loader.convert_tm5gosat_unit(time,1e6)
        elif obj == 'tm5is':
            time = data_loader.convert_tm5is_unit(time,1e6)
        elif obj == 'gosatprior':
            time = data_loader.convert_tm5prior_unit(time, 1e6)
        elif obj == 'firedataset':
            time = data_loader.convert_firedataset_unit(time, 1e6)
        elif obj == 'lai':
            time = time
        elif obj == 'sif':
            time = time
        self.timeseries = time
        self.season_cyc = data_loader.get_season_cycle(self.timeseries, self.name)
        if obj == 'trendyv11':
            self.good_timeser = self.timeseries[self.good_name].mean(axis=1)
            self.good_timeser_std = self.timeseries[self.good_name].std(axis=1)
            self.bad_timeser = self.timeseries[self.bad_name].mean(axis=1)
            self.bad_timeser_std = self.timeseries[self.bad_name].std(axis=1)
            self.season_cyc = data_loader.get_season_cycle(self.timeseries, self.name)
            self.good_season = data_loader.get_season_cycle(self.timeseries, self.good_name)
            self.bad_season = data_loader.get_season_cycle(self.timeseries, self.bad_name)
if __name__ == '__main__':
    import pickle
    path    = "/home/mhuang/mycode/pkl"
    setting = input.Africa_05N15N
    data    = ProcessAll(setting).excicute()
    save_file = os.path.join(path, setting['region'].replace(" ", "_") + ".pkl")
    print(save_file)
    with open(save_file, "wb") as file:
        pickle.dump(data, file)
