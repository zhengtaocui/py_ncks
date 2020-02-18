#!/bin/bash

module load python

pdy=`date +%Y%m%d` 
cycle=`date +%H` 

if [ ! -e "/gpfs/hps3/ptmp/Zhengtao.Cui/cycle_rfc_num_of_stations" ]; then mkdir -p /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_rfc_num_of_stations; fi

if [ "$cycle" == "09" ]; then
   mv /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_rfc_num_of_stations/real_time_station_numbers.txt  /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_rfc_num_of_stations/real_time_station_numbers.txt.bak
   mv /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_rfc_num_of_stations/checkCycle.log /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_rfc_num_of_stations/checkCycle.log.bak
fi

cd /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_rfc_num_of_stations

/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/checkCycleUSGSStatationNumbers.py -d /gpfs/hps3/nwc/noscrub/Zhengtao.Cui/usgs_canadian_timeslices/com/nwm/test -p $pdy -c $cycle -o /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_rfc_num_of_stations/real_time_station_numbers.txt -t rfc >> /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_rfc_num_of_stations/checkCycle.log 2>&1

