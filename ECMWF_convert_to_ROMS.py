import os
from datetime import datetime
import netCDF4
import numpy as np
from netCDF4 import num2date
import ECMWF_plot
import ECMWF_query
import logging


class ECMWF_convert_to_ROMS:

	def __init__(self):
		self.plotter = ECMWF_plot.ECMWF_plot()

	def convert_to_ROMS_units_standards(self, out_filename: str, metadata, parameter: str, config_ecmwf: ECMWF_query):
		dset = netCDF4.Dataset(out_filename, 'r+')

		da = dset.variables[metadata['short_name']][:]
		masked_array = np.ma.masked_where(da == dset.variables[metadata['short_name']].missing_value, da)
		logging.debug("[ECMWF_convert_to_ROMS] Will convert for parameter: {}".format(parameter))
		if parameter in ['mean_surface_net_short_wave_radiation_flux',
						 'mean_surface_net_long_wave_radiation_flux',
						 'mean_surface_downward_long_wave_radiation_flux',
						 'mean_surface_latent_heat_flux',
						 'mean_surface_sensible_heat_flux',
						 'mean_surface_downward_short_wave_radiation_flux']:
			# masked_array = np.ma.divide(masked_array, (3600. * 3.0))
			units = 'W m**-2'
			logging.debug("[ECMWF_convert_to_ROMS] Converted parameter: {}".format(parameter))
		elif parameter in ['specific_humidity']:
			units = 'kg kg-1'
			logging.debug("[ECMWF_convert_to_ROMS] Converted parameter: {}".format(parameter))
		elif parameter in ['10m_u_component_of_wind', '10m_v_component_of_wind']:
			units = 'm s-1'
			logging.debug("[ECMWF_convert_to_ROMS] Converted parameter: {}".format(parameter))
		elif parameter in ['2m_temperature', '2m_dewpoint_temperature']:
			masked_array = np.ma.subtract(masked_array, 273.15)
			units = 'Celsius'
			logging.debug("[ECMWF_convert_to_ROMS] Converted parameter: {}".format(parameter))
		elif parameter in ['evaporation']:
			Rho_w = 1000.  # kg m - 3
			masked_array = np.ma.multiply(masked_array, (Rho_w / (1 * 3600.)))
			units = 'kg m-2 s-1'
			logging.debug("[ECMWF_convert_to_ROMS] Converted parameter: {}".format(parameter))
		elif parameter in ['mean_sea_level_pressure']:
			masked_array = np.ma.divide(masked_array, 100) #(1 mb = 100 Pa)
			units = 'mb'
			logging.debug("[ECMWF_convert_to_ROMS] Converted parameter: {}".format(parameter))
		elif parameter in ['total_cloud_cover']:
			dset.renameVariable(metadata['short_name'], 'cloud')
			units = 'nondimensional'
			logging.debug("[ECMWF_convert_to_ROMS] Converted parameter: {}".format(parameter))
		elif parameter in ['total_precipitation']:
			# Convert meter (m) to rate (kgm-2s-1)
			Rho_w = 1000  # kg m - 3
			masked_array = np.ma.multiply(masked_array, (Rho_w / (1 * 3600.)))
			units = 'kg m-2 s-1'
			logging.debug("[ECMWF_convert_to_ROMS] Converted parameter: {}".format(parameter))
		else:
			raise Exception("[ECMWF_convert_to_ROMS] Unable to find parameter {} to convert to ROMS format".format(parameter))
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
	# reference time 1948-01-01 so that we can optionally use ocean_time as time name
	def change_reference_date(self, ds, config_ecmwf: ECMWF_query):

		era5_time = ds.variables['time'][:]
		era5_time_units = ds.variables['time'].units
		era5_time_cal = ds.variables['time'].calendar
		logging.debug("[ECMWF_convert_to_ROMS] Original time: {} to {} cal: {} units: {}".format(era5_time[0],era5_time[-1], era5_time_cal, era5_time_units))

		dates = num2date(era5_time, units=era5_time_units, calendar=era5_time_cal)
		logging.debug(
			"[ECMWF_convert_to_ROMS] Converted time: {} to {}".format(dates[0], dates[-1]))

		# Convert back to julian day and convert to days since 1948-01-01 as that is standard for ROMS
		# days_to_seconds = 86400.0
		times = netCDF4.date2num(dates, units=config_ecmwf.time_units)  # * days_to_seconds
		logging.debug(
			"[ECMWF_convert_to_ROMS] Converted time: {} to {} units: {}".format(times[0], times[-1], config_ecmwf.time_units))

		return times, config_ecmwf.time_units, era5_time_cal

	def write_to_ROMS_netcdf_file(self, config_ecmwf: ECMWF_query, data_array, var_units: str, netcdf_file,
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
		logging.info(
			"[ECMWF_convert_to_ROMS] Writing {} to ROMS netcdf file".format(parameter))

		longitude = ds.variables['longitude'][:]
		latitude = ds.variables['latitude'][:]
		time, time_units, time_calendar = self.change_reference_date(ds, config_ecmwf)

		netcdf_roms_filename = netcdf_file[0:-3] + '_roms.nc'
		if os.path.exists(netcdf_roms_filename): os.remove(netcdf_roms_filename)
		logging.info(
			"[ECMWF_convert_to_ROMS] Writing final product to file {}".format(netcdf_roms_filename))

		f1 = netCDF4.Dataset(netcdf_roms_filename, 'w')
		f1.title = "{} ECMWF model forcing for parameter {}".format(config_ecmwf.dataset.upper(), parameter)
		f1.description = "Created by Trond Kristiansen (at) niva.no." \
						 "Atmospheric data on original grid but converted to ROMS units and parameter names." \
						 "Files created using the ECMWF_tools toolbox:" \
						 "https://github.com/trondkr/ERA5-ROMS"
		f1.history = "Created {}".format(datetime.now())
		f1.link = "https://github.com/trondkr/"
		f1.Conventions = "CF-1.0"
		fill_val = 1.0e35
		data_array[data_array.mask] = fill_val

		# Define dimensions
		f1.createDimension('lon', len(longitude))
		f1.createDimension('lat', len(latitude))
		f1.createDimension(metadata['time_name'], None)

		vnc = f1.createVariable('lon', 'd', 'lon', fill_value=fill_val)
		vnc.long_name = 'Longitude'
		vnc.units = 'degree_east'
		vnc.standard_name = 'longitude'
		vnc[:] = longitude

		vnc = f1.createVariable('lat', 'd', 'lat', fill_value=fill_val)
		vnc.long_name = 'Latitude'
		vnc.units = 'degree_north'
		vnc.standard_name = 'latitude'
		vnc[:] = latitude

		vnc = f1.createVariable(metadata['time_name'], 'd', (metadata['time_name'],), fill_value=fill_val)
		vnc.long_name = 'time'
		vnc.units = time_units
		vnc.field = 'time, scalar, series'
		vnc.calendar = time_calendar
		vnc[:] = time

		vnc = f1.createVariable(metadata['roms_name'], 'd', (metadata['time_name'], 'lat', 'lon'), fill_value=fill_val)
		vnc.long_name = metadata["name"]
		vnc.standard_name = metadata["short_name"]
		vnc.coordinates = "lon lat {}".format(metadata['time_name'])
		vnc.units = var_units
		vnc.missing_value = fill_val
		vnc[:, :, :] = data_array
		logging.info(
			"[ECMWF_convert_to_ROMS] Finished writing to file {}".format(netcdf_roms_filename))
		os.remove(netcdf_file)
		f1.close()
