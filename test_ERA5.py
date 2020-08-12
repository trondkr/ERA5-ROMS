import unittest
import ECMWF_tools
import ECMWF_query
import ECMWF_convert_to_ROMS

from datetime import datetime
import numpy as np
import xarray as xr
from typing import List

class TestECMWF_init(unittest.TestCase):
	def setUp(self):
		self.tool = ECMWF_tools.ECMWF_tools()


class TestInit(TestECMWF_init):

	def test_init_setup_config(self):
		self.assertIsNotNone(self.tool.config_ecmwf)
		self.assertIsNotNone(self.tool)

	def test_server_not_null(self):
		self.assertTrue(self.tool.server)

	def test_initial_config_not_null(self):
		self.assertIsNotNone(self.tool.config_ecmwf)

	def test_initial_config_not_null(self):
		self.assertIsNotNone(self.tool.config_ecmwf.time_units)

	def test_ecmwf_class_correct(self):
		self.assertTrue(self.tool.config_ecmwf.dataset_class in ["ei","ea"])

	def test_reference_date_equal_to_ROMS_standard(self):
		self.assertTrue(self.tool.config_ecmwf.time_units=="days since 1948-01-01 00:00:00")

	def test_initial_start_and_end_dates(self):
		self.assertIsNotNone(self.tool.config_ecmwf.start_year)
		self.assertIsNotNone(self.tool.config_ecmwf.end_year)

	def test_inital_start_and_end_dates_correct_format(self):
		self.assertTrue(datetime.strptime(str(self.tool.config_ecmwf.start_year), '%Y'))
		self.assertTrue(datetime.strptime(str(self.tool.config_ecmwf.end_year), '%Y'))


	def test_initial_variable_and_table_ids_equal_length(self):
		self.assertTrue(self.tool.config_ecmwf.reanalysis)

	def test_each_variable_has_metadata(self):
		for parameter in self.tool.config_ecmwf.parameters:
			self.assertIsNotNone(self.tool.config_ecmwf.get_parameter_metadata(parameter))
			self.assertEqual(type({}), type(self.tool.config_ecmwf.get_parameter_metadata(parameter)))

	def test_each_variable_has_metadata_units(self):
		for parameter in self.tool.config_ecmwf.parameters:
			self.assertIsNotNone(self.tool.config_ecmwf.get_parameter_metadata(parameter))
			self.assertIsNotNone(self.tool.config_ecmwf.get_parameter_metadata(parameter)["units"])


if __name__ == "__main__":
	unittest.main()
