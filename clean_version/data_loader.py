import os
import xarray as xr
import pandas as pd
import warnings
import numpy as np
import matplotlib.pyplot as plt
import datetime

import name_dic

warnings.filterwarnings("ignore")

def grid_area(lat,lon,resolution,check):
    """
    Calculate the subregion area in a given resolution
    :param lat: list of the latitudes in subregion
    :param lon: list of the longitudes in subregion
    :param resolution: resolution of grid [1,1]
    :param check: if == 'check', scatter the points to see if get the wanted region
    :return: area of the subregion
    """
    print('Resolution: ',resolution[1],'x',resolution[0], '   calculating area of grid cell... ')
    #print('Points latitudes: ',lat)
    #print('Points longitudes: ',lon)
    lat_lb, lat_ub, lon_lb, lon_ub = lat-resolution[1]/2, lat+resolution[1]/2, lon-resolution[0]/2, lon+resolution[0]/2
    R = 6371  # earth radius, km
    transfer = np.pi/180
    lat_lb, lat_ub, lon_lb, lon_ub = lat_lb*transfer, lat_ub*transfer, lon_lb*transfer, lon_ub*transfer
    cell_area = (np.sin(lat_ub)-np.sin(lat_lb))*(lon_ub-lon_lb)*R**2
    if check == 'check':
        fig = plt.figure(figsize=(8, 4))
        plt.scatter(lon, lat,s=3,marker='s')
        plt.xlim(-180,180)
        plt.ylim(-90,90)
        #plt.title('Points in box: {}, {}, {}, {}'.format(lon.min(), lon.max(), lat.min(), lat.max()))
        plt.show()

    print('Grid counts: ', np.shape(cell_area))
    total_area = np.sum(cell_area) * 1e6
    print('Total area: ', total_area, ' km2')
    return total_area

def create_date(start_date,end_date):
    """
    Function to create the date list and date range for datasets
    :param start_date: the start date, str
    :param end_date:   the end date, str
    :return:
    datelist
    """
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    date_list = date_range.strftime('%Y-%m').tolist()
    date_dict = {
        'range': date_range,
        'list': date_list
    }
    return date_dict

