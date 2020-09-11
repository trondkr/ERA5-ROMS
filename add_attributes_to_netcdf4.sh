#!/bin/bash
# Add attribute "coordinates":"lon lat" to all ERA5 data

declare -a array_var_name=("evaporation" "lwrad_down" "Pair" "lwrad" "latent" "sensible" "Tair" "Uwind" "Vwind" "cloud" "rain" "Qair")
declare -a array_era_name=("e" "msdwlwrf" "msl" "msnlwrf" "mslhf" "msshf" "t2" "u10" "v10" "tcc" "tp" "q")
arraylength=${#array_var_name[@]}

for (( i=0; i<${arraylength}; i++ ));do
	for filename in halo/era5_${array_era_name[$i]}_*.nc; do
			echo "Adding attribute: $filename"
			export command="ncatted -a coordinates,${array_var_name[$i]},a,c,'lon lat' $filename"
			echo $command
			eval $command
	done
done

