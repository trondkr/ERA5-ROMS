import os
import cdsapi
import ECMWF_query
import ECMWF_convert_to_ROMS
import multiprocessing
from tqdm import tqdm

# **API UUID and key**
# Before you run this toolbox make sure that you have correctly setup your $HOME/.cdsapirc file.
#
# url: https://cds.climate.copernicus.eu/api/v2
# key: 23112:f85a8914-6595-422d-af2a-de274kj38d2b
#
# Login to your account here to get these : https://cds.climate.copernicus.eu


class ECMWF_tools:
    def __init__(self):
        # https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means?tab=form
        # https://confluence.ecmwf.int/pages/viewpage.action?pageId=82870405#ERA5:datadocumentation-Table4
        # Check data availability: http://apps.ecmwf.int/datasets/

        self.config_ecmwf = ECMWF_query.ECMWF_query()
        self.server = cdsapi.Client(debug=self.config_ecmwf.debug)

    def create_requests_as_processes(self):
        processes = []
        years = [
            self.config_ecmwf.start_year + y
            for y in range(self.config_ecmwf.end_year - self.config_ecmwf.start_year)
        ]

        if not os.path.exists(self.config_ecmwf.resultsdir):
            os.mkdir(self.config_ecmwf.resultsdir)
        for year in years:

            print("=> Downloading for year {}".format(year))

            for parameter in self.config_ecmwf.parameters:
                print("=> getting data for : {} ".format(parameter))
                metadata = self.config_ecmwf.get_parameter_metadata(parameter)

                out_filename = "{}{}_{}_year_{}.nc".format(
                    self.config_ecmwf.resultsdir,
                    self.config_ecmwf.dataset,
                    metadata["short_name"],
                    year,
                )
                roms_outfile = f"{out_filename[0:-3]}_roms.nc"
                if os.path.exists(roms_outfile):
                    if not self.config_ecmwf.skip_existing_files:
                        os.remove(out_filename)
                        processes.append((parameter, str(year), out_filename))
                    else:
                        print(f"Skipping existing file: {out_filename}")
                else:
                    processes.append((parameter, str(year), out_filename))
        return processes

    def submit_request(self, req):
        parameter, year, out_filename = req
        print("Running  submit_request=",parameter,year, out_filename)
        times = [
            "00:00",
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
            "20:00",
            "21:00",
            "22:00",
            "23:00",
        ]

        if self.config_ecmwf.extract_data_every_N_hours is True:
            times = times = [
                "00:00",
                "02:00",
                "04:00",
                "06:00",
                "08:00",
                "10:00",
                "12:00",
                "14:00",
                "16:00",
                "18:00",
                "20:00",
                "22:00",
            ]

        options = {
            "product_type": "reanalysis",
            "year": year,
            "month": [
                "01",
                "02",
                "03",
                "04",
                "05",
                "06",
                "07",
                "08",
                "09",
                "10",
                "11",
                "12",
            ],
            "day": [
                "01",
                "02",
                "03",
                "04",
                "05",
                "06",
                "07",
                "08",
                "09",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
                "27",
                "28",
                "29",
                "30",
                "31",
            ],
            "time": times,
            "variable": [parameter],
            "format": "netcdf",
            "area": self.config_ecmwf.area,
#            "verbose": self.config_ecmwf.debug,
        }

        # Add more specific options for variables on pressure surfaces
        if parameter == "specific_humidity":
            self.config_ecmwf.reanalysis = "reanalysis-era5-pressure-levels"
            options["levtype"] = "pl"
            options["pressure_level"] = "1000"
        else:
            self.config_ecmwf.reanalysis = "reanalysis-era5-single-levels"

        try:
            # Do the request
            self.server.retrieve(self.config_ecmwf.reanalysis, options, out_filename)
        except Exception as e:
            print(e)
            print(
                "[!] -------------------------- PROBLEMS WITH {0}".format(out_filename)
            )

        metadata = self.config_ecmwf.get_parameter_metadata(parameter)

        converter = ECMWF_convert_to_ROMS.ECMWF_convert_to_ROMS()
        converter.convert_to_ROMS_units_standards(
            out_filename, metadata, parameter, self.config_ecmwf
        )


if __name__ == "__main__":
    tool = ECMWF_tools()
    requests = tool.create_requests_as_processes()

    pbar = tqdm(total=len(requests))

    def update(*a):
        pbar.update()

    pool = multiprocessing.Pool(processes=4)
    pool.map(tool.submit_request, requests)
    pool.close()
    pool.join()