def load_data(fname,members,start_date, end_date,transcom_region):
    """
    read data in transcom continental scale:

    :param fname:            Dataset file name
    :param members:          Dataset members name
    :param dates:            Dictionary with date range and datelist
    :param transcom_region:  Dictionary with region info:
                             transcom region name, transcom region area, transcom region id

    :return:var_spatial:     Spatial time-series dataset in the rectangle region,
                             dim = [time, lat, lon]
    :return:var_time:        Spatial mean time-series dataset in the rectangle region,
                             [members, mean, SD, year, month, days]
    """
    #print('============================== Reading data ============================== ')
    #print('file: ', fname)
    #print('region: ', transcom_region['name'],', ','area: ', transcom_region['area'])
    #print('lon min: ', transcom_region['lon_min'],' ','lon max: ', transcom_region['lon_max'],' ','lat min: ',
    #      transcom_region['lat_min'],' ','lat max: ', transcom_region['lat_max'])

    data = xr.open_dataset(fname).sel(time=slice(pd.Timestamp(start_date), pd.Timestamp(end_date)))
    #print(slice(pd.Timestamp(start_date), pd.Timestamp(start_date)))
    dates = create_date(start_date, end_date)
    var_time = pd.DataFrame(columns=members, index=dates['list'])
    """
    tr = data.transcom_regions.values.copy()
    for i in range(1,179):
        for j in range(1,359):
            if data.transcom_regions[i,j] == transcom_region['id']:
                #print(i,j)
                tr[i+1,j] = transcom_region['id']
                tr[i - 1, j] = transcom_region['id']
                tr[i , j+1] = transcom_region['id']
                tr[i, j-1] = transcom_region['id']

    data.transcom_regions.values = tr
    """
    print(transcom_region['id'])
    var_spatial = data.where((data.transcom_regions.isin(transcom_region['id']))
                             #& (data.landseamask <= 60)
                             & (data.lon >= transcom_region['lon_min'])
                             & (data.lon <= transcom_region['lon_max'])
                             & (data.lat >= transcom_region['lat_min'])
                             & (data.lat <= transcom_region['lat_max'])
                             #& (data.country_id.isin(transcom_region['country']))
                             ,np.nan)
    print(np.unique(var_spatial.transcom_regions.values))
    #print(pd.Timestamp(dates['list'][-1]))
    #print(var_spatial.time)
    #var_spatial = var_spatial.sel(time=slice(pd.Timestamp(start_date), pd.Timestamp(end_date)))
    for member in members:
        if member in list(var_spatial.keys()):
            #print(member)
            value=[]
            #print('Calculating ', member, ' month mean ...')
            #print(len(dates['list']))
            for i in range(len(dates['list'])):
                var_spatial[member] = var_spatial[member].where(var_spatial[member]!=-9999,0)
                value.append(np.nanmean(var_spatial[member][i,:,:]))
                #print('finish')
                """
                mont = var_spatial[member][i,:,:]
                monmean = mont.sel(lon=slice(transcom_region['lat_min'],transcom_region['lat_max']),
                                   lat=slice(transcom_region['lon_min'],transcom_region['lon_max']))
                value.append(np.nanmean(monmean))
                """
                """
                value.append(np.nanmean(var_spatial[member][i,transcom_region['lat_min']:transcom_region['lat_max'],
                                        transcom_region['lon_min']:transcom_region['lon_max']].values))
                """
            var_time[member] = value

    var_time['mean'] = var_time.mean(axis=1)
    var_time['SD']   = var_time.std(axis=1)

    var_time['year'] = dates['range'].strftime('%Y').tolist()
    var_time['month'] = dates['range'].strftime('%m').tolist()
    var_time['year'] = var_time['year'].astype(int)
    var_time['month'] = var_time['month'].astype(int)
    var_time['days'] = var_time['month'].astype(int)

    i = 0
    # print(select_gpp['days'][0:1])
    for yr in var_time['year']:
        for mon in var_time['month']:
            if mon in (1, 3, 5, 7, 8, 10, 12):
                var_time['days'][i:i + 1] = 31
                i = i + 1
            if mon in (4, 6, 9, 11):
                var_time['days'][i:i + 1] = 30
                i = i + 1
            if yr in (2009, 2010, 2011, 2013, 2014, 2015, 2017, 2018, 2019) and mon == 2:
                var_time['days'][i:i + 1] = 28
                i = i + 1
            if yr in (2012, 2016, 2020) and mon == 2:
                var_time['days'][i:i + 1] = 29
                i = i + 1
    #print(var_time)
    #print('Module: load_continent complete')
    #plt.pcolormesh(var_spatial.lon, var_spatial.lat,var_spatial.CLASSIC[0,:,:])
    #plt.show()
    return var_spatial,var_time

def load_data_lev2(data, members, dates, ref, ref_value):
    var_spatial = data.where((data[ref].isin(ref_value))
                             , np.nan)
    var_time = pd.DataFrame(columns=members, index=dates['list'])
    for member in members:
        if member in list(var_spatial.keys()):
            value=[]
            #print('Calculating ', member, ' month mean ...')
            for i in range(len(dates['list'])):
                value.append(np.nanmean(var_spatial[member][i,:,:]))
                """
                mont = var_spatial[member][i,:,:]
                monmean = mont.sel(lon=slice(transcom_region['lat_min'],transcom_region['lat_max']),
                                   lat=slice(transcom_region['lon_min'],transcom_region['lon_max']))
                value.append(np.nanmean(monmean))
                """
                """
                value.append(np.nanmean(var_spatial[member][i,transcom_region['lat_min']:transcom_region['lat_max'],
                                        transcom_region['lon_min']:transcom_region['lon_max']].values))
                """
            var_time[member] = value

    var_time['mean'] = var_time.mean(axis=1)
    var_time['SD']   = var_time.std(axis=1)

    var_time['year'] = dates['range'].strftime('%Y').tolist()
    var_time['month'] = dates['range'].strftime('%m').tolist()
    var_time['year'] = var_time['year'].astype(int)
    var_time['month'] = var_time['month'].astype(int)
    var_time['days'] = var_time['month'].astype(int)

    i = 0
    # print(select_gpp['days'][0:1])
    for yr in var_time['year']:
        for mon in var_time['month']:
            if mon in (1, 3, 5, 7, 8, 10, 12):
                var_time['days'][i:i + 1] = 31
                i = i + 1
            if mon in (4, 6, 9, 11):
                var_time['days'][i:i + 1] = 30
                i = i + 1
            if yr in (2009, 2010, 2011, 2013, 2014, 2015, 2017, 2018, 2019, 2021) and mon == 2:
                var_time['days'][i:i + 1] = 28
                i = i + 1
            if yr in (2012, 2016, 2020) and mon == 2:
                var_time['days'][i:i + 1] = 29
                i = i + 1
    #print(var_time)
    #print('Module: load_continent complete')
    #plt.pcolormesh(var_spatial.lon, var_spatial.lat,var_spatial.CLASSIC[0,:,:])
    #plt.show()
    return var_spatial,var_time

