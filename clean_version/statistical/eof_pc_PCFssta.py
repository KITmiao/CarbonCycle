import name_dic
import os
import numpy as np
import xarray as xr
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
from matplotlib.colors import ListedColormap
from statistical_analysis import change_order
from statistical_analysis import dfn_season
from statistical_analysis import get_season_mean
from settings import define_season
from settings import order
from monthly_plots import MonthlyPlot
from season_plots import SeasonPlot
from visual_lines import VisualLines
import matplotlib.pyplot as plt
from statistical_analysis import get_mean
from latlon_plot import LatlonPlot
from statistical_analysis import pearson_map
from statistical_analysis import get_anno
import pandas as pd
from plots.plots_design import ScatterPlots as sp
from pyEOF import *
from eofs.standard import Eof
from sklearn.preprocessing import StandardScaler
from plots.plots_design import visual_EOF
import pickle
from statistical_analysis import running_mean
def eof_method(ssta, n):
    lat  = ssta.lat
    lon  = ssta.lon
    lat  = np.array(lat)
    coslat = np.cos(np.deg2rad(lat))
    wgts   = np.sqrt(coslat)[..., np.newaxis]
    ssta = ssta * wgts
    ssta = ssta.to_dataframe().reset_index().drop(columns=["month"])  # get df from da
    ssta = get_time_space(ssta, time_dim="time", lumped_space_dims=["lat", "lon"])
    pca = df_eof(ssta)  # implement EOF
    eofs = pca.eofs(s=2, n=n)  # get eofs
    eofs_da = eofs.stack(["lat", "lon"]).to_xarray()  # make it convenient for visualization
    pcs = pca.pcs(s=2, n=n)  # get pcs
    pcs = pcs / pcs.std(axis=0)
    evfs = pca.evf(n=n)  # get variance fraction
    print(evfs)
    return pcs, eofs_da, evfs
def eof_method_rotated(ssta,n):
    lat = ssta.lat
    lon = ssta.lon
    lat = np.array(lat)
    coslat = np.cos(np.deg2rad(lat))
    wgts = np.sqrt(coslat)[..., np.newaxis]
    ssta = ssta * wgts
    ssta = ssta.to_dataframe().reset_index().drop(columns=["month"])  # get df from da
    ssta = get_time_space(ssta, time_dim="time", lumped_space_dims=["lat", "lon"])
    pca = df_eof(ssta, pca_type="varimax", n_components=n)  # implement EOF
    eofs = pca.eofs(s=2, n=n)  # get eofs
    eofs_da = eofs.stack(["lat", "lon"]).to_xarray()  # make it convenient for visualization
    pcs = pca.pcs(s=2, n=n)  # get pcs
    pcs = pcs / pcs.std(axis=0)
    evfs = pca.evf(n=n)  # get variance fraction
    print(evfs)
    return pcs, eofs_da, evfs
def eof_method2(ssta,n):
    lat = ssta.lat
    lon = ssta.lon
    time= ssta.time
    ssta = np.array(ssta)
    lat = np.array(lat)
    coslat = np.cos(np.deg2rad(lat))
    wgts = np.sqrt(coslat)[..., np.newaxis]
    solver = Eof(ssta, weights=wgts)
    #solver = Eof(ssta)
    eof    = solver.eofsAsCorrelation(neofs=n)
    pc     = solver.pcs(npcs=n, pcscaling=1)
    var    = solver.varianceFraction(neigs=n)
    pc     = pd.DataFrame(index=time, data=pc)
    eof    = xr.DataArray(
        data=eof,
        coords={
            'pc': str(range(n)),
            'lat': lat,
            'lon': lon,
        },
        dims=['pc', 'lat', 'lon'],
        name="sst"
    )
    return pc, eof, var
print(__name__)
from settings import Pacific_range as Pr
from settings import number_of_EOFs as n
from settings import sst_product as name
#from statistical.eof_pc_modereconstruction import reconstruct_EOFs
#from statistical.eof_pc_modereconstruction import filtered_sst as sst

sst = xr.open_dataset(os.path.join('/home/mhuang/data/trendy/v11', 'sst.nc'))

sst = sst.sel(
        time=slice('2009-01-01', '2018-12-31'),
        lat=slice(Pr[1], Pr[0]),
        lon=slice(Pr[2], Pr[3])
    )

meansst = sst.mean(dim=['lat','lon'])
ssta = sst.groupby('time.month') - sst.groupby('time.month').mean(dim='time', skipna=True)
pcs, eofs_da, evfs = eof_method2(ssta[name], n)
with open('/home/mhuang/mycode/pkl/eof_pcf.pkl', 'wb') as f:
    pickle.dump((pcs, eofs_da, evfs), f)
eofs_da[1, :, :] = -eofs_da[1, :, :]
pcs.iloc[:, 1] = -pcs.iloc[:, 1]
if __name__ == '__main__':
    for i in range(n):
        product = name + 'SST'
        ax=visual_EOF(pcs,eofs_da,evfs,i, product)
        ax.set_aspect(1)
        plt.show()