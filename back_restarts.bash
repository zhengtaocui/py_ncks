#!/bin/bash

if [ ! -e "/gpfs/hps3/ptmp/Zhengtao.Cui/back_restarts" ]; then mkdir -p /gpfs/hps3/ptmp/Zhengtao.Cui/back_restarts; fi

cd /gpfs/hps3/ptmp/Zhengtao.Cui/back_restarts

comdir=/gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test

pdy=`date --date 'now 1 day ago' +%Y%m%d` 

tarfilename=nwm.$pdy.restarts_0z_12z_hourly_nudging.tar


tar -cvf $tarfilename --transform='s|gpfs/hps3/ptmp/Zhengtao.Cui/com/nwm/test/||' $comdir/nwm.$pdy/restart/nwm.rst.00 $comdir/nwm.$pdy/restart/nwm.rst.12 $comdir/nwm.$pdy/restart/nwm.rst.0[1-9]/nudgingLastObs.*.nc $comdir/nwm.$pdy/restart/nwm.rst.1[013-9]/nudgingLastObs.*.nc $comdir/nwm.$pdy/restart/nwm.rst.2[0-3]/nudgingLastObs.*.nc > tar.log 2>&1

cp $tarfilename /gpfs/hps/nco/storage/nwm_retro/v1.2_restart_back