def load_gosat_con(remofile, acosfile, dates):
    years  = np.unique(dates['range'].year)
    months = np.unique(dates['range'].month)
    data   = pd.DataFrame(columns=['RemoTeC', 'ACOS', 'mean', 'year', 'month'])
    remo   = pd.read_csv(remofile)
    acos   = pd.read_csv(acosfile)
    for yr in years:
        for mn in months:
            #print(yr, mn)
            ds1 = remo[
                (remo['Year'] == yr)
                & (remo['Month'] == mn)
                & (remo['land_flag'] == 0) # 0 land
                #& (remo['gain']== 'H')
                ]
            remo_mean = ds1['CO2'].mean()
            ds2 = acos[
                (acos['Year'] == yr)
                & (acos['Month'] == mn)
                & (acos['land_frac'] >= 50)
                & (acos['quality'] == 0)
                ]
            acos_mean = ds2['CO2'].mean()
            new_row = pd.DataFrame({
                'RemoTeC': [remo_mean],
                'ACOS': [acos_mean],
                'year': [yr],
                'month': [mn]
            })
            data = pd.concat([data, new_row], ignore_index=True)
    data['mean'] = (data['RemoTeC'] + data['ACOS']) /2
    return data

def load_remotec_con(path, transcom_region):
    print(path)
    remotec = []
    remotec_xco2 = []
    remotec_xco2_monmean = []
    lat = []
    lon = []
    yr= []
    month = []
    years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017','2018']
    for year in years:
        remotec.append(xr.open_dataset(path + year + '.nc'))
    remotec.append(xr.open_dataset('/mnt/data/users/eschoema/GOSAT/NetCDF_files_withCH4/fp_short_fil_corr_210210_2018.nc'))
    for i in range(11):
        print(np.unique(remotec[i].year))
        remotec[i] = remotec[i].where(
            (remotec[i].longitude >= transcom_region['lon_min'])
            & (remotec[i].longitude <= transcom_region['lon_max'])
            & (remotec[i].latitude >= transcom_region['lat_min'])
            & (remotec[i].latitude <= transcom_region['lat_max'])
        )
        for key, values in remotec[i].groupby('month'):
            if i == 9 and key == 3:
                pass
            else:
                print(key)
                remotec_xco2.extend(values.xco2.values)
                remotec_xco2_monmean.append(np.nanmean(values.xco2.values))
                lat.extend(values.latitude.values)
                lon.extend(values.longitude.values)
                yr.extend(values.year.values)
                month.extend(values.month.values)

    data = dict.fromkeys(['xco2','xco2_monmean', 'lat','lon','year','month'])
    data['xco2'] = remotec_xco2
    data['xco2_monmean'] = remotec_xco2_monmean
    data['lat'] = lat
    data['lon'] = lon
    data['year'] = yr
    data['month'] = month
    return data

