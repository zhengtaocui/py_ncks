#!/bin/bash

#./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/prod --pdycyc=2019022623 --case=forcing_short_range --type=forcing --var=T2D --tmorf=2 --start=270 --stop=320 --step=5 --title="20190226 23z f002" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf T2D_SR_Forcing_20190226_23zf002.jpg
#
#./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/prod --pdycyc=2019022623 --case=forcing_short_range --type=forcing --var=T2D --tmorf=1 --start=270 --stop=320 --step=5 --title="20190226 23z f001" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf T2D_SR_Forcing_20190226_23zf001.jpg
#
#./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/prod --pdycyc=2019022700 --case=forcing_analysis_assim --type=forcing --var=T2D --tmorf=0 --start=270 --stop=320 --step=5 --title="20190227 00z tm00" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf T2D_AnA_Forcing_20190227_00ztm00.jpg
#
#./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/prod --pdycyc=2019022701 --case=forcing_analysis_assim --type=forcing --var=T2D --tmorf=0 --start=270 --stop=320 --step=5 --title="20190227 01z tm00" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf T2D_AnA_Forcing_20190227_01ztm00.jpg
#
#./plot2DGrid.py --dir=/gpfs/hps/nco/ops/com/nwm/prod --pdycyc=2019022622 --case=forcing_short_range --type=forcing --var=T2D --tmorf=3 --start=270 --stop=320 --step=5 --title="20190226 22z f003" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf T2D_SR_Forcing_20190226_22zf003.jpg

#./plot2DGrid.py --dir=/gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test --pdycyc=2019022623 --case=forcing_short_range --type=forcing --var=T2D --tmorf=2 --start=270 --stop=320 --step=5 --title="20190226 23z f002" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf T2D_SR_Forcing_20190226_23zf002_zt.jpg
#
#./plot2DGrid.py --dir=/gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test --pdycyc=2019022623 --case=forcing_short_range --type=forcing --var=T2D --tmorf=1 --start=270 --stop=320 --step=5 --title="20190226 23z f001" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf T2D_SR_Forcing_20190226_23zf001_zt.jpg
#
#./plot2DGrid.py --dir=/gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test --pdycyc=2019022700 --case=forcing_analysis_assim --type=forcing --var=T2D --tmorf=0 --start=270 --stop=320 --step=5 --title="20190227 00z tm00" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf T2D_AnA_Forcing_20190227_00ztm00_zt.jpg
#
#./plot2DGrid.py --dir=/gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test --pdycyc=2019022701 --case=forcing_analysis_assim --type=forcing --var=T2D --tmorf=0 --start=270 --stop=320 --step=5 --title="20190227 01z tm00" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf T2D_AnA_Forcing_20190227_01ztm00_zt.jpg
#
#./plot2DGrid.py --dir=/gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test --pdycyc=2019022622 --case=forcing_short_range --type=forcing --var=T2D --tmorf=3 --start=270 --stop=320 --step=5 --title="20190226 22z f003" --output="NWM_grid"
#
#convert -density 300 NWM_grid.pdf T2D_SR_Forcing_20190226_22zf003_zt.jpg

./plot2DGrid.py --dir=/gpfs/hps3/ptmp/Zhengtao.Cui/debug/com/nwm/test --pdycyc=2019022700 --case=forcing_analysis_assim --type=forcing --var=T2D --tmorf=0 --start=270 --stop=320 --step=5 --title="20190227 00z tm00" --output="NWM_grid"

convert -density 300 NWM_grid.pdf T2D_AnA_Forcing_20190227_00ztm00_zt_debug.jpg

./plot2DGrid.py --dir=/gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test --pdycyc=2019022623 --case=forcing_short_range --type=forcing --var=T2D --tmorf=1 --start=270 --stop=320 --step=5 --title="20190226 23z f001" --output="NWM_grid"

convert -density 300 NWM_grid.pdf T2D_SR_Forcing_20190226_23zf001_zt_debug.jpg

./plot2DGrid.py --dir=/gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test --pdycyc=2019022622 --case=forcing_short_range --type=forcing --var=T2D --tmorf=2 --start=270 --stop=320 --step=5 --title="20190226 22z f002" --output="NWM_grid"

convert -density 300 NWM_grid.pdf T2D_SR_Forcing_20190226_22zf002_zt_debug.jpg
