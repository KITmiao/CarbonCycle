import os
import data_processor
import input
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import xskillscore as xs
from matplotlib.projections import PolarAxes
from mpl_toolkits.axisartist import floating_axes
from mpl_toolkits.axisartist import grid_finder
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
import xarray as xr
from pyEOF import *
from eofs.standard import Eof
from sklearn.preprocessing import StandardScaler
from plots.plots_design import visual_EOF
def stand_1Dzscore(data):
    data_stand = (data-data.mean(axis=0, skipna=True))/data.std(axis=0, skipna=True)
    return data_stand
def stand_1Dmaxmin(data):
    data_stand = (data-data.mean(axis=0, skipna=True))/(data.max(axis=0, skipna=True) - data.min(axis=0, skipna=True))
    return data_stand
def stand_3Dzscore(data):
    data_stand = (data-data.mean(skipna=True))/data.std(skipna=True)
    data_stand['time'] = np.array(data_stand['time'], dtype='datetime64')
    return data_stand
def stand_3Dmaxmin(data):
    data_stand = (data-data.mean(skipna=True))/(data.max(skipna=True)-data.min(skipna=True))
    #print(data_stand['time'])
    data_stand['time'] = np.array(data_stand['time'], dtype='datetime64')
    return data_stand
def rmse(mod, obs):
    squ_bias = (mod-obs)**2
    sum_squ_bias = (squ_bias).sum(skipna=True)/len(squ_bias)
    RMSE = np.sqrt(sum_squ_bias)
    return RMSE
def set_tayloraxes(fig, location):
    sd_max=2
    trans = PolarAxes.PolarTransform()
    r1_locs = np.hstack((np.arange(1,10)/10.0,[0.95,0.99]))
    t1_locs = np.arccos(r1_locs)
    gl1 = grid_finder.FixedLocator(t1_locs)
    tf1 = grid_finder.DictFormatter(dict(zip(t1_locs, map(str,r1_locs))))
    r2_locs = np.arange(0,sd_max+0.25,0.25)
    r2_labels = ['0 ', '0.25 ', '0.50 ', '0.75 ', 'REF ', '1.25 ', '1.50 ', '1.75 ', '2 ']
    gl2 = grid_finder.FixedLocator(r2_locs)
    tf2 = grid_finder.DictFormatter(dict(zip(r2_locs, map(str,r2_labels))))
    ghelper = floating_axes.GridHelperCurveLinear(trans,extremes=(0,np.pi/2,0,sd_max),
                                                  grid_locator1=gl1,tick_formatter1=tf1,
                                                  grid_locator2=gl2,tick_formatter2=tf2)
    ax = floating_axes.FloatingSubplot(fig, location, grid_helper=ghelper)
    fig.add_subplot(ax)

    ax.axis["top"].set_axis_direction("bottom")
    ax.axis["top"].toggle(ticklabels=True, label=True)
    ax.axis["top"].major_ticklabels.set_axis_direction("top")
    ax.axis["top"].label.set_axis_direction("top")
    ax.axis["top"].label.set_text("Correlation")
    ax.axis["top"].label.set_fontsize(14)
    ax.axis["left"].set_axis_direction("bottom")
    ax.axis["left"].label.set_text("Standard deviation ratio")
    ax.axis["left"].label.set_fontsize(14)
    ax.axis["right"].set_axis_direction("top")
    ax.axis["right"].toggle(ticklabels=True)
    ax.axis["right"].major_ticklabels.set_axis_direction("left")
    ax.axis["bottom"].set_visible(False)
    ax.grid(True)
    polar_ax = ax.get_aux_axes(trans)

    rs,ts = np.meshgrid(np.linspace(0,sd_max,100),
                            np.linspace(0,np.pi/2,100))
    rms = np.sqrt(1 + rs**2 - 2*rs*np.cos(ts))
    CS = polar_ax.contour(ts, rs,rms,colors='gray',linestyles='--')
    plt.clabel(CS, inline=1, fontsize=10)
    t = np.linspace(0,np.pi/2)
    r = np.zeros_like(t) + 1
    polar_ax.plot(t,r,'k--')
    polar_ax.text(np.pi/2+0.032,1.02, " 1.00", size=10.3,ha="right", va="top",
                  bbox=dict(boxstyle="square",ec='w',fc='w'))

    return polar_ax