def load_acos_con(path):
    print(path)
    acos_xco2_monmean = []
    data = xr.open_dataset(os.path.join(path, 'acos.nc4'))
    print(data)
    data['year'] = data['time'].dt.year
    print(data['year'].values)
    data['month'] = data['time'].dt.month

    # Group by year and month, then calculate the mean
    for yr, yr_value in data.groupby('year'):
        if yr == 2019:
            pass
        elif yr == 2014:
            print(yr)
            for month, month_value in yr_value.groupby('month'):
                if month == 12:
                    print(month, np.nanmean(month_value.xco2.values))
                    acos_xco2_monmean.append(np.nanmean(month_value.xco2.values))
                    acos_xco2_monmean.append(np.nan)
                else:
                    print(month, np.nanmean(month_value.xco2.values))
                    acos_xco2_monmean.append(np.nanmean(month_value.xco2.values))

        else:
            print(yr)
            for month, month_value in yr_value.groupby('month'):
                print(month, np.nanmean(month_value.xco2.values))
                acos_xco2_monmean.append(np.nanmean(month_value.xco2.values))

    acos = dict.fromkeys(['xco2', 'xco2_monmean', 'lat', 'lon', 'year', 'month'])
    acos['xco2'] = data.xco2.values
    acos['xco2_monmean'] = acos_xco2_monmean
    acos['lat'] = data.latitude.values
    acos['lon'] = data.longitude.values
    acos['year'] = data.date.values[:,0],
    acos['month'] = data.date.values[:,1]
    return acos

def load_tm5_4dvar_con(path,transcom_region,trans):
    data = xr.open_mfdataset(os.path.join(path,'*.nc'), combine='nested', concat_dim='tracer')
    data = data.sel(tracer=slice('2009-04-01','2018-12-31'))
    tm5  = dict.fromkeys(['xco2_monmean', 'time'])
    data =  data.where(
            (data.lon >= transcom_region['lon_min'])
            & (data.lon <= transcom_region['lon_max'])
            & (data.lat >= transcom_region['lat_min'])
            & (data.lat <= transcom_region['lat_max'])
            & (trans.transcom_regions == transcom_region['id'])
        )
    #print(data.mix)
    xco2_monmean = data.mix.mean(dim=['lat', 'lon'])
    #print(xco2_monmean.values[:,0].shape)
    tm5['xco2_monmean'] = xco2_monmean.values[:,0]
    tm5['time'] = data.tracer.values
    return tm5

def load_carbontracker_con(path,transcom_region,trans):
    data = xr.open_dataset(os.path.join(path,'CT2022_regrid.nc'))
    data = data.sel(time=slice('2009-04-01','2018-12-31'))
    data = data.where(
        (data.lon >= transcom_region['lon_min'])
        & (data.lon <= transcom_region['lon_max'])
        & (data.lat >= transcom_region['lat_min'])
        & (data.lat <= transcom_region['lat_max'])
        & (trans.transcom_regions == transcom_region['id'])
    )
    for i in range(len(data.level)):
        la = data.co2 * data.air_mass
    co2a = la.sum(dim='level', skipna=True)/data.air_mass.sum(dim='level', skipna=True)
    xco2_monmean = co2a.mean(dim=['lat', 'lon'], skipna=True)
    ct = dict.fromkeys(['xco2_monmean', 'time'])
    ct['time'] = data.time.values
    ct['xco2_monmean'] = xco2_monmean.values
    return ct

