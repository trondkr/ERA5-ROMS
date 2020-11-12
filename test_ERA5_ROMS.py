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
		self.convert = ECMWF_convert_to_ROMS.ECMWF_convert_to_ROMS()


class TestInit(TestECMWF_init):

	def test_init_setup_config(self):
		self.assertIsNotNone(self.convert)
		self.assertIsNotNone(self.convert.plotter)



if __name__ == "__main__":
	unittest.main()
