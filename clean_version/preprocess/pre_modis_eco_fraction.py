import numpy as np
import netCDF4 as nc

def calculate_area_fraction(input_file, output_file):
    ds = nc.Dataset(input_file)
    eco_type = ds.variables['eco_type'][:]
    lat = ds.variables['lat'][:]
    lon = ds.variables['lon'][:]
    ds.close()

    new_res = 0.5
    lat_new = np.arange(-89.75, 90.25, 0.5)
    lon_new = np.arange(-179.75, 180.25, 0.5)

    area_fraction = np.zeros((len(lat_new), len(lon_new), 11))

    for i, lat_val in enumerate(lat_new):
        print(i)
        for j, lon_val in enumerate(lon_new):
            lat_mask = (lat >= lat_val) & (lat < lat_val + new_res)
            lon_mask = (lon >= lon_val) & (lon < lon_val + new_res)
            combined_mask = lat_mask[:, None] & lon_mask[None, :]

            if np.any(combined_mask):
                subgrid = eco_type[combined_mask]
                total_count = subgrid.size
                for eco in range(11):
                    eco_count = np.sum(subgrid == eco)
                    area_fraction[i, j, eco] = eco_count / total_count

    ds_out = nc.Dataset(output_file, 'w', format='NETCDF4')
    ds_out.createDimension('lat', len(lat_new))
    ds_out.createDimension('lon', len(lon_new))
    ds_out.createDimension('eco_type', 11)

    lat_out = ds_out.createVariable('lat', 'f4', ('lat',))
    lon_out = ds_out.createVariable('lon', 'f4', ('lon',))
    area_fraction_out = ds_out.createVariable('area_fraction', 'f4', ('lat', 'lon', 'eco_type'))

    lat_out[:] = lat_new
    lon_out[:] = lon_new
    area_fraction_out[:, :, :] = area_fraction

    ds_out.close()

input_file = '/home/mhuang/data/otherdata/modis_ecotype.nc'
output_file = '/home/mhuang/data/otherdata/modis_ecotype_fraction.nc'
calculate_area_fraction(input_file, output_file)