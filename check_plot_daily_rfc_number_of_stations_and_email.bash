#!/bin/bash

module load python

export PYTHONPATH=/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest3/nwm.v2.1/ush/rfc_ingestion:$PYTHONPATH

pdy=`date --date 'now 1 day ago' +%Y%m%d` 

if [ ! -e "/gpfs/hps3/ptmp/Zhengtao.Cui/rfc_daily_num_of_stations" ]; then mkdir -p /gpfs/hps3/ptmp/Zhengtao.Cui/rfc_daily_num_of_stations; fi

cd /gpfs/hps3/ptmp/Zhengtao.Cui/rfc_daily_num_of_stations

/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/check_daily_RFC_station_list.py -d /gpfs/hps3/nwc/noscrub/Zhengtao.Cui/usgs_canadian_timeslices/com/nwm/test -p $pdy -s /gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest3/nwm.v2.1/ush/rfc_ingestion/RFC_Reservoir_Locations_for_Forecast_Ingest_into_NWM_All_RFCs.csv -o /gpfs/hps3/ptmp/Zhengtao.Cui/rfc_daily_num_of_stations/rfc_daily_${pdy}_number_of_stations.pdf >> /gpfs/hps3/ptmp/Zhengtao.Cui/rfc_daily_num_of_stations/rfc_daily.log 2>&1

echo -e "Daily RFC number of stations summary." | mail -s "Daily Real-time RFC Number of Stations Summary" -a ./rfc_daily_${pdy}_number_of_stations.pdf -r 'Zhengtao.Cui@noaa.gov' Zhengtao.Cui@noaa.gov,brian.cosgrove@noaa.gov,jamesmcc@ucar.edu,gochis@ucar.edu,mehdi.rezaeianzadeh@noaa.gov 
