import xarray as xr
import numpy as np
import os

path = '/home/mhuang/data/trendy/v11'
class CreateSIFEnsemble:
    def __init__(self):
        self.gosif = xr.open_dataset(os.path.join(path, 'GOSIF1x1.nc'))
        self.gome  = xr.open_dataset(os.path.join(path, 'GOME_sif.nc'))
        self.ensemble   = [
            self.gosif.GOSIF,
            self.gome.GOME,
            self.gome.transcom_regions,
            self.gome.land_ecosystems,
            self.gome.country_id,
            self.gome.eco_type
        ]
    def exicute(self):
        ensemble  = xr.merge(self.ensemble)
        ensemble.to_netcdf(os.path.join(path, 'SIF_ensemble1x1.nc'))
class CreateSIFGPPEnsemble:
    def __init__(self):
        self.gosif = xr.open_dataset(os.path.join(path, 'GOSIF_GPP1x1.nc'))
        self.gome  = xr.open_dataset(os.path.join(path, 'sif_based_gpp_eraT_1x1.nc'))
        self.postor= xr.open_dataset(os.path.join(path, 'HeteroResp2_1x1.nc'))
        self.ensemble   = [
            self.gosif.GOSIF,
            self.gome.GOME,
            self.gome.transcom_regions,
            self.gome.land_ecosystems,
            self.gome.country_id,
            self.gome.eco_type,
            self.postor.CUE
        ]
    def exicute(self):
        ensemble  = xr.merge(self.ensemble)
        ensemble.to_netcdf(os.path.join(path, 'SIFGPP_ensemble1x1.nc'))

if __name__ == '__main__':
    CreateSIFEnsemble().exicute()
    CreateSIFGPPEnsemble().exicute()