import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import netCDF4

class ECMWF_plot:

	def plot_test_case(self):
		# This plotting is run interactively in pycharm
		df = xr.open_dataset("results/era5_msdwswrf_year_1980_roms.nc")
		swrad = df["swrad"]
		swrad.mean({"lat", "lon"}).plot(c="blue",alpha=0.5)
		swrad.mean({"lat", "lon"}).resample(swrad_time="7D").mean().plot(c="orange", linewidth=3)
		swrad.mean({"lat", "lon"}).resample(swrad_time="1M").mean().plot(c="red", linewidth=3)

		df = xr.open_dataset("results/era5_t2m_year_1980_roms.nc")
		swrad = df["Tair"]
		swrad.mean({"lat", "lon"}).plot(c="blue", alpha=0.5)
		swrad.mean({"lat", "lon"}).resample(Tair_time="7D").mean().plot(c="orange", linewidth=3)
		swrad.mean({"lat", "lon"}).resample(Tair_time="1M").mean().plot(c="red", linewidth=3)

		df = xr.open_dataset("results/era5_q_year_1980_roms.nc")
		swrad = df["Qair"]
		swrad.mean({"lat", "lon"}).plot(c="blue", alpha=0.5)
		swrad.mean({"lat", "lon"}).resample(qair_time="7D").mean().plot(c="orange", linewidth=3)
		swrad.mean({"lat", "lon"}).resample(qair_time="1M").mean().plot(c="red", linewidth=3)

		df = xr.open_dataset("results/era5_msl_year_1980_roms.nc")
		swrad = df["Pair"]
		swrad.mean({"lat", "lon"}).plot(c="blue", alpha=0.5)
		swrad.mean({"lat", "lon"}).resample(pair_time="7D").mean().plot(c="orange", linewidth=3)
		swrad.mean({"lat", "lon"}).resample(pair_time="1M").mean().plot(c="red", linewidth=3)

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
