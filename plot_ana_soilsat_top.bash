#!/bin/bash

./plot2DGrid.py --dir=/gpfs/hps3/ptmp/Zhengtao.Cui/com.bak/nwm/test --pdycyc=2018101815 --case=analysis_assim --type=land --var=SOILSAT_TOP --tmorf=0 --title="SOILSAT TOP 2018101815" --output="NWM_grid"

convert -density 300 NWM_grid.pdf SOIL_TOP_2018101815_tm00.jpg

./plot2DGrid.py --dir=/gpfs/hps3/ptmp/Zhengtao.Cui/com.bak/nwm/test --pdycyc=2018101816 --case=analysis_assim --type=land --var=SOILSAT_TOP --tmorf=0 --title="SOILSAT TOP 2018101816" --output="NWM_grid"

convert -density 300 NWM_grid.pdf SOIL_TOP_2018101816_tm00.jpg
