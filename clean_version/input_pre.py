import xarray as xr
import numpy as np
co2con = {
    'path': '/mnt/data/users/eschoema',
    'PATH_TO_REMOTEC': '/mnt/data/users/eschoema/GOSAT/NetCDF_files_withCH4/',
    'PATH_TO_ACOS':'/mnt/data/users/eschoema/ACOS/ACOS_L2_Lite_FP.9r',
    'PATH_TO_TM5':'/mnt/data/users/eschoema/TK5_4DVAR/Molefractions/IS/output/2009010100-2019070100/mix',
    'PATH_TO_CAMS':'/mnt/data/users/eschoema/CAMS/MeanColumn',
    'OUT_PATH':'/home/mhuang/data/trendy/v11'
}
nbp = {
    'TRENDY_PATH':'/mnt/data/users/mhuang/trendy-v11',
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'VAR':'nbp',
    'START_DATE':'2009-01-01',
    'END_DATE':'2020-12-31',
    'START_DATE_OCO':'2014-09-01',
    'END_DATE_OCO':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'CABLE-POPv11':'/home/mhuang/data/trendy/v11/nbp_regrid/CABLE-POP_S3_nbp',
    'PATH_TO_GOSAT_IS':'/mnt/data/users/eschoema/TM5Inversion/glb3x2_20220413/new_gridded_flux',
    'REMOTEC':'flux_1x1_RemoTeC_2.4.0+IS.nc',
    'ACOS':'flux_1x1_ACOS+IS.nc',
    'PRIOR':'flux_1x1_prior.nc',
    'PATH_TO_IS':'/home/mhuang/data/otherdata',
    'TM5':'TM5-4DVAR.nc',
    'CAMS':'CAMS.nc',
    'CarbonTracker':'CarbonTracker.nc',
    'OCO':'/mnt/data/users/eschoema/TM5Inversion/OCO-2_flux/flux_1x1_LNLG.nc'
}

ra = {
    'TRENDY_PATH':'/mnt/data/users/mhuang/trendy-v11',
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'VAR':'ra',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc'
}

rh = {
    'TRENDY_PATH':'/mnt/data/users/mhuang/trendy-v11',
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'VAR':'rh',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc'
}

gpp = {
    'TRENDY_PATH':'/mnt/data/users/mhuang/trendy-v11',
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'VAR':'gpp',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc'
}

npp = {
    'TRENDY_PATH':'/mnt/data/users/mhuang/trendy-v11',
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'VAR':'npp',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc'
}

fFire = {
    'TRENDY_PATH':'/mnt/data/users/mhuang/trendy-v11',
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'VAR':'fFire',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc'
}

fLuc = {
    'TRENDY_PATH':'/mnt/data/users/mhuang/trendy-v11',
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'VAR':'fLuc',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc'
}

fire = {
    'PATH':'/home/mhuang/data/old/fire',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'OUT_PATH': '/home/mhuang/data/trendy/v11'
}

lai = {
    'TRENDY_PATH':'/mnt/data/users/mhuang/trendy-v11',
    'PATH_TO_MODIS':'/mnt/data/users/mhuang/modis_lai/modis_lai_fpar/global',
    'PATH_TO_MODIS_EVI':'/mnt/data2/users/mhuang/EVI/modis_aqua_vegetationindex/DATA',
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'VAR':['lai','fpar','evi','ndvi'],
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc'
}

is_nbp = {
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'PATH_TO_IS':'/home/mhuang/data/otherdata',
    'TM5':'TM5-4DVAR.nc',
    'TM5_pri':'/mnt/data/users/eschoema/TM5Inversion/glb3x2_20220413/new_gridded_flux/flux_1x1_prior.nc',
    'CAMS':'CAMS.nc',
    'CarbonTracker':'CarbonTracker.nc',
    'CarbonTracker_b4_pri':'CT2022_pri/CT2022_prior_b4.nc',
    'CarbonTracker_w4_pri':'CT2022_pri/CT2022_prior_w4.nc',
    'CarbonTracker_bc_pri':'CT2022_pri/CT2022_prior_bc.nc',
    'CarbonTracker_wc_pri':'CT2022_pri/CT2022_prior_wc.nc',
}

