import os
from datetime import datetime
import netCDF4
import numpy as np
from netCDF4 import num2date
import ECMWF_plot
import ECMWF_query


class ECMWF_convert_to_ROMS:

	def __init__(self):
		self.plotter = ECMWF_plot.ECMWF_plot()

	def convert_to_ROMS_standards(self, out_filename: str, metadata, parameter: str, config_ecmwf: ECMWF_query):
		dset = netCDF4.Dataset(out_filename, 'r+')

		da = dset.variables[metadata['short_name']][:]
		masked_array = np.ma.masked_where(da == dset.variables[metadata['short_name']].missing_value, da)

		if parameter in ['mean_surface_net_short_wave_radiation_flux',
						 'mean_surface_net_long_wave_radiation_flux',
						 'mean_surface_downward_long_wave_radiation_flux',
						 'mean_surface_latent_heat_flux',
						 'mean_surface_sensible_heat_flux',
						 'mean_surface_downward_short_wave_radiation_flux']:
			# masked_array = np.ma.divide(masked_array, (3600. * 3.0))
			units = 'W m**-2'

		if parameter in ['specific_humidity']:
			units = 'kg kg-1'

		if parameter in ['10m_u_component_of_wind', '10m_v_component_of_wind']:
			units = 'm s-1'

		if parameter in ['2m_temperature', '2m_dewpoint_temperature']:
			masked_array = np.ma.subtract(masked_array, 273.15)
			units = 'Celsius'

		if parameter in ['evaporation']:
			Rho_w = 1000  # kg m - 3
			masked_array = np.ma.multiply(masked_array, (Rho_w / (3 * 3600.)))
			units = 'kg m-2 s-1'

		if parameter in ['mean_sea_level_pressure']:
			#	masked_array = np.ma.divide(masked_array, 100)
			units = 'Pa'

		if parameter in ['total_cloud_cover']:
			dset.renameVariable(metadata['short_name'], 'cloud')
			units = 'nondimensional'

		if parameter in ['total_precipitation']:
			Rho_w = 1000  # kg m - 3
			masked_array = np.ma.multiply(masked_array, (Rho_w / (3 * 3600.)))
			units = 'kg m-2 s-1'

		# longitude = dset.variables['longitude'][:]
		# latitude = dset.variables['latitude'][:]

		# do_plot = False
		# if do_plot:
		#		self.plotter.plot_data(longitude, latitude, masked_array, time, parameter)

		self.write_to_ROMS_netcdf_file(config_ecmwf,
									   masked_array,
									   units,
									   out_filename,
									   parameter,
									   dset)
		dset.close()

	# We change the reference date to be equal to the standard ROMS
	# reference time 1948-01-01 so that we can use ocean_time as time name
	def change_reference_date(self, ds, config_ecmwf: ECMWF_query):

		era5_time = ds.variables['time'][:]
		era5_time_units = ds.variables['time'].units
		era5_time_cal = ds.variables['time'].calendar

		dates = num2date(era5_time, units=era5_time_units, calendar=era5_time_cal)
		# Convert back to julian day and convert toi seconds since 1948-01-01 as that is standard for ROMS
		days_to_seconds = 86400.0
		times = netCDF4.date2num(dates, units=config_ecmwf.time_units) *  days_to_seconds
		return times, config_ecmwf.time_units

	def write_to_ROMS_netcdf_file(self, config_ecmwf: ECMWF_query, data_array, \
								  var_units: str, netcdf_file, \
								  parameter: str, ds):
		"""
		:param config_ecmwf: The config object containing the metadata
		:param data_array:  the data array downloaded from ECMWF and converted to correct ROMS units
		:param units: the units to write to file
		:param netcdf_file: name of file
		:param parameter: the parameter to write to file - name converted to ROMS name using metadata
		:param longitude: longitude dimension of data
		:param latitude: latitude dimension of data
		:param time: time dimension  of data

		https://www.myroms.org/index.php?page=forcing
		"""
		metadata = config_ecmwf.get_parameter_metadata(parameter)

		longitude = ds.variables['longitude'][:]
		latitude = ds.variables['latitude'][:]
		time, time_units = self.change_reference_date(ds, config_ecmwf)

		netcdf_roms_filename = netcdf_file[0:-3] + '_roms.nc'
		if os.path.exists(netcdf_roms_filename): os.remove(netcdf_roms_filename)
		print("Writing final product to file {}".format(netcdf_roms_filename))

		f1 = netCDF4.Dataset(netcdf_roms_filename, 'w')
		f1.title = "{} ECMWF model forcing for parameter {}".format(config_ecmwf.dataset.upper(), parameter)
		f1.description = "Created by Trond Kristiansen (at) niva.no." \
						 "Atmospheric data on original grid but converted to ROMS units and parameter names." \
						 "Files created using the ECMWF_tools toolbox:" \
						 "https://github.com/trondkr/ERA5-ROMS"
		f1.history = "Created {}".format(datetime.now())
		f1.link = "https://github.com/trondkr/"
		f1.Conventions = "CF-1.0"
		fillval = 1.0e35
		data_array[data_array.mask] = fillval

		# Define dimensions
		f1.createDimension('lon', len(longitude))
		f1.createDimension('lat', len(latitude))
		f1.createDimension('ocean_time', None)

		vnc = f1.createVariable('lon', 'd', 'lon', fill_value=fillval)
		vnc.long_name = 'Longitude'
		vnc.units = 'degree_east'
		vnc.standard_name = 'longitude'
		vnc[:] = longitude

		vnc = f1.createVariable('lat', 'd', 'lat', fill_value=fillval)
		vnc.long_name = 'Latitude'
		vnc.units = 'degree_north'
		vnc.standard_name = 'latitude'
		vnc[:] = latitude

		vnc = f1.createVariable('ocean_time', 'd', ('ocean_time',), fill_value=fillval)
		vnc.long_name = time_units
		vnc.units = time_units
		vnc.field = 'time, scalar, series'
		vnc.calendar = 'standard'
		vnc[:] = time

		vnc = f1.createVariable(metadata['roms_name'], 'd', ('ocean_time', 'lat', 'lon'), fill_value=fillval)
		vnc.long_name = metadata["name"]
		vnc.standard_name = metadata["short_name"]
		vnc.coordinates = "lon lat"
		vnc.units = var_units
		vnc.missing_value = fillval
		vnc[:, :, :] = data_array
		print("Finished writing to file {}".format(netcdf_roms_filename))
		os.remove(netcdf_file)
		f1.close()
