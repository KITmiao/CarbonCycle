import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap
import os
import xarray as xr
import cartopy.crs as ccrs
import name_dic
import pandas as pd
def change_order(data, new_order):
    new_data = data.reindex(new_order).reset_index()
    return new_data
def visual_EOF(pcs, eofs, evfs, n, product):
    start = pcs.index[0].strftime("%Y-%m")
    end   = pcs.index[-1].strftime("%Y-%m")

    fig = plt.figure(figsize=[15, 3*(15/13)])
    ax = fig.add_subplot(121, projection=ccrs.PlateCarree(central_longitude=180))
    ax.coastlines()
    map = ax.pcolormesh(eofs.lon + 180, eofs.lat, eofs[n, :, :], cmap='seismic', vmin=-1, vmax=1)
    cbar1 = fig.colorbar(map, ax=ax, extend='both', orientation='horizontal')
    #ax.set_ylim(latrange)
    ax.set_title(f'EOF{int(n+1)}({product} from {start} to {end})', loc='left')
    ax.set_title('%.2f%%' % (evfs[n]*100), loc='right')
    gl = ax.gridlines(draw_labels=True, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    ax2 = fig.add_subplot(122)
    ax2.plot(pcs.index, pcs.iloc[:, n], color='b')
    ax2.axhline(0, linestyle='--')
    ax2.set_ylabel('PC')
    ax2.set_xlabel('Year')
    ax2.set_title(f'PC{n+1}', loc='left')
    return ax
def elev_spatial(ax):
    path = '/home/mhuang/data/trendy/v11'
    fname = 'GMTED2010_15n240_1000deg.nc'
    elev = xr.open_dataset(os.path.join(path, fname))
    contour = ax.contour(elev.longitude, elev.latitude, elev.elevation
                         , levels=10, colors='black', linewidths=0.5)
    """for i, segs in enumerate(contour.allsegs):
        for segment in segs:
            if len(segment) > 0:  # 检查 segment 是否为空
                # 获取每条等高线的中点位置
                x = segment[len(segment) // 2][0]
                y = segment[len(segment) // 2][1]
                if xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1]:
                    ax.text(x, y, f'{contour.levels[i]:.2f}', color='black', fontsize=5, ha='center')"""
class DefineCmaps:
    def white_to_blue(self):
        colors = plt.cm.Blues(np.linspace(0, 1, 256))
        colors[0] = np.array([1, 1, 1, 1])
        custom_cmap = ListedColormap(colors)
        return custom_cmap
    def white_to_red(self):
        colors = plt.cm.YlOrRd(np.linspace(0, 1, 256))
        colors[0] = np.array([1, 1, 1, 1])
        custom_cmap = ListedColormap(colors)
        return custom_cmap
    def landcover(self):
        colors = [
            '#ADD8E6',  # water (lightblue)
            '#FFFF00',  # grasses/cereal (yellow)
            '#FFD700',  # shrubs (gold)
            '#FF6347',  # broadleaf crops (red)
            '#FFA500',  # savannah (orange)
            '#006400',  # evergreen broadleaf forest (darkgreen)
            '#8B4513',  # deciduous broadleaf forest (brown)
            '#228B22',  # evergreen needleleaf forest (forestgreen)
            '#32CD32',  # deciduous needleleaf forest (lightgreen)
            '#A9A9A9',  # unvegetated (grey)
            '#8B0000'  # urban (darkred)
        ]
        txt    = [
            'water',
            'grasses/cereal',
            'shrubs',
            'broadleaf crops',
            'savannah',
            'evergreen broadleaf forest',
            'deciduous broadleaf forest',
            'evergreen needleleaf forest',
            'deciduous needleleaf forest',
            'unvegetated',
            'urban'
        ]
        cmap = mcolors.ListedColormap(colors)
        bounds = np.arange(-0.5, 11.5, 1)
        norm = mcolors.BoundaryNorm(bounds, cmap.N)
        return cmap, norm, colors, txt
class mn_season:
    def __init__(self):
        pass
    def ini_fig(self):
        fig = plt.figure(figsize=(11, 3.5))
        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        fig.subplots_adjust(wspace=0)
        mon = plt.subplot(gs[0])
        sea = plt.subplot(gs[1])
        return mon, sea
    def same_ylim(self,ax1,ax2):
        ylim = ax1.get_ylim()
        ax2.set_ylim(ylim)
    def optimiz_fig(self, mon, sea):
        sea.set_yticks([])
        sea.set_ylabel('')
        mon.legend(ncol=4)
        plt.gcf().subplots_adjust(bottom=0.15, top=0.95)
    def ytick_color(self, ax, direction, color):
        ax.tick_params(axis='y', colors=color)
        ax.spines[direction].set_color(color)
        ylabel = ax.get_ylabel()
        ax.set_ylabel(ylabel, color=color)
class ScatterPlots:
    def __init__(self):
        self.fig = plt.figure(figsize=(5, 4))
        self.ax  = self.fig.add_subplot(111)
    def mat_map(self):
        self.ax.set_ylabel('MAT (\u00B0C)')
        self.ax.set_xlabel('MAP (mm/yr)')
        return self
class RegionBox():
    def __init__(self,region):
        self.region = region
    def rectangle(self, ax):
        rect = plt.Rectangle(
            (name_dic.transcom[self.region]['lon_min'], name_dic.transcom[self.region]['lat_min'])
            , name_dic.transcom[self.region]['lon_max'] - name_dic.transcom[self.region]['lon_min']
            , name_dic.transcom[self.region]['lat_max'] - name_dic.transcom[self.region]['lat_min']
            , edgecolor='k', linewidth=2, facecolor='none')
        ax.add_patch(rect)
        return ax
    def obspack(self, ax, station):
        obspack = pd.read_csv(station)
        obspack['Type'] = obspack['Type'].replace({
            'aircraft-flask': 'aircraft',
            'aircraft-insitu': 'aircraft',
            'aircraft-pfp': 'aircraft',
            'shipboard-flask': 'ship',
            'shipboard-insitu': 'ship',
            'surface-flask': 'surface',
            'surface-insitu': 'surface',
            'surface-pfp': 'surface',
            'tower-insitu': 'surface'
        })
        type = {
            'aircore': {'color': 'k', 'marker': 'o'},
            'aircraft': {'color': 'k', 'marker': '>'},
            'ship': {'color': 'purple', 'marker': 'o'},
            'surface': {'color': 'purple', 'marker': 'x'}
        }
        for key, value in obspack.groupby('Type'):
            value.plot.scatter(x='Longitude', y='Latitude', s=50, label=key, **type[key], ax=ax)
            ax.legend(loc='lower left')