def set_hovmolleraxes(fig, location, ylabel, xlabel, title):
    ax = fig.add_subplot(location)
    fig.add_subplot(ax)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    if title:
        ax.set_title(title, fontsize=14)
    return ax
def plot_taylor(axes, refsample, sample, *args, **kwargs):
    std = np.std(refsample)/np.std(sample)
    corr = np.corrcoef(refsample, sample)
    theta = np.arccos(abs(corr[0,1]))
    t,r = theta,std
    print(t,r)
    d = axes.plot(t,r, *args, **kwargs)
    return d
class TaylorOnePlot:
    def __init__(self, obs, mod_values, mod_names, title, subtitle):
        self.obs        = obs
        self.mod_values = mod_values
        self.mod_names  = mod_names
        self.title      = title
        self.subtitle     = subtitle
    def plot(self):
        fig = plt.figure(figsize=(8, 8))
        ax1 = set_tayloraxes(fig, 111)
        i = 0
        style = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'b+', 'g+', 'r+', 'c+', 'm+', 'y+', 'bv', 'gv', 'rv', 'cv', 'mv',
                 'yv']

        for member in self.mod_names:
            print(member)
            plot_taylor(ax1, self.obs, self.mod_values[member],
                        style[i], markersize=12, label=member)
            i = i + 1

        plot_taylor(ax1, self.obs, self.obs, 'ko',
                    markersize=12, label='obs')
        ax1.legend(loc='upper right')
        ax1.set_title(self.title)
        fig.text(0.05, 0.95, self.subtitle, fontsize=16)
def set_fluxtowerplot(fig):
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    ax3 = ax1.twinx()

    ax3.spines['right'].set_position(('outward', 60))

    ax3.spines['right'].set_visible(True)

    ax1.set_xlabel('time')
    ax1.set_ylabel('CO$_2$ flux ($\mu$mol m$_{-2}$ s$^{-1}$)', color='g')
    ax2.set_ylabel('precipitation (mm)', color='b')
    ax3.set_ylabel('soil water contain', color='peru')
    return ax1, ax2, ax3
def pearson_map(ax1, data1, data2):
    r = xs.pearson_r(data1, data2, dim='time', skipna=True)
    p = xs.pearson_r_p_value(data1, data2, dim='time', skipna=True)
    p_mask = p >= 0.05
    p_x, p_y = np.meshgrid(p.lon.values, p.lat.values)
    p_x = p_x[p_mask]
    p_y = p_y[p_mask]
    ax1.coastlines()
    map = ax1.pcolormesh(r.lon, r.lat, r, vmin=-1, vmax=1, transform=ccrs.PlateCarree(),cmap='bwr')
    ax1.scatter(p_x, p_y, c='k', marker='x', alpha=0.55, s=25, linewidth=0.5, label='p>0.05')
    plt.legend(loc='lower right')
    return map, ax1
def change_order(data, new_order):
    new_data = data.reindex(new_order).reset_index()
    return new_data
def colum_filter(df, keyword):
    filtered_columns = [col for col in df.columns if keyword not in col]
    filtered_df = df[filtered_columns]
    return filtered_df
def same_ylim(ax1,ax2):
    ylim = ax1.get_ylim()
    ax2.set_ylim(ylim)
def get_mean(value, period):
    start = period['start']
    end = period['end']
    field = value.sel(time=slice(start, end)).mean(dim=['time'], skipna=True)
    return field
def get_season_mean(value, period, season):
    start = period['start']
    end   = period['end']
    value = value.sel(time=slice(start, end))
    value = value.groupby('time.month').mean(dim='time', skipna=True)
    value = value.sel(month=season).mean(dim='month', skipna=True)
    return value
def get_anno(value, period, period_clim, season):
    clim  = get_season_mean(value, period_clim, season)
    targ  = get_season_mean(value, period, season)
    anno  = targ - clim
    return anno
def dfn_season(start_month, lasts):
    season_months = []
    for i in range(lasts):
        current_month = (start_month + i - 1) % 12 + 1
        season_months.append(current_month)
    return season_months
