import os
import cdsapi
import ECMWF_query
import ECMWF_convert_to_ROMS

class ECMWF_tools:

	def __init__(self):
		# https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means?tab=form
		# https://confluence.ecmwf.int/pages/viewpage.action?pageId=82870405#ERA5:datadocumentation-Table4
		# Check data availability: http://apps.ecmwf.int/datasets/

		self.config_ecmwf = ECMWF_query.ECMWF_query()
		self.server = cdsapi.Client(debug=self.config_ecmwf.debug)

	def create_requests(self):
		years = [self.config_ecmwf.start_year + y for y in range(self.config_ecmwf.end_year)]

		if not os.path.exists(self.config_ecmwf.resultsdir):
			os.mkdir(self.config_ecmwf.resultsdir)
		for year in years:

			print("=> Downloading for year {}".format(year))

			for parameter in self.config_ecmwf.parameters:
				metadata = self.config_ecmwf.get_parameter_metadata(parameter)
					print("=> getting data for : {} ".format(metadata['name']))

				out_filename = "{}{}_{}_year_{}.nc".format(self.config_ecmwf.resultsdir,
															   self.config_ecmwf.dataset,
															   "all",
															   year)
				if os.path.exists(out_filename):
					os.remove(out_filename)

				self.submit_request("all", year, out_filename)

	def submit_request(self, parameter, year, out_filename):

		options = {
			'product_type': 'reanalysis',
			"year": year,
			"month": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
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
			"variable": [parameter],
			'format': "netcdf",
			"area": self.config_ecmwf.area,
			"verbose": self.config_ecmwf.debug,
		}
		# Add more specific options for variables on pressure surfaces
		if parameter == "specific_humidity":
			self.config_ecmwf.reanalysis = "reanalysis-era5-pressure-levels"
			options["levtype"] = 'pl'
			options["pressure_level"] = '1000'
		else:
			self.config_ecmwf.reanalysis = 'reanalysis-era5-single-levels'

		try:
			# Do the request
			self.server.retrieve(self.config_ecmwf.reanalysis, options, out_filename)
		except Exception as e:
			print(e)
			print("[!] -------------------------- PROBLEMS WITH {0}".format(out_filename))

		metadata = self.config_ecmwf.get_parameter_metadata(parameter)
		converter = ECMWF_convert_to_ROMS.ECMWF_convert_to_ROMS()
 		converter.convert_to_ROMS_standards(out_filename, metadata, parameter, self.config_ecmwf)


if __name__ == '__main__':
	tool = ECMWF_tools()
	tool.create_requests()
