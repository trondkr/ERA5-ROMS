for file in era5*.nc
do
 name=${file##*/}
 base=${name%.nc}
 echo "$file" new file "${base}_halo.nc"
 cdo sethalo,0,1 "$file" "${base}_halo.nc"
done