def asc_to_nc(asc_file, nc_file):
    with open(asc_file, 'r') as f:
        header = {}
        for _ in range(6):
            line = f.readline().strip()
            key, value = line.split()
            header[key] = float(value)

        ncols = int(header['ncols'])
        nrows = int(header['nrows'])
        xllcorner = header['xllcorner']
        yllcorner = header['yllcorner']
        cellsize = header['cellsize']
        nodata_value = header['NODATA_value']

        data = np.loadtxt(f)
        data[data == nodata_value] = np.nan

        x = np.arange(xllcorner, xllcorner + ncols * cellsize, cellsize)
        y = np.arange(yllcorner, yllcorner + nrows * cellsize, cellsize)

        da = xr.DataArray(data, coords=[y, x], dims=['y', 'x'])
        ds = xr.Dataset({'data': da})
        ds.to_netcdf(nc_file)
        print(f"转换完成：{nc_file}")
def tif_to_nc(tif, nc):
    from osgeo import gdal
    gdal.Translate(nc, tif, format='netCDF')
    print(nc)
def simple_moving_average(data, window_size):
    # data np.array
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')
def running_mean(data, window_size):
    # data xarray
    rolling_avg = data.rolling(time=window_size, center=True).mean()
    sst_smoothed = rolling_avg.fillna(data.mean(dim="time"))
    return sst_smoothed
def custom_yrsum(data, mn1, mn2):
    data.index = pd.to_datetime(data.index)
    result = []
    for year in range(data.index.year.min(), data.index.year.max()):
        start = f'{year}-{mn1}-01'
        end = f'{year + 1}-{mn2}-01'
        yearly_sum = data[start:end].sum()
        result.append((start, yearly_sum))
    start = f'{year + 1}-{mn1}-01'
    yearly_sum = 0
    result.append((start, yearly_sum))
    result_df = pd.DataFrame(result, columns=['Time', 'Sum'])
    return result_df
def custom_yrsum2(data, mn1, mn2):
    data.index = pd.to_datetime(data.index)
    result = []
    for year in range(data.index.year.min(), data.index.year.max()):
        start = f'{year}-{mn1}-01'
        end = f'{year}-{mn2}-01'
        yearly_sum = data[start:end].sum()
        result.append((start, yearly_sum))
    start = f'{year + 1}-{mn1}-01'
    end = f'{year + 1}-{mn2}-01'
    yearly_sum = data[start:end].sum()
    result.append((start, yearly_sum))
    start = f'{year + 2}-{mn1}-01'
    yearly_sum = 0
    result.append((start, yearly_sum))
    result_df = pd.DataFrame(result, columns=['Time', 'Sum'])
    return result_df
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
def eof_reconstruction(pc, eof, n):
    eof = eof[n,:,:]
    pc  = pc.iloc[:,n]
    #reconstructed = (pc.values[:, :, np.newaxis, np.newaxis] * eof.values[np.newaxis, :, :, :]).sum(axis=1)
    reconstructed = pc.values[:, np.newaxis, np.newaxis] * eof.values[np.newaxis, :, :]
    reconstructed = xr.DataArray(
        data=reconstructed,
        coords={
            'time': pc.index,
            'lat': eof.lat,
            'lon': eof.lon,
        },
        dims=['time', 'lat', 'lon'],
        name="reconstructed_sst"
    )
    return reconstructed
def pairwise_rotation(eof1, eof2, pc1, pc2, theta):
    """
    eof1, eof2 : xr.DataArray
    pc1, pc2 : pd.Series or np.array
    theta : float

    rotated_eof1, rotated_eof2 : xr.DataArray
    rotated_pc1, rotated_pc2 : np.array
    """
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                [np.sin(theta), np.cos(theta)]])

    eof_stack = np.stack([eof1, eof2], axis=0)
    rotated_eofs = np.tensordot(rotation_matrix, eof_stack, axes=1)

    pcs_stack = np.stack([pc1, pc2], axis=0)
    rotated_pcs = np.dot(rotation_matrix, pcs_stack)

    return rotated_eofs[0], rotated_eofs[1], rotated_pcs[0], rotated_pcs[1]
def zscore(x):
    mean = x.mean(dim=["lat", "lon"])
    std = x.std(dim=["lat", "lon"])
    res = (x - mean) / std
    return res