sif = {
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'PATH_TO_SIF':'/mnt/data/users/eschoema/SIF/GOME2', #/home/mhuang/data/otherdata
    'FNAME':'sif_monmean.nc',
    'VAR':'SIF'
}

sif_based_gpp = {
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'PATH_TO_SIF':'/home/mhuang/data/trendy/v11',
    'FNAME':'sif_based_gpp_noco2_0.5x0.5.nc',
    'VAR':'SIF',
    'OUT_FNAME':'sif_based_gpp_eraT_1x1.nc'
}
gosif = {
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'OUT_FNAME':'GOSIF1x1.nc',
    'TIF_PATH':'/mnt/data2/users/mhuang/GOSIF',
    'NC_PATH':'/home/mhuang/data/GOSIF',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'TIMEDIM_PATH':'/home/mhuang/data/GOSIF/same_grid/with_time_dim',
    'TARGET_GRID':xr.Dataset(
        {
            "lat": (["lat"], np.arange(-90, 90, 1.0)),
            "lon": (["lon"], np.arange(-180, 180, 1.0)),
        }
    )
}
gosif_gpp = {
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'OUT_FNAME':'GOSIF_GPP1x1.nc',
    'TIF_PATH':'/mnt/data2/users/mhuang/GOSIF_GPP',
    'NC_PATH':'/home/mhuang/data/GOSIF_GPP',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'TIMEDIM_PATH':'/home/mhuang/data/GOSIF_GPP/same_grid/with_time_dim',
    'TARGET_GRID':xr.Dataset(
        {
            "lat": (["lat"], np.arange(-90, 90, 1.0)),
            "lon": (["lon"], np.arange(-180, 180, 1.0)),
        }
    )
}
nirv_based_gpp = {
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'START_DATE':'2009-01-01',
    'END_DATE':'2017-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'PATH':'/mnt/data2/users/mhuang/NIRvGPP',
    'FNAME':'sif_based_gpp_rf_0.5x0.5.nc',
    'VAR':'GPP'
}
Koning2019 = {
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'IN_FILE':'/mnt/data2/users/mhuang/HeteroResp2.nc',
    'OUT_FILE':'/home/mhuang/data/trendy/v11/HeteroResp2_1x1.nc'
}
transcom = {
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'PATH_TO_FLUXCOM_X':'/mnt/data/users/eschoema/FLUXCOM-X',
    'PATH_TO_FLUXCOM':'/mnt/data/users/eschoema/FLUXCOM'
}

era5 = {
    'OUT_PATH':'/home/mhuang/data/trendy/v11',
    #'START_DATE':'1981-01-01',
    #'END_DATE':'2023-12-31',
    'START_DATE':'2009-01-01',
    'END_DATE':'2018-12-31',
    'TRANSCOM_FILE':'/home/mhuang/data/regions_regrid.nc',
    'PATH_TO_TP':'/mnt/data/users/eschoema/ERA5/aridity_global',
    'FNAME_TP':'total_precipitation.nc',
    #'PATH_TO_TP':'/home/mhuang/data/ERA5',
    #'FNAME_TP':'tp_1981-2024.nc',
    'PATH_TO_T2M':'/home/mhuang/data/ERA5',
    'FNAME_T2M':'t2m.nc',
    'PATH_TO_E':'/home/mhuang/data/ERA5',
    'FNAME_E':'data.nc',
    'PATH_TO_WIND':'/home/mhuang/data/ERA5',
    'FNAME_WIND':'era5_wind.nc',
    'PATH_TO_SWC':'/mnt/data/users/mhuang/ERA5_reanalysis',
    'FNAME_SWC':'swc.nc',
    'PATH_TO_SST':'/home/mhuang/data/nontrendy',
    'FNAME_SST':'sst.mon.mean.nc'
}