def load_cams_con(path,transcom_region,trans):
    data = xr.open_mfdataset(os.path.join(path, '*.nc'), combine='nested', concat_dim='time')
    data = data.sel(time=slice('2009-04-01', '2018-12-31'))
    cams = dict.fromkeys(['xco2_monmean', 'time'])
    #print(np.unique(data.XCO2.values))
    data = data.where(
        #(data.lon >= transcom_region['lon_min'])
        #& (data.lon <= transcom_region['lon_max'])
        #& (data.lon >= transcom_region['lat_min'])
        #& (data.lon <= transcom_region['lat_max'])
         (trans.transcom_regions == transcom_region['id'])
    )
    #print(np.unique(data.XCO2.values))
    xco2_monmean = data.XCO2.mean(dim=['lat', 'lon'], skipna=True)
    #print(xco2_monmean.values.shape)
    cams['xco2_monmean'] = xco2_monmean.values
    cams['time'] = data.time.values

    """
    xco2_monmean = []
    data = xr.open_dataset(os.path.join(path, 'cams.nc'))
    data = data.where(
        (data.longitude >= transcom_region['lon_min'])
        & (data.longitude <= transcom_region['lon_max'])
        & (data.latitude >= transcom_region['lat_min'])
        & (data.latitude <= transcom_region['lat_max'])
    )
    data['year'] = data['time'].dt.year
    print(data['year'].values)
    data['month'] = data['time'].dt.month
    data = data.sel(time=slice("2009-04-01","2018-12-31"))
    xco2_monmean = data.CO2.mean(dim=['latitude', 'longitude'], skipna=True)

    cams = dict.fromkeys(['xco2_monmean'])
    #cams['time'] = data.time.values
    cams['xco2_monmean'] = xco2_monmean.values*1e6
    """
    return cams

def load_tp(fname,members,dates,transcom_region):
    """
    read data in transcom continental scale:

    :param fname:            Dataset file name
    :param members:          Dataset members name
    :param dates:            Dictionary with date range and datelist
    :param transcom_region:  Dictionary with region info:
                             transcom region name, transcom region area, transcom region id

    :return:var_spatial:     Spatial time-series dataset in the rectangle region,
                             dim = [time, lat, lon]
    :return:var_time:        Spatial mean time-series dataset in the rectangle region,
                             [members, mean, SD, year, month, days]
    """
    #print('============================== Reading data ============================== ')
    #print('file: ', fname)
    #print('region: ', transcom_region['name'],', ','area: ', transcom_region['area'])
    #print('lon min: ', transcom_region['lon_min'],' ','lon max: ', transcom_region['lon_max'],' ','lat min: ',
    #      transcom_region['lat_min'],' ','lat max: ', transcom_region['lat_max'])

    data = xr.open_dataset(fname, decode_times=False)
    var_time = pd.DataFrame(columns=members, index=dates['list'])
    var_spatial = data.where((data.transcom_regions == transcom_region['id'])
                             & (data.lon >= transcom_region['lon_min'])
                             & (data.lon <= transcom_region['lon_max'])
                             & (data.lat >= transcom_region['lat_min'])
                             & (data.lat <= transcom_region['lat_max'])
                             ,np.nan)

    for member in members:
        if member in list(var_spatial.keys()):
            value=[]
            #print('Calculating ', member, ' month mean ...')
            for i in range(len(dates['list'])):
                value.append(np.nansum(var_spatial[member][i,:,:]))
                """
                mont = var_spatial[member][i,:,:]
                monmean = mont.sel(lon=slice(transcom_region['lat_min'],transcom_region['lat_max']),
                                   lat=slice(transcom_region['lon_min'],transcom_region['lon_max']))
                value.append(np.nanmean(monmean))
                """
                """
                value.append(np.nanmean(var_spatial[member][i,transcom_region['lat_min']:transcom_region['lat_max'],
                                        transcom_region['lon_min']:transcom_region['lon_max']].values))
                """
            var_time[member] = value

    var_time['mean'] = var_time.mean(axis=1)
    var_time['SD']   = var_time.std(axis=1)

    var_time['year'] = dates['range'].strftime('%Y').tolist()
    var_time['month'] = dates['range'].strftime('%m').tolist()
    var_time['year'] = var_time['year'].astype(int)
    var_time['month'] = var_time['month'].astype(int)
    var_time['days'] = var_time['month'].astype(int)

    i = 0
    # print(select_gpp['days'][0:1])
    for yr in var_time['year']:
        for mon in var_time['month']:
            if mon in (1, 3, 5, 7, 8, 10, 12):
                var_time['days'][i:i + 1] = 31
                i = i + 1
            if mon in (4, 6, 9, 11):
                var_time['days'][i:i + 1] = 30
                i = i + 1
            if yr in (2009, 2010, 2011, 2013, 2014, 2015, 2017, 2018, 2019) and mon == 2:
                var_time['days'][i:i + 1] = 28
                i = i + 1
            if yr in (2012, 2016, 2020) and mon == 2:
                var_time['days'][i:i + 1] = 29
                i = i + 1
    #print(var_time)
    #print('Module: load_continent complete')
    #plt.pcolormesh(var_spatial.lon, var_spatial.lat,var_spatial.CLASSIC[0,:,:])
    #plt.show()
    return var_spatial,var_time

