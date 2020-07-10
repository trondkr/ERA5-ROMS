import unittest
import ECMWF_tools
import ECMWF_query
import ECMWF_convert_to_ROMS

from datetime import datetime
import numpy as np
import xarray as xr


class TestECMWF_init(unittest.TestCase):
	def setUp(self):
		self.tool = ECMWF_tools.ECMWF_tools()


class TestInit(TestECMWF_init):

	def test_init_setup_config(self):
		self.assertIsNotNone(self.tool.config_ecmwf)
		self.assertIsNotNone(self.tool)


def test_server_not_null(self):
	self.assertFalse(self.tool.server)


def test_initial_config_not_null(self):
	self.assertIsNotNone(self.cmip6.config)


def test_initial_start_and_end_dates(self):
	self.assertIsNotNone(self.cmip6.config.start_date)
	self.assertIsNotNone(self.cmip6.config.end_date)


def test_inital_start_and_end_dates_correct_format(self):
	start_date = datetime.strptime(self.cmip6.config.start_date, '%Y-%m-%d')
	end_date = datetime.strptime(self.cmip6.config.end_date, '%Y-%m-%d')
	self.assertIsInstance(start_date, datetime,
						  "Make sure that start and end date in `CMIP6_config` is of correct format `YYYY-mm-dd`")
	self.assertIsInstance(end_date, datetime,
						  "Make sure that start and end date in `CMIP6_config` is of correct format `YYYY-mm-dd`")


def test_initial_variable_and_table_ids_equal_length(self):
	self.assertTrue(len(self.cmip6.config.table_ids) == len(self.cmip6.config.variable_ids),
					"Make sure that you initialize CMIP6_config using equal length of variable ids and table ids")


if __name__ == "__main__":
	unittest.main()
