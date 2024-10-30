import os
import xarray as xr
import numpy as np
import xesmf
import pandas as pd
import input_pre
import pre_trendy
import matplotlib.pyplot as plt

class FirePreprocess:
    def __init__(self, setting):
        self.start   = setting['START_DATE']
        self.end     = setting['END_DATE']
        self.out_fn  = os.path.join(setting['OUT_PATH'], 'Global_Fire.nc')
        self.finn_fn = os.path.join(setting['PATH'], 'FINN.nc')
        self.gfed_fn = os.path.join(setting['PATH'], 'GFED.nc')
        self.gfas_fn = os.path.join(setting['PATH'], 'GFAS.nc')

        self.finn = xr.open_dataset(self.finn_fn)
        self.gfed = xr.open_dataset(self.gfed_fn)
        self.gfas = xr.open_dataset(self.gfas_fn)
        self.tran = xr.open_dataset(setting['TRANSCOM_FILE'])

        self.finn_regrid = None
        self.gfed_regrid = None
        self.gfas_regrid = None
        self.tran_regrid = None
        self.ecos_regrid = None

    def regrid_data(self):
        ecos = xr.open_dataset('/home/mhuang/data/otherdata/modis_ecotype.nc')
        target_grid = xr.Dataset(
            {
                "lat": (["lat"], np.arange(-90, 90, 1.0)),
                "lon": (["lon"], np.arange(-180, 180, 1.0)),
            }
        )
        regrider = xesmf.Regridder(self.finn, target_grid, method='nearest_s2d', periodic=False)
        self.finn_regrid = regrider(self.finn)
        regrider = xesmf.Regridder(self.gfed, target_grid, method='nearest_s2d', periodic=False)
        self.gfed_regrid = regrider(self.gfed)
        regrider = xesmf.Regridder(self.gfas, target_grid, method='nearest_s2d', periodic=False)
        self.gfas_regrid = regrider(self.gfas)
        regrider = xesmf.Regridder(self.tran, target_grid, method='nearest_s2d', periodic=False)
        self.tran_regrid = regrider(self.tran)
        regrider = xesmf.Regridder(ecos, target_grid, method='nearest_s2d', periodic=False)
        self.ecos_regrid = regrider(ecos)
        return self

    def merge_data(self):
        finn = self.finn_regrid.sel(time=slice(self.start, self.end))
        gfed = self.gfed_regrid.sel(time=slice(self.start, self.end))
        gfas = self.gfas_regrid.sel(time=slice(self.start, self.end))
        gfas['time'] = finn['time']
        gfed['time'] = finn['time']
        ensemble = [
            finn,
            gfed,
            gfas,
            self.tran_regrid.transcom_regions,
            self.tran_regrid.land_ecosystems,
            self.tran_regrid.country_id,
            self.ecos_regrid
        ]
        ensemble = xr.merge(ensemble)
        ensemble.to_netcdf(self.out_fn)
        print(self.out_fn)



if __name__ == "__main__":
    setting = input_pre.fire
    x= FirePreprocess(setting).regrid_data().merge_data()
"""
if __name__ == 'pre_fire':
    setting = input_pre.fire
    x = FirePreprocess(setting).regrid_data().merge_data()
"""