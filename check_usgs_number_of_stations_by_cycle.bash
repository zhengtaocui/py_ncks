#!/bin/bash

#module load netcdf4-python
module load python

#export PYTHONPATH=$PYTHONPATH:/gpfs/sss/nwc/shared/Zhengtao.Cui/python_local/lib64/python2.6/site-packages:/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy

pdy=`date +%Y%m%d` 
cycle=`date +%H` 

if [ "$cycle" == "09" ]; then
   mv /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations/real_time_station_numbers.txt  /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations/real_time_station_numbers.txt.bak
   mv /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations/checkCycle.log /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations/checkCycle.log.bak
fi

if [ ! -e "/gpfs/hps3/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations" ]; then mkdir -p /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations; fi

cd /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations

/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/checkCycleUSGSStatationNumbers.py -d /gpfs/hps/nco/ops/com/nwm/prod -p $pdy -c $cycle -o /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations/real_time_station_numbers.txt >> /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations/checkCycle.log 2>&1