def convert_trendy_unit(trendy_time, region_area):
    """
    Convert TRENDY variables unit from (kgC m-2 s-1) to (TgC month-1)

    :param trendy_time: Spatial mean time-series TRENDY datasets,
                        unit: kg m-2 s-1; variables: [members, mean, SD, year, month, days]
    :param region_area: TRENDY datasets area, unit: m2

    :return trendy_time:     Spatial mean time-series TRENDY datasets,
                        unit: TgC month-1; variables: [members, mean, SD]
    """
    trendy = trendy_time.iloc[:,0:20]
    for i in range(20):
        trendy.iloc[:,i] = trendy_time.iloc[:,i] * trendy_time['days'] * 86400 * region_area * 1e-9
    trendy['month'] = trendy_time['month']
    trendy['year']  = trendy_time['year']
    return trendy

def convert_tm5gosat_unit(gosat_time, region_area):
    """
    Convert TM5-GOSAT variables unit from (gC/m^2/day) to (TgC month-1)

    :param gosat_time:  Spatial mean time-series TM5-GOSAT datasets,
                        unit: kg m-2 s-1; variables: [members, mean, SD, year, month, days]
    :param region_area: TM5-GOSAT datasets area, unit: m2

    :return gosat_time:   Spatial mean time-series TM5-GOSAT datasets,
                        unit: TgC month-1; variables: [members, mean, SD]
    """
    for i in range(4):
        gosat_time.iloc[:, i] = gosat_time.iloc[:, i] * gosat_time['days'] * region_area * 1e-12
    return gosat_time

def convert_tm5prior_unit(is_time, region_area):
    """
    Convert TM5-GOSAT variables unit from (gC/m^2/day) to (TgC month-1)

    :param gosat_time:  Spatial mean time-series TM5-GOSAT datasets,
                        unit: kg m-2 s-1; variables: [members, mean, SD, year, month, days]
    :param region_area: TM5-GOSAT datasets area, unit: m2

    :return gosat_time:   Spatial mean time-series TM5-GOSAT datasets,
                        unit: TgC month-1; variables: [members, mean, SD]
    """
    """
        Convert TM5-insitu variables unit to (TgC month-1)
        CAMS           unit: kgC m-2 month-1
        Carbon Tracker unit: mol m-2 s-1
        TM5-4DVAR      unit: gC m-2 day-1

        :param is_time:     Spatial mean time-series TM5-insitu datasets,
                            unit: kg m-2 s-1; variables: [members, mean, SD, year, month, days]
        :param region_area: TM5-insitu datasets area, unit: m2

        :return tm5is:      Spatial mean time-series TM5-insitu datasets,
                            unit: TgC month-1; variables: [members, mean, SD]
        """
    tm5is = pd.DataFrame(columns=['CAMS_prior', 'CT_pri_cms', 'CT_pri_4p1s', 'TM5-4DVAR_prior', 'mean', 'SD', 'year', 'month'],
                         index=is_time.index)
    tm5is['CAMS_prior'] = is_time['CAMS_prior'] * region_area * 1e-9
    tm5is['CT_pri_cms'] = is_time['CT_pri_cms'] * 86400 * is_time['days'] * region_area * ((1e-9) / 44)
    tm5is['CT_pri_4p1s'] = is_time['CT_pri_4p1s'] * 86400 * is_time['days'] * region_area * ((1e-9) / 44)
    tm5is['TM5-4DVAR_prior'] = is_time['TM5-4DVAR_prior'] * is_time['days'] * region_area * 1e-12
    tm5is['mean'] = tm5is.iloc[:, 0:4].mean(axis=1)
    tm5is['SD'] = tm5is.iloc[:, 0:4].std(axis=1)
    tm5is['year'] = is_time['year']
    tm5is['month'] = is_time['month']
    # print(tm5is)
    return tm5is
    """
    for i in range(3):
        gosat_time.iloc[:, i] = gosat_time.iloc[:, i] * gosat_time['days'] * region_area * 1e-12
    return gosat_time"""


