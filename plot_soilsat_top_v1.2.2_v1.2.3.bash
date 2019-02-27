#!/bin/bash

#echo "Ana prod"
#./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/prod --pdycyc=2018111515 --case=analysis_assim --type=land --var=SOILSAT_TOP --tmorf=0 --title="V1.2.2 AnA 2018111515" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf V1_2_2_AnA_SOIL_TOP_2018111515_tm00.jpg
#
#echo "Ana para"
#./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/para --pdycyc=2018111515 --case=analysis_assim --type=land --var=SOILSAT_TOP --tmorf=0 --title="V1.2.3 AnA 2018111515" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf V1_2_3_AnA_SOIL_TOP_2018111515_tm00.jpg
#
#echo "short prod"
#./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/prod --pdycyc=2018111515 --case=short_range --type=land --var=SOILSAT_TOP --tmorf=6 --title="V1.2.2 Short f006 2018111515" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf V1_2_2_Short_SOIL_TOP_2018111515_f006.jpg
#
#echo "short para"
#./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/para --pdycyc=2018111515 --case=short_range --type=land --var=SOILSAT_TOP --tmorf=6 --title="V1.2.3 Short f006 2018111515" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf V1_2_3_Short_SOIL_TOP_2018111515_f006.jpg
#
##./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/prod --pdycyc=2018111506 --case=medium_range --type=land --var=SOILSAT_TOP --tmorf=6 --title="V1.2.2 Med f006 2018111506" --output="NWM_grid"
##
##convert -density 300 NWM_grid.pdf V1_2_2_Medium_SOIL_TOP_2018111506_f006.jpg
#
##./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/para --pdycyc=2018111506 --case=medium_range --type=land --var=SOILSAT_TOP --tmorf=6 --title="V1.2.3 Med f006 2018111506" --output="NWM_grid"
##
##convert -density 300 NWM_grid.pdf V1_2_3_Medium_SOIL_TOP_2018111506_f006.jpg

echo "long prod"
./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/prod --pdycyc=2018111500 --case=long_range_mem1 --type=land --var=SOILSAT_TOP --tmorf=48 --title="V1.2.2 Med f048 2018111500" --output="NWM_grid"

convert -density 300 NWM_grid.pdf V1_2_2_Long_SOIL_TOP_2018111500_f048.jpg
rm NWM_grid.pdf

echo "long para"
./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/para --pdycyc=2018111500 --case=long_range_mem1 --type=land --var=SOILSAT_TOP --tmorf=48 --title="V1.2.3 Med f048 2018111500" --output="NWM_grid"

convert -density 300 NWM_grid.pdf V1_2_3_Long_SOIL_TOP_2018111500_f048.jpg
rm NWM_grid.pdf
