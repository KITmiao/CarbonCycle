import cartopy.crs as ccrs
from matplotlib import pyplot as plt
from statistical.eof_pc_GLBssta import ssta
from statistical.eof_pc_GLBssta import pcs
from statistical.eof_pc_GLBssta import eofs_da as eofs
from statistical_analysis import eof_reconstruction as reconstruct
from settings import reconstruct_EOFs as n

print(__name__)
fig = plt.figure(figsize=[12, 3])
ax = fig.add_subplot(111)
for i in n:
    print(i)
    reconstruct_EOFs = reconstruct(pcs,eofs,i)
    ax.plot(reconstruct_EOFs.time, reconstruct_EOFs.mean(dim=['lat','lon']), label=f'reconstruction{i}')
ax.plot(ssta.time, ssta.mean(dim=['lat','lon']), label='HadISSTa')
ax.legend()
plt.show()
filtered_sst     = ssta - reconstruct_EOFs