def convert_tm5is_unit(is_time, region_area):
    """
    Convert TM5-insitu variables unit to (TgC month-1)
    CAMS           unit: kgC m-2 month-1
    Carbon Tracker unit: mol m-2 s-1
    TM5-4DVAR      unit: gC m-2 day-1

    :param is_time:     Spatial mean time-series TM5-insitu datasets,
                        unit: kg m-2 s-1; variables: [members, mean, SD, year, month, days]
    :param region_area: TM5-insitu datasets area, unit: m2

    :return tm5is:      Spatial mean time-series TM5-insitu datasets,
                        unit: TgC month-1; variables: [members, mean, SD]
    """
    tm5is = pd.DataFrame(columns=['CAMS','CarbonTracker','TM5-4DVAR','mean','SD','year','month'], index=is_time.index)
    tm5is['CAMS']          = is_time['CAMS'] * region_area * 1e-9
    tm5is['CarbonTracker'] = is_time['CarbonTracker'] * 86400 * is_time['days'] * region_area * ((1e-9) / 44)
    tm5is['TM5-4DVAR']     = is_time['TM5-4DVAR'] * is_time['days'] * region_area * 1e-12
    tm5is['mean']          = tm5is.iloc[:, 0:3].mean(axis=1)
    tm5is['SD']            = tm5is.iloc[:, 0:3].std(axis=1)
    tm5is['year'] = is_time['year']
    tm5is['month'] = is_time['month']
    #print(tm5is)
    return tm5is
def convert_oco2mip_unit(oco2mip, region_area):
    """
    tm5is = pd.DataFrame(columns=['EnsMean', 'EnsStd','mean', 'SD', 'year', 'month'],
                         index=oco2mip.index)
    tm5is['EnsMean'] = oco2mip['EnsMean'] * region_area*(1/12)*1e-12
    tm5is['EnsStd']  = oco2mip['EnsStd'] * region_area*(1/12)*1e-12
    """
    for name in name_dic.oco2mip_names:
        oco2mip[name] = oco2mip[name] * region_area*(1/12)*1e-12
    return oco2mip
def convert_firedataset_unit(fire_time, region_area):
    """
    Convert fire datasets unit to (TgC month-1)
    GFED unit: g m-2 month-1
    GFAS unit: kg m-2 s-1
    FINN unit: kg m-2 s-1

    :param fire_time:    Spatial mean time-series fire datasets,
                         unit: kg m-2 s-1; variables: [members, mean, SD, year, month, days]
    :param region_area:  fire datasets area, unit: m2
    :return firedataset: Spatial mean time-series fire datasets,
                         unit: TgC month-1; variables: [members, mean, SD]
    """
    firedataset = pd.DataFrame(columns=['gfed', 'gfas', 'finn', 'mean', 'SD'], index=fire_time.index)
    firedataset['gfed']  = fire_time['gfed'] * region_area * 1e-12
    firedataset['gfas']  = fire_time['gfas'] * 86400 * fire_time['days'] * region_area * 1e-9 *(12/44)
    firedataset['finn']  = fire_time['finn'] * 86400 * fire_time['days'] * region_area * 1e-9 *(12/44)
    firedataset['mean']  = fire_time.iloc[:, 0:3].mean(axis=1)
    firedataset['SD']    = fire_time.iloc[:, 0:3].std(axis=1)
    firedataset['month'] = fire_time['month']
    return firedataset
