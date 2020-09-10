#!/bin/bash

# The global files from ERA5 uses hours since 1948-01-01 and still uses to ocean_time as variable.
# We change the units to seconds since 1948-01-01 to avoid confusing ROMS

# /cluster/projects/nn9630k/A20/FORCING/ERA5-ROMS/halo

ncrename -d ocean_time,swrad_time era5_msdwswrf_year_1980_roms_halo.nc
ncrename -d ocean_time,pair_time era5_msl_year_1980_roms_halo.nc
ncrename -d ocean_time,Qair_time era5_q_year_1980_roms_halo.nc
ncrename -d ocean_time,Tair_time era5_t2m_year_1980_roms_halo.nc
ncrename -d ocean_time,wind_time era5_v10_year_1980_roms_halo.nc
ncrename -d ocean_time,wind_time era5_u10_year_1980_roms_halo.nc
ncrename -d ocean_time,cloud_time era5_tcc_year_1980_roms_halo.nc
ncrename -d ocean_time,lwrad_time era5_msnlwrf_year_1980_roms_halo.nc
ncrename -d ocean_time,rain_time era5_tp_year_1980_roms_halo.nc

ncrename -v ocean_time,swrad_time era5_msdwswrf_year_1980_roms_halo.nc
ncrename -v ocean_time,pair_time era5_msl_year_1980_roms_halo.nc
ncrename -v ocean_time,qair_time era5_q_year_1980_roms_halo.nc
ncrename -v ocean_time,tair_time era5_t2m_year_1980_roms_halo.nc
ncrename -v ocean_time,wind_time era5_v10_year_1980_roms_halo.nc
ncrename -v ocean_time,wind_time era5_u10_year_1980_roms_halo.nc
ncrename -v ocean_time,cloud_time era5_tcc_year_1980_roms_halo.nc
ncrename -v ocean_time,lwrad_time era5_msnlwrf_year_1980_roms_halo.nc
ncrename -v ocean_time,rain_time era5_tp_year_1980_roms_halo.nc

ncatted -a units,swrad_time,o,c,"days since 1948-01-01 00:00:00" era5_msdwswrf_year_1980_roms_halo.nc
ncatted -a units,pair_time,o,c,"days since 1948-01-01 00:00:00" era5_msl_year_1980_roms_halo.nc
ncatted -a units,Qair_time,o,c,"days since 1948-01-01 00:00:00" era5_q_year_1980_roms_halo.nc
ncatted -a units,Tair_time,o,c,"days since 1948-01-01 00:00:00" era5_t2m_year_1980_roms_halo.nc
ncatted -a units,wind_time,o,c,"days since 1948-01-01 00:00:00" era5_v10_year_1980_roms_halo.nc
ncatted -a units,wind_time,o,c,"days since 1948-01-01 00:00:00" era5_u10_year_1980_roms_halo.nc
ncatted -a units,cloud_time,o,c,"days since 1948-01-01 00:00:00" era5_tcc_year_1980_roms_halo.nc
ncatted -a units,lwrad_time,o,c,"days since 1948-01-01 00:00:00" era5_msnlwrf_year_1980_roms_halo.nc
ncatted -a units,rain_time,o,c,"days since 1948-01-01 00:00:00" era5_tp_year_1980_roms_halo.nc
