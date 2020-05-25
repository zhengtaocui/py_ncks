#!/bin/bash

reservoiroutput="/gpfs/hps3/ptmp/Zhengtao.Cui/dev/RFC_data/Reservoir"
if [ ! -e $reservoiroutput ]; then mkdir -p $reservoiroutput; fi
rfclog="/gpfs/hps3/ptmp/Zhengtao.Cui/Rfclog"

if [ ! -e $rfclog ]; then mkdir -p $rfclog; fi

cd $reservoiroutput

wget -N --user=ftpin705 --password="Kk+Y/cDerZUOhjjnx4Nfeg==" -a ${rfclog}/log.txt ftp://ftps-in1.cprk.ncep.noaa.gov/in/*[NM][BC]* 

wget -N --user=ftpin705 --password="Kk+Y/cDerZUOhjjnx4Nfeg==" -a ${rfclog}/log.txt ftp://ftps-in1.bldr.ncep.noaa.gov/in/*[NM][BC]* 

reservoirarchieve="/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/rfc_reservoir"
if [ ! -e $reservoirarchieve ]; then mkdir -p $reservoirarchieve; fi

cd $reservoirarchieve

wget -N --user=ftpin705 --password="Kk+Y/cDerZUOhjjnx4Nfeg==" -a ${rfclog}/rfc_archieve_log.txt ftp://ftps-in1.cprk.ncep.noaa.gov/in/* 

wget -N --user=ftpin705 --password="Kk+Y/cDerZUOhjjnx4Nfeg==" -a ${rfclog}/rfc_archieve_log.txt ftp://ftps-in1.bldr.ncep.noaa.gov/in/* 