def convert_sif_unit(sif_time, region_area):
    """
    Converts SIF unit from gC m-2 day to TgC month-1, GOSIF scaling factor: 1e-3
    :param sif_time:
    :param region_area:
    :return:
    """
    sif =  pd.DataFrame(columns=['GOME','GOSIF','month'], index=sif_time.index)
    sif['GOME'] = sif_time['GOME'] * sif_time['days'] * region_area * 1e-12
    sif['GOSIF']= sif_time['GOSIF'] * region_area * (1e-12) * (0.01)
    sif['month'] = sif_time['month']
    sif['days'] = sif_time['days']
    return sif

def convert_fluxcom_unit(fluxcom_time, region_area):
    """
    Converts fluxcom data unit from gC m-2 day-1 to TgC month
    :param fluxcom_time:
    :param region_area:
    :return:
    """
    for i in range(4):
        fluxcom_time.iloc[:, i] = fluxcom_time.iloc[:, i] * fluxcom_time['days'] * region_area * 1e-12
    return fluxcom_time

def get_season_cycle(data_time,members):
    """
    Calculate seasonal cycle
    :param data_time: Spatial mean time-series datasets
    :param members:   dataset members name
    :return seasonal cycle: seasonal cycle of Spatial mean time-series datasets, variables [members, mean, SD]
    """
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    season_cycle = pd.DataFrame(columns=members, index=months)

    for member in members:
        season_cycle[member] = data_time.groupby('month').mean()[member]
    season_cycle['mean'] = season_cycle.iloc[:, 0:len(members)].mean(axis=1, skipna=True)
    season_cycle['SD'] = season_cycle.iloc[:, 0:len(members)].std(axis=1, skipna=True)

    #print('season result')
    #print(season_cycle)
    return season_cycle

def detrend_go(data):
    # create background dataset
    rate = [1.58, 2.41, 1.69, 2.41, 2.43, 2.05, 2.94, 2.83, 2.16, 2.33, 2.57, 2.35, 2.60]  # updated on 02.06.2022
    detrend_all_month = []
    detrend_year = []
    detrend_month = []
    offset = 384.5  # 384.5

    for y in range(2009, 2019):
        if y == 2009:
            for m in range(4, 13):
                detrend_all_month.append(offset + rate[y - 2009] / 12 * (m - 4))
                detrend_month.append(m)
                detrend_year.append(y)
        else:
            for m in range(1, 13):
                detrend_all_month.append(detrend_all_month[-1] + rate[y - 2009] / 12)
                detrend_month.append(m)
                detrend_year.append(y)

    data = np.array(data)-np.array(detrend_all_month)
    return data

def detrend_is(data):
    rate = [1.58, 2.41, 1.69, 2.41, 2.43, 2.05, 2.94, 2.83, 2.16, 2.33, 2.57, 2.35, 2.60]  # updated on 02.06.2022
    detrend_all_month = []
    detrend_year = []
    detrend_month = []
    offset = 384.5  # 384.5
    for y in range(2009, 2019):
        if y == 2009:
            for m in range(1, 13):
                detrend_all_month.append(offset + rate[y - 2009] / 12 * (m - 4))
                detrend_month.append(m)
                detrend_year.append(y)
        else:
            for m in range(1, 13):
                detrend_all_month.append(detrend_all_month[-1] + rate[y - 2009] / 12)
                detrend_month.append(m)
                detrend_year.append(y)

    data = data - detrend_all_month
    return data

def doy_to_date(year, doy):
    base = datetime.datetime(year,1,1)
    time = base + datetime.timedelta(doy-1)
    time_str = time.strftime('%Y-%m-%d')
    return time_str

def read_asiaflux(fname, year,encoding):
    data = pd.read_csv(fname,encoding=encoding, skipinitialspace=True)
    data.columns = data.columns.str.strip()
    print(data)
    data = data.drop(index=0)

    data = data.astype(float)
    data = data.replace(-9999, np.nan)
    data = data.replace(-99999, np.nan)
    year = int(year)
    doys = data['DOY'].astype(int)
    dates= []
    for doy in doys:
        date = doy_to_date(year,int(doy))
        dates = np.append(dates, date)
    data['date'] = dates
    data['date'] = pd.to_datetime(data['date'])
    data = data.groupby('date').mean()
    return data