import os
import cdsapi

class ECMWF_tools:

	def __init__(self):
		self.server = cdsapi.Client(debug=True)

	def create_requests(self):
		years = [1980 + y for y in range(2019)]
		months=[i for i in range(1,13,1)]

		for year in years:
			for month in months:
				print("=> Downloading for year {} month {}".format(year, month))

				out_filename = "ERA5_all_yyyymm_{}{}.nc".format(year, str(month).zfill(2))
				if os.path.exists(out_filename):
					os.remove(out_filename)

				self.submit_request(year, month, out_filename)

	def submit_request(self, year, month, out_filename):

		try:
			self.server.retrieve('reanalysis-era5-single-levels', {
				'product_type': 'reanalysis',
				"year": year,
				"month": [month],
				'day': [
					'01', '02', '03',
					'04', '05', '06',
					'07', '08', '09',
					'10', '11', '12',
					'13', '14', '15',
					'16', '17', '18',
					'19', '20', '21',
					'22', '23', '24',
					'25', '26', '27',
					'28', '29', '30',
					'31',
				],
				'time': [
					'00:00', '01:00', '02:00',
					'03:00', '04:00', '05:00',
					'06:00', '07:00', '08:00',
					'09:00', '10:00', '11:00',
					'12:00', '13:00', '14:00',
					'15:00', '16:00', '17:00',
					'18:00', '19:00', '20:00',
					'21:00', '22:00', '23:00',
				],
				"variable": [
                    '10m_u_component_of_wind',
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
                ],
				'format': "netcdf",
				"area": "90/-180/44/180",
				"verbose": True,
			}, out_filename)

		except Exception as e:
			print(e)
			print("[!] -------------------------- PROBLEMS WITH {0}".format(out_filename))


if __name__ == '__main__':
	tool = ECMWF_tools()
	tool.create_requests()
