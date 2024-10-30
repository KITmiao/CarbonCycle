import os
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import name_dic

def lim(min, max):
    scaler = 3
    lim = [min - scaler, max + scaler]
    return lim
class LatlonPlot():
    def __init__(self):
        pass
    def create_map(self, region):
        fig = plt.figure(figsize=[6, 3])
        ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
        lon_min = name_dic.transcom[region]['lon_min']
        lon_max = name_dic.transcom[region]['lon_max']
        lat_min = name_dic.transcom[region]['lat_min']
        lat_max = name_dic.transcom[region]['lat_max']
        ax.set_xlim(lim(lon_min, lon_max))
        ax.set_ylim(lim(lat_min, lat_max))
        ax.coastlines()
        gl = ax.gridlines(draw_labels=True, linestyle='--')
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xlines = False
        gl.ylines = False
        return fig, ax
    def create_map2(self, region, ax):
        lon_min = name_dic.transcom[region]['lon_min']
        lon_max = name_dic.transcom[region]['lon_max']
        lat_min = name_dic.transcom[region]['lat_min']
        lat_max = name_dic.transcom[region]['lat_max']
        ax.set_xlim(lim(lon_min, lon_max))
        ax.set_ylim(lim(lat_min, lat_max))
        ax.coastlines()
        gl = ax.gridlines(draw_labels=True, linestyle='--')
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xlines = False
        gl.ylines = False
        return ax
    def glb_map(self, ax):
        ax.coastlines()
        gl = ax.gridlines(draw_labels=True, linestyle='--')
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xlines = False
        gl.ylines = False
        return ax
    def cbar(self, fig, ax, map):
        cbar1 = fig.colorbar(map, ax=ax, extend='both', orientation='horizontal')
        cbar1.set_label('CO$_2$ flux (gC/m$^2$/day)')
        cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    def corelation_cbar(self, fig, ax, map):
        cbar1 = fig.colorbar(map, ax=ax, extend='both', orientation='horizontal')
        cbar1.set_label('Correlation')
        cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    def elev_spatial(self,ax):
        path = '/home/mhuang/data/trendy/v11'
        fname = 'GMTED2010_15n240_1000deg.nc'
        elev = xr.open_dataset(os.path.join(path, fname))
        contour = ax.contour(elev.longitude, elev.latitude, elev.elevation
                             , levels=10, colors='black', linewidths=0.5)


