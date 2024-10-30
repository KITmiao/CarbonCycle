import datetime

import xarray as xr
import data_processor
import data_loader
from data_loader import doy_to_date
import input
import matplotlib.pyplot as plt
from forplot import plot_station
import pandas as pd
import os
import glob
import numpy as np

process_LHP = False
process_LHP_daily = False

process_JOP = False
process_JOP_daily = True

if process_LHP == True:
    root = '/mnt/data/users/mhuang/AsiaFlux/files/'
    file_pattern = os.path.join(root, 'FxMt_LHP_*.csv')
    file_list = glob.glob(file_pattern)

    if not file_list:
        raise FileNotFoundError(f"No files found for pattern: {file_pattern}")

    df_list = []
    for file in file_list:
        df = pd.read_csv(file)
        df = df.drop(index=0)
        df = df.replace(-9999, np.nan)
        df_list.append(df)

    LHP_Fxmt = pd.concat(df_list, ignore_index=True)
    LHP_Fxmt = LHP_Fxmt.astype(float)
    LHP_Fxmt=LHP_Fxmt.sort_values(by=['Year','DOY'])
    LHP_Fxmt = LHP_Fxmt.reset_index(drop=True)

    #years = LHP_Fxmt['Year'].astype(int)
    #doys  = LHP_Fxmt['DOY'].astype(int)
    #print(doys)
    dates  = []
    i=0
    years = [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
    for yr in years:
        df = LHP_Fxmt[LHP_Fxmt.Year.astype(float)==yr]
        doys = df['DOY'].astype(int)
        for doy in doys:
            i+=1

            date = doy_to_date(year=int(yr),doy=doy)
            print(yr, doy, date)
            dates=np.append(dates,date)

    LHP_Fxmt['Date'] = dates
    LHP_Fxmt.to_csv('/home/mhuang/data/AsiaFlux/FxMt_LHP_2009-2019.csv')
if process_LHP_daily == True:
    file = '/home/mhuang/data/AsiaFlux/FxMt_LHP_2009-2019.csv'
    df = pd.read_csv(file)
    LHP_Fxmt_daily = df.groupby('Date').mean()
    LHP_Fxmt_daily.to_csv('/home/mhuang/data/AsiaFlux/FxMt_LHP_2009-2019_daily.csv')
if process_JOP == True:
    root = '/mnt/data/users/mhuang/AsiaFlux/files/'
    file_pattern = os.path.join(root, 'FxMt_JOP_*.csv')
    file_list = glob.glob(file_pattern)

    if not file_list:
        raise FileNotFoundError(f"No files found for pattern: {file_pattern}")

    df_list = []
    for file in file_list:
        print(file)
        df = pd.read_csv(file)
        df = df.drop(index=0)
        df = df.replace('NA', np.nan)
        df_list.append(df)

    LHP_Fxmt = pd.concat(df_list, ignore_index=True)
    LHP_Fxmt = LHP_Fxmt.astype(float)
    LHP_Fxmt=LHP_Fxmt.sort_values(by=['Year','DOY'])
    LHP_Fxmt = LHP_Fxmt.reset_index(drop=True)

    #years = LHP_Fxmt['Year'].astype(int)
    #doys  = LHP_Fxmt['DOY'].astype(int)
    #print(doys)
    dates  = []
    i=0
    years = [2014,2015,2016,2017,2018,2019,2020]
    for yr in years:
        df = LHP_Fxmt[LHP_Fxmt.Year.astype(float)==yr]
        doys = df['DOY'].astype(int)
        for doy in doys:
            i+=1

            date = doy_to_date(year=int(yr),doy=doy)
            print(yr, doy, date)
            dates=np.append(dates,date)

    LHP_Fxmt['Date'] = dates
    LHP_Fxmt.to_csv('/home/mhuang/data/AsiaFlux/FxMt_JOP_2014-2020.csv')
if process_JOP_daily == True:
    file = '/home/mhuang/data/AsiaFlux/FxMt_JOP_2014-2020.csv'
    df = pd.read_csv(file)
    LHP_Fxmt_daily = df.groupby('Date').mean()
    LHP_Fxmt_daily.to_csv('/home/mhuang/data/AsiaFlux/FxMt_JOP_2014-2020_daily.csv')