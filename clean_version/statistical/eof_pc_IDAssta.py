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
from plots.plots_design import visual_EOF
def eof_method(ssta, n):
    lat  = ssta.lat
    lon  = ssta.lon
    lat  = np.array(lat)
    coslat = np.cos(np.deg2rad(lat))
    wgts   = np.sqrt(coslat)[..., np.newaxis]
    #ssta = ssta.sst * wgts
    ssta = ssta.to_dataframe().reset_index().drop(columns=["month"])  # get df from da
    ssta = get_time_space(ssta, time_dim="time", lumped_space_dims=["lat", "lon"])
    pca = df_eof(ssta)  # implement EOF
    eofs = pca.eofs(s=2, n=n)  # get eofs
    eofs_da = eofs.stack(["lat", "lon"]).to_xarray()  # make it convenient for visualization
    pcs = pca.pcs(s=2, n=n)  # get pcs
    evfs = pca.evf(n=n)  # get variance fraction
    print(evfs)
    return pcs, eofs_da, evfs
print(__name__)
from settings import IndiaOc_range as Ir
from settings import sst_clim
sst = xr.open_dataset('/home/mhuang/data/nontrendy/sst.mon.mean.nc')
sst = sst.sel(
        time=slice('2009-01-01', '2020-12-31'),
        lat=slice(Ir[0], Ir[1]),
        lon=slice(Ir[2], Ir[3])
    )
"""
clim = xr.open_dataset(sst_clim).sel(
        lat=slice(Pr[0], Pr[1]),
        lon=slice(Pr[2], Pr[3])
    )
clim_aligned = clim.sst.groupby('time.month').mean(dim='time')
clim_expanded = clim_aligned.sel(month=sst['time.month'])
ssta = sst.sst - clim_expanded
"""
n = 3
ssta = sst.groupby('time.month') - sst.groupby('time.month').mean(dim='time', skipna=True)
pcs, eofs_da, evfs = eof_method(ssta, n)
pcs = pcs/pcs.std(axis=0)
if __name__ == '__main__':
    for i in range(n):
        ax = visual_EOF(pcs,eofs_da,evfs,i,'COBE-SSTa')
        ax.set_aspect(0.5)
        plt.show()
