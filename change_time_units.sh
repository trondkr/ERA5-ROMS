#!/bin/bash

# The global files from ERA5 uses hours since 1948-01-01 and still uses to ocean_time as variable.
# We change the units to seconds since 1948-01-01 to avoid confusing ROMS

# /cluster/projects/nn9630k/A20/FORCING/ERA5-ROMS/halo

for filename in halo/*.nc; do
  	echo "$(basename "$filename" .nc)"
		echo "Converting: " "$filename" " to" "../halo_secs/$filename"
		#ncatted -a units,ocean_time,o,c,"seconds since 1948-01-01" $filename tmp.nc
		#ncap2 -s ocean_time*=86400 tmp.nc ../halo_secs/$filename
done
