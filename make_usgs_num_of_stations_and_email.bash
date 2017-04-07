#!/bin/bash

module load netcdf4-python

export PYTHONPATH=$PYTHONPATH:/gpfs/sss/nwc/shared/Zhengtao.Cui/python_local/lib64/python2.6/site-packages:/gpfs/hps/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy

startpdy=`date --date 'now 10 day ago' +%Y%m%d` 
endpdy=`date --date 'now tomorrow' +%Y%m%d` 


if [ ! -e "/gpfs/hps/ptmp/Zhengtao.Cui/usgs_num_of_stations" ]; then mkdir -p /gpfs/hps/ptmp/Zhengtao.Cui/usgs_num_of_stations; fi

cd /gpfs/hps/ptmp/Zhengtao.Cui/usgs_num_of_stations

/gpfs/hps/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/checkUSGSStatationNumbers.py -d /gpfs/hps/nco/ops/com/nwm/prod -s $startpdy -e $endpdy > /gpfs/hps/ptmp/Zhengtao.Cui/usgs_num_of_stations/prod.log 2>&1

mv NumberOfUSGSStations.pdf NumberOfUSGSStations_prod.pdf


/gpfs/hps/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/checkUSGSStatationNumbers.py -d /gpfs/hps/nco/ops/com/nwm/para -s $startpdy -e $endpdy > /gpfs/hps/ptmp/Zhengtao.Cui/usgs_num_of_stations/para.log 2>&1

mv NumberOfUSGSStations.pdf NumberOfUSGSStations_para.pdf

#mail -s "USGS Number of Stations versus Time" -a ./NumberOfUSGSStations_prod.pdf -a NumberOfUSGSStations_para.pdf -r 'Zhengtao.Cui@noaa.gov' Zhengtao.Cui@noaa.gov <<< 'V1.0: NumberOfUSGSStations_prod.pdf\\n V1.1: NumberOfUSGSStations_para.pdf'
echo -e "V1.0: NumberOfUSGSStations_prod.pdf\nV1.1: NumberOfUSGSStations_para.pdf" | mail -s "USGS Number of Stations versus Time" -a ./NumberOfUSGSStations_prod.pdf -a NumberOfUSGSStations_para.pdf -r 'Zhengtao.Cui@noaa.gov' Zhengtao.Cui@noaa.gov,brian.cosgrove@noaa.gov,jamesmcc@ucar.edu,gochis@ucar.edu 
