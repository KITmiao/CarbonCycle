import os
import numpy as np
import xarray as xr
import data_loader
import data_processor
import input
import name_dic
class GetSubregionArea:
    def __init__(self, settings):
        self.region = settings.region
        self.spatial = settings.spatial
        self.area    = settings.area
    def get_area(self):
        print('------------- Area test result -------------')
        print('Subregion name: ', self.region['name'])
        lat_min = self.region['lat_min']
        lat_max = self.region['lat_max']
        lon_min = self.region['lon_min']
        lon_max = self.region['lon_max']
        #lats, lons = np.where(self.spatial['transcom_regions'].values != 'nan')
        lats, lons = np.where(~np.isnan(self.spatial['transcom_regions'].values))
        x=np.unique(self.spatial['transcom_regions'].values)
        print(np.unique(self.spatial['transcom_regions'].values))
        S = data_loader.grid_area(self.spatial.lat[lats].values, self.spatial.lon[lons].values,
                               [1, 1], 'check')
        print('area in input: ', self.area, ' km2')
        print('difference: ' , S - self.area)
        return S

if __name__ == '__main__':
    # remember to change the transcom region id (get_area(self))!!!!
    setting = input.Africa_05N15N
    TRENDY = data_processor.ProcessTRENDY(setting, 'nbp')
    GetSubregionArea(TRENDY).get_area()
