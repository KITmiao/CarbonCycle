import name_dic
import pickle
import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from statistical_analysis import eof_method2
from statistical_analysis import running_mean
from statistical_analysis import pairwise_rotation
from plots.plots_design import visual_EOF

print(__name__)
from settings import number_of_EOFs as n
from settings import sst_product as name
sst = xr.open_dataset(os.path.join('/home/mhuang/data/trendy/v11', 'sst.nc'))
sst = sst.sel(
        time=slice('1910-01-01', '2021-12-31'),
        lat=slice(65,-65),
        lon=slice(0.5,359.5)
    )
#sst = running_mean(sst, 13)
meansst = sst.mean(dim=['lat','lon'])
runmeansst = running_mean(sst, 3).mean(dim=['lat','lon'])
ssta = sst[name].groupby('time.month') - sst[name].groupby('time.month').mean(dim='time', skipna=True)
ssta = running_mean(ssta, 3).sel(time=slice('1911-01-01', '2020-12-31'))
pcs, eofs_da, evfs = eof_method2(ssta, n)
with open('/home/mhuang/mycode/pkl/eof_glb.pkl', 'wb') as f:
    pickle.dump((pcs, eofs_da, evfs), f)

fig = plt.figure(figsize=[12, 3])
ax = fig.add_subplot(111)
ax.plot(meansst.time, meansst['HadI'],  alpha=0.4, color='orange')
ax.plot(meansst.time, meansst['COBE'],  alpha=0.4, color='blue')
ax.plot(runmeansst.time, runmeansst['HadI'], label='HadISST', color='orange')
ax.plot(runmeansst.time, runmeansst['COBE'], label='COBESST', color='blue')
ax.legend()
plt.show()
if __name__ == '__main__':
    for i in range(n):
        ax=visual_EOF(pcs,eofs_da,evfs,i, 'HadISST')
        ax.set_aspect(1)
        plt.show()
    """
    eofs_da[2,:,:], eofs_da[3,:,:], pcs.iloc[:,2], pcs.iloc[:,3] = pairwise_rotation(
        eofs_da[2, :, :], eofs_da[3, :, :], pcs.iloc[:, 2], pcs.iloc[:, 3], 47 * np.pi / 180
    )
    for i in range(n):
        ax=visual_EOF(pcs,eofs_da,evfs,i, 'HadISST')
        ax.set_aspect(1)
        plt.show()"""