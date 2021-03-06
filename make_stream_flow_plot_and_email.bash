#!/bin/bash

module load netcdf4-python

export PYTHONPATH=$PYTHONPATH:/gpfs/sss/nwc/shared/Zhengtao.Cui/python_local/lib64/python2.6/site-packages:/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy

startpdy=`date --date 'now 6 day ago' +%Y%m%d` 
#startpdy=20170612
endpdy=`date --date 'now tomorrow' +%Y%m%d` 

srpdyh=`date --date 'now 4 day ago' +%Y%m%d`
srpdyh1=$srpdyh'00'
srpdyh2=$srpdyh'06'
srpdyh3=`date --date 'now 3 day ago' +%Y%m%d`'00'

echo $srpdyh1
echo $srpdyh2
echo $srpdyh3

if [ ! -e "/gpfs/hps3/ptmp/Zhengtao.Cui/stream_flow_plot" ]; then mkdir -p /gpfs/hps3/ptmp/Zhengtao.Cui/stream_flow_plot; fi

cd /gpfs/hps3/ptmp/Zhengtao.Cui/stream_flow_plot

#/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/plotStreamFlow.py -d /gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test -s $startpdy -e $endpdy -u 07064533 --title "V1.2 fixed dev USGS07064533 stream flow" --sr $srpdyh1,$srpdyh2,$srpdyh3 --tm0= --tm1= --tm2= -o v1_2_fixed_dev_USGS07064533 > /gpfs/hps3/ptmp/Zhengtao.Cui/stream_flow_plot/para.log 2>&1

/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/plotStreamFlow.py -d /gpfs/hps3/ptmp/Zhengtao.Cui/nwtest3comroot/com/nwm/test -s $startpdy -e $endpdy -u 07064533 --title "V1.1 fixed dev USGS07064533 stream flow" --sr $srpdyh1,$srpdyh2,$srpdyh3 --tm0= --tm1= --tm2= -o v1_1_fixed_dev_USGS07064533 > /gpfs/hps3/ptmp/Zhengtao.Cui/stream_flow_plot/para_fixed.log 2>&1

/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/plotStreamFlow.py -d /gpfs/hps/nco/ops/com/nwm/prod -s $startpdy -e $endpdy -u 07064533 --title "V1.1 not fixed prod USGS07064533 stream flow" --sr $srpdyh1,$srpdyh2,$srpdyh3 --tm0= --tm1= --tm2= -o v1_1_not_fixed_prod_USGS07064533 > /gpfs/hps3/ptmp/Zhengtao.Cui/stream_flow_plot/prod.log 2>&1

ssh luna "module load netcdf4-python; module load NetCDF-intel-sandybridge/4.2; cd /gpfs/hps3/ptmp/Zhengtao.Cui/stream_flow_plot; /gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/plotStreamFlow.py -d /gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test -s $startpdy -e $endpdy -u 07064533 --title \"V1.2 not fixed dev USGS07064533 stream flow\" --sr $srpdyh1,$srpdyh2,$srpdyh3 --tm0= --tm1= --tm2= -o v1_2_fixed_prod_USGS07064533; scp v1_2_fixed_prod_USGS07064533.pdf surge:/gpfs/hps3/ptmp/Zhengtao.Cui/stream_flow_plot"
#mail -s "USGS Number of Stations versus Time" -a ./NumberOfUSGSStations_prod.pdf -a NumberOfUSGSStations_para.pdf -r 'Zhengtao.Cui@noaa.gov' Zhengtao.Cui@noaa.gov <<< 'V1.0: NumberOfUSGSStations_prod.pdf\\n V1.1: NumberOfUSGSStations_para.pdf'
echo -e "V1.1 prod (not fixed): v1_1_not_fixed_prod_USGS07064533.pdf\nV1.2 devonprod (fixed): v1_2_fixed_prod_USGS07064533.pdf\nV1.1 dev (fixed): v1_1_fixed_dev_USGS07064533.pdf" | mail -s "USGS 07064533 Stream flow" -a  v1_1_not_fixed_prod_USGS07064533.pdf -a v1_2_fixed_prod_USGS07064533.pdf -a v1_1_fixed_dev_USGS07064533.pdf -r 'Zhengtao.Cui@noaa.gov' Zhengtao.Cui@noaa.gov,brian.cosgrove@noaa.gov,yuqiong.liu@noaa.gov

#,brian.cosgrove@noaa.gov,jamesmcc@ucar.edu,gochis@ucar.edu 
