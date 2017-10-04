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

/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/py_ncks_sss_copy/plotStreamFlow.py -d /gpfs/hps/nco/ops/com/nwm/para -s $startpdy -e $endpdy -u 07064533 --title "V1.1.4 parallel USGS07064533 stream flow" --sr $srpdyh1,$srpdyh2,$srpdyh3 --tm0= --tm1= --tm2= -o v1_1_4_parallel_USGS07064533 > /gpfs/hps3/ptmp/Zhengtao.Cui/stream_flow_plot/para_fixed.log 2>&1

echo -e "V1.1.4 parallel: v1_1_4_parallel_USGS07064533.pdf" | mail -s "V1.1.4 Parallel USGS 07064533 Stream flow" -a  v1_1_4_parallel_USGS07064533.pdf -r 'Zhengtao.Cui@noaa.gov' Zhengtao.Cui@noaa.gov,brian.cosgrove@noaa.gov,yuqiong.liu@noaa.gov,jianbin.yang@noaa.gov

#,brian.cosgrove@noaa.gov,jamesmcc@ucar.edu,gochis@ucar.edu 
