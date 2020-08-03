import os
import pprint


class ECMWF_query:

	def __init__(self):

		# https://www.ecmwf.int/en/forecasts/access-forecasts/ecmwf-web-api
		self.use_era5 = True
		self.start_year = 1992
		self.end_year = 1999
		self.resultsdir = "results/"
		self.debug = False
		self.time_units = "days since 1948-01-01 00:00:00"

		if not os.path.exists(self.resultsdir):
			os.mkdir(self.resultsdir)
		if self.use_era5:
			self.dataset = 'era5'
			self.dataset_class = 'ea'
			self.grid = '0.25/0.25'
		else:
			self.dataset = 'interim'
			self.dataset_class = 'ei'
			self.grid = '0.75/0.75'

		self.reanalysis = 'reanalysis-era5-single-levels'  # 'reanalysis-era5-complete'
		# self.area = "70/0/55/22"  # North/West/South/East
		self.area = "90/-180/44/180"
		self.parameters = ['10m_u_component_of_wind',
						   '10m_v_component_of_wind',
						   '2m_temperature',
						   'evaporation',
						   'mean_sea_level_pressure',
						   'mean_surface_downward_long_wave_radiation_flux',
						   'mean_surface_latent_heat_flux',
						   'mean_surface_net_long_wave_radiation_flux',
						   'mean_surface_net_short_wave_radiation_flux',
						   'mean_surface_sensible_heat_flux',
						   'total_cloud_cover',
						   'total_precipitation',
						   'specific_humidity']
	def info(self):
		pprint("ERA5: \n Reanalysis: 0.25°x0.25° (atmosphere), 0.5°x0.5° (ocean waves) \n \
		Period: 1979 - present \n \
		More info on ERA5 can be found here:\n \
		https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means?tab=overview")

	# List of parameters to download:
	# https://apps.ecmwf.int/codes/grib/param-db
	# https: // apps.ecmwf.int / data - catalogues / era5 / batch / 3647799 /

	def get_parameter_metadata(self, parameter):
		return {'2m_temperature': {'parameter_id': '167.128',
								   'short_name': 't2m',
								   'roms_name': 'Tair',
								   'name': '2 metre temperature', 'units': 'K',
								   'time_name': 'Tair_time'},
				'2m_dewpoint_temperature': {'parameter_id': '168.128',
											'short_name': 'd2m',
											'roms_name': 'Qair',
											'name': '2 metre dewpoint temperature', 'units': 'K'},
				'specific_humidity': {'parameter_id': '133.128',
									  'short_name': 'q',
									  'roms_name': 'Qair',
									  'name': 'specific humidity',
									  'units': 'kg kg-1'},
				'10m_v_component_of_wind': {'parameter_id': '166.128',
											'short_name': 'v10',
											'roms_name': 'Vwind',
											'name': '10 metre v-wind component',
											'units': 'm s-1'},
				'10m_u_component_of_wind': {'parameter_id': '165.128',
											'short_name': 'u10',
											'roms_name': 'Uwind',
											'name': '10 metre u-wind component',
											'units': 'm s-1'},
				'mean_sea_level_pressure': {'parameter_id': '151.128',
											'short_name': 'msl',
											'roms_name': 'Pair',
											'name': 'Mean sea level pressure',
											'units': 'Pa'},
				'total_cloud_cover': {'parameter_id': '164.128',
									  'short_name': 'tcc',
									  'roms_name': 'cloud',
									  'name': 'Total cloud cover',
									  'units': '(0-1)'},
				'total_precipitation': {'parameter_id': '228.128',
										'short_name': 'tp',
										'roms_name': 'rain',
										'name': 'Total precipitation',
										'units': 'm'},
				'mean_surface_net_short_wave_radiation_flux': {'parameter_id': '37.235',
															   'short_name': 'msnswrf',
															   'roms_name': 'swrad',
															   'name': 'Mean surface net short-wave radiation flux',
															   'units': 'W m-2'},
				'mean_surface_net_long_wave_radiation_flux': {'parameter_id': '38.235',
															  'short_name': 'msnlwrf',
															  'roms_name': 'lwrad',
															  'name': 'Mean surface net long-wave radiation flux',
															  'units': 'W m-2',
															  'time_name': 'swrad_time'},
				'mean_surface_downward_long_wave_radiation_flux': {'parameter_id': '36.235',
																   'short_name': 'msdwlwrf',
																   'roms_name': 'lwrad_down',
																   'name': 'Mean surface downward long-wave radiation flux',
																   'units': 'W m-2',
																   'time_name': 'lwrad_time'},
				'mean_surface_latent_heat_flux': {'parameter_id': '34.235',
												  'short_name': 'mslhf',
												  'roms_name': 'latent',
												  'name': 'Surface latent heat flux',
												  'units': 'W m-2'},
				'mean_surface_sensible_heat_flux': {'parameter_id': '33.235',
													'short_name': 'msshf',
													'roms_name': 'sensible',
													'name': 'Surface sensible heat flux', 'units': 'W m-2'},
				'evaporation': {'parameter_id': '182.128',
								'short_name': 'e',
								'roms_name': 'evaporation',
								'name': 'Evaporation',
								'units': 'm of water equivalent'}}[parameter]
