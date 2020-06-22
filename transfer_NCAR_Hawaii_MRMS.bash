#!/bin/bash

HOST="ftp.rap.ucar.edu"
USER="anonymous"
PASS="zhengtao@noaa.gov"
LDIR="/gpfs/hps3/ptmp/Zhengtao.Cui/Hawaii_MRMS"    # can be empty
RDIR="/pub/gaydos/Hawaii_MRMS"

ncarlogdir="$LDIR/logs"
if [ ! -e $ncarlogdir ]; then mkdir -p $ncarlogdir; fi
                # only start if the cd was successful
#  -A 'MRMS/EXP/MultiSensor/*/MRMS_EXP_MultiSensor_QPE_01H_Pass1*' \
cd $LDIR && \
wget \
  --continue \
  --mirror \
  --no-host-directories \
  --cut-dirs=4       \
  --ftp-user=$USER    \
  --ftp-password=$PASS  \
  -a $ncarlogdir/ncar_hawaii_mrms_log.txt \
  -A '*MRMS_EXP_MultiSensor_QPE_01H_Pass1*' \
  ftp://$HOST/$RDIR
