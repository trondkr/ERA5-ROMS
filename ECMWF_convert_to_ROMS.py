from datetime import datetime
import netCDF4
import numpy as np
import ECMWF_plot
import os

import ECMWF_query


class ECMWF_convert_to_ROMS:

	def __init__(self):
		self.plotter = ECMWF_plot.ECMWF_plot()

	def convert_to_ROMS_standards(self, out_filename: str, metadata, parameter: str, config_ecmwf:ECMWF_query):
		dset = netCDF4.Dataset(out_filename, 'r+')

		da = dset.variables[metadata['short_name']][:]
		masked_array = np.ma.masked_where(da == dset.variables[metadata['short_name']].missing_value, da)

		if parameter in ['Mean_surface_net_short-wave_radiation_flux',
						   'Mean_surface_net_long-wave_radiation_flux',
						   'Mean_surface_downward_long-wave_radiation_flux',
						   'Mean_surface_latent_heat_flux',
						   'Mean_surface_sensible_heat_flux']:
			#masked_array = np.ma.divide(masked_array, (3600. * 3.0))
			units = 'W m**-2'

		if parameter in ['Specific_humidity']:
			units = 'kg kg-1'

		if parameter in ['10m_u_component_of_wind', '10m_v_component_of_wind']:
			units = 'm s-1'

		if parameter in ['2m_temperature', '2m_dewpoint_temperature']:
			masked_array = np.ma.subtract(masked_array, 273.15)
			units = 'Celsius'

		if parameter in ['Evaporation']:
			Rho_w = 1000  # kg m - 3
			masked_array = np.ma.multiply(masked_array, (Rho_w / (3 * 3600.)))
			units = 'kg m-2 s-1'

		if parameter in ['Mean_sea_level_pressure']:
		#	masked_array = np.ma.divide(masked_array, 100)
			units = 'Pa'

		if parameter in ['Total_cloud_cover']:
			dset.renameVariable(metadata['short_name'], 'cloud')
			units = 'nondimensional'

		if parameter in ['Total_precipitation']:
			Rho_w = 1000  # kg m - 3
			masked_array = np.ma.multiply(masked_array, (Rho_w / (3 * 3600.)))
			units = 'kg m-2 s-1'

		longitude = dset.variables['longitude'][:]
		latitude = dset.variables['latitude'][:]
		time = dset.variables['time'][:]
		dset.close()

		do_plot = False
		if do_plot:
			self.plotter.plot_data(longitude, latitude, masked_array, time, parameter)

		self.write_to_ROMS_netcdf_file(config_ecmwf,
											masked_array,
											units,
											out_filename,
											parameter,
											longitude,
											latitude,
											time)

	def write_to_ROMS_netcdf_file(self, config_ecmwf: ECMWF_query, data_array, units, netcdf_file, \
								  parameter, longitude, latitude,
								  time):
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

		netcdf_roms_filename = config_ecmwf.resultsdir+'/'+netcdf_file[0:-3] + '_roms.nc'
		if os.path.exists(netcdf_roms_filename): os.remove(netcdf_roms_filename)
		print("Writing final product to file {}".format(netcdf_roms_filename))

		f1 = netCDF4.Dataset(netcdf_roms_filename, 'w')
		f1.title = "{} ECMWF model forcing for parameter {}".format(config_ecmwf.dataset.upper(), parameter)
		f1.description = "Created by Trond Kristiansen (at) niva.no \n" \
						 "Atmospheric data on original grid but converted to ROMS units and parameter names. \n" \
						 "Files created using the ECMWF_tools toolbox: \n" \
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
		vnc.long_name = 'hours since 1900-01-01 00:00:00.0'
		vnc.units = 'hours since 1900-01-01 00:00:00.0'
		vnc.field = 'time, scalar, series'
		vnc.calendar = 'standard'
		vnc[:] = time

		vnc = f1.createVariable(metadata['roms_name'], 'd', ('ocean_time', 'lat', 'lon'), fill_value=fillval)
		vnc.long_name = 'Latitude'
		vnc.units = 'degree_north'
		vnc.standard_name = 'latitude'
		vnc.units = units
		vnc.missing_value = fillval
		vnc[:, :, :] = data_array
		print("Finished writing to file {}".format(netcdf_roms_filename))
		os.remove(netcdf_file)
		f1.close()
