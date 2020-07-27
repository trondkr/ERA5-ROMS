#!/bin/bash

# The global files from ERA5 covers -180 to -179.75 which is not full global coverage in
# ROMS. We need to add the final value to the grid which is done using CDO.
for filename in results/*.nc; do
		echo "Converting: " "$filename" " to" "halo/$(basename "$filename" .nc)_halo.nc"
    cdo sethalo,0,1 "$filename" "halo/$(basename "$filename" .nc)_halo.nc"
done
