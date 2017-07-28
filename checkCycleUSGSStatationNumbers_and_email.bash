#!/bin/bash

module load netcdf4-python

export PYTHONPATH=$PYTHONPATH:/gpfs/sss/nwc/shared/Zhengtao.Cui/python_local/lib64/python2.6/site-packages:/gpfs/hps/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy

if [ ! -e "/gpfs/hps/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations" ]; then mkdir -p /gpfs/hps/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations; fi

cd /gpfs/hps/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations

/gpfs/hps/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/plotRealtimeCycleUSGSStatationNumbers.py -i /gpfs/hps/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations/real_time_station_numbers.txt -o CycleNumberOfUSGSStations.pdf -t "USGS number of stations by cycle" > /gpfs/hps/ptmp/Zhengtao.Cui/cycle_usgs_num_of_stations/plot.log 2>&1

echo -e "USGS number of stations as seen by model at each cycle." | mail -s "Real-time USGS Number of Stations versus cycle" -a ./CycleNumberOfUSGSStations.pdf -r 'Zhengtao.Cui@noaa.gov' Zhengtao.Cui@noaa.gov,brian.cosgrove@noaa.gov,jamesmcc@ucar.edu,gochis@ucar.edu 
