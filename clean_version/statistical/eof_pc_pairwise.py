import pickle
import numpy as np
import matplotlib.pyplot as plt
from plots.plots_design import visual_EOF
from statistical_analysis import pairwise_rotation as pwr

"""
with open('/home/mhuang/mycode/pkl/eof_glb.pkl', 'rb') as f:
    pcs, eofs_da = pickle.load(f)"""
i = 0
j = 2
with open('/home/mhuang/mycode/pkl/eof_pcf.pkl', 'rb') as f:
    pcs, eofs_da, evfs = pickle.load(f)
evfs = [0,0,0,0]
eofs_da[i,:,:], eofs_da[j,:,:], pcs.iloc[:,i], pcs.iloc[:,j] = pwr(
        eofs_da[i, :, :], eofs_da[j, :, :], pcs.iloc[:, i], pcs.iloc[:, j], 20 * np.pi / 180
    )

ax=visual_EOF(-pcs,-eofs_da,evfs,i, 'HadISST')
ax.set_aspect(1)
plt.show()
ax=visual_EOF(pcs,eofs_da,evfs,j, 'HadISST')
ax.set_aspect(1)
plt.show()