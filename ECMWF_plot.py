import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import netCDF4

class ECMWF_plot:

	def plot_data(self, longitude, latitude, masked_array, time, parameter):
		proj = ccrs.PlateCarree()

		for i in range(3):
			dd = xr.DataArray(masked_array[i, :, :],
							  name=parameter,
							  dims=('latitude', 'longitude'),
							  coords={'latitude': latitude,
									  'longitude': longitude})

			fig, ax1 = plt.subplots(ncols=1, subplot_kw={'projection': proj})

			dd.plot(transform=proj, ax=ax1)
			ax1.coastlines()
			plt.title(netCDF4.num2date(time[i], units='hours since 1900-01-01 00:00:00.0', calendar='standard'))
			plt.show()
