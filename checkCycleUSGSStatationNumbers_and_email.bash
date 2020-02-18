#!/bin/bash

#module load netcdf4-python
#module swap python/2.7.14

#export PYTHONPATH=$PYTHONPATH:/gpfs/sss/nwc/shared/Zhengtao.Cui/python_local/lib64/python2.6/site-packages:/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy
export PYTHONPATH=$PYTHONPATH:/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy

usage()
{
     echo "usage: checkCycleUSGSStatationNumbers_and_email.bash [[ -t casetype ] | [ -h ] ]"
}


casetype='usgs'

while [ "$1" != "" ]; do 
    case $1 in
        -t | --type )           shift
                                casetype=$1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

if [[ "$casetype" == "rfc" ]]; then
   PLOT=plotRealtimeCycleRFCStatationNumbers.py
else
   PLOT=plotRealtimeCycleUSGSStatationNumbers.py
fi

if [ ! -e "/gpfs/hps3/ptmp/Zhengtao.Cui/cycle_${casetype}_num_of_stations" ]; then mkdir -p /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_${casetype}_num_of_stations; fi

cd /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_${casetype}_num_of_stations

/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/${PLOT} -i /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_${casetype}_num_of_stations/real_time_station_numbers.txt -o CycleNumberOf${casetype^^}Stations.pdf -t "${casetype^^} number of stations by cycle" > /gpfs/hps3/ptmp/Zhengtao.Cui/cycle_${casetype}_num_of_stations/plot.log 2>&1

#scp ./CycleNumberOf${casetype^^}Stations.pdf surge:/gpfs/hps3/nwc/save/Zhengtao.Cui/Real_time_${casetype^^}_Number_of_Stations/CycleNumberOf${casetype^^}Stations_$(date +"%Y_%m_%d").pdf

echo -e "${casetype^^} number of stations as seen by model at each cycle." | mail -s "Real-time ${casetype^^} Number of Stations versus cycle" -a ./CycleNumberOf${casetype^^}Stations.pdf -r 'Zhengtao.Cui@noaa.gov' Zhengtao.Cui@noaa.gov,brian.cosgrove@noaa.gov,jamesmcc@ucar.edu,gochis@ucar.edu,mehdi.rezaeianzadeh@noaa.gov 
