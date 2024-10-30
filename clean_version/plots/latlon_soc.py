import name_dic
import numpy as np
from data_processor import (
    process_trendy_nbp,
    process_trendy_ra,
    process_trendy_rh,
    process_trendy_gpp,
    process_trendy_fLuc,
    process_trendy_fFire,
    process_trendy_lai,
    ProcessTM5GOSAT,
    ProcessTRENDY,
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
    ProcessNIRvGPP,
    ProcessAll
)
import read_pkl
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from read_pkl import data
import cartopy.crs as ccrs
import xarray as xr
print(__name__)
if __name__.split('.')[-1] == 'latlon_soc':
    soc = xr.open_dataset('/home/mhuang/data/trendy/v11/GSOCmap1.5.0.nc')
    fig = plt.figure(figsize=[6, 3])
    ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    map = ax1.pcolormesh(soc.lon, soc.lat, soc.Band1, cmap='Greens')
    cbar1 = fig.colorbar(map, ax=ax1, extend='both', orientation='horizontal')
    cbar1.set_label('GPP (gC/m2/day)')
    cbar1.ax.set_position([0.26, 0.2, 0.5, 0.04])
    ax1.set_xlim(data.fire['fire'].region['lon_min'] - 3, data.fire['fire'].region['lon_max'] + 3)
    ax1.set_ylim(data.fire['fire'].region['lat_min'] - 3, data.fire['fire'].region['lat_max'] + 3)
    ax1.set_title('SOC map')
    gl = ax1.gridlines(draw_labels=True, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
if __name__ == '__main__':
    pass
