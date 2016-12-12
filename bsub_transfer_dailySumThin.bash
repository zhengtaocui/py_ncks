#!/bin/bash

if [ ! -e "/gpfs/hps/ptmp/Zhengtao.Cui/dailySumThin" ]; then mkdir -p /gpfs/hps/ptmp/Zhengtao.Cui/dailySumThin; fi

if [ ! -e "/gpfs/hps/ptmp/Zhengtao.Cui/dailySumThinlog" ]; then mkdir -p /gpfs/hps/ptmp/Zhengtao.Cui/dailySumThinlog; fi

cd /gpfs/hps/ptmp/Zhengtao.Cui/dailySumThinlog

if [ -e "ncks.bsub" ]; then rm -f "ncks.bsub";  fi

pdy=`date --date 'now 1 day ago' +%Y%m%d` 

tarfilename=/gpfs/hps/ptmp/Zhengtao.Cui/dailySumThin/nwm.fe_long_range_thin_daily_rainrate.20160905/nwm.fe_long_range_thin_daily_rainrate.20160905.tar

echo "tarfilename is $tarfilename"
target_filename=`basename $tarfilename`.`date +%Y%m%d:%H%M%S.%N`
echo "target_filename is $target_filename"

cat > ncks.bsub << EOF
#!/bin/bash
#BSUB -J dailysumtransfer    # Job name
#BSUB -o dailysumtransfer.out.%J                    # output filename
#BSUB -e dailysumtransfer.err.%J                     # error filename
#BSUB -L /bin/sh                     # shell script
#BSUB -q "dev_transfer"                       # queue
#BSUB -W 01:00                  # wallclock time - timing require to complete run
#BSUB -P "NWM-T2O"                   # Project name
##BSUB  -R 'span[ptile=10]'
#BSUB -M 12288                 # where ## is memory in MB

#source $HOME/.bashrc

curl -T $tarfilename -u anonymous:anonymous ftp://ftp.nohrsc.noaa.gov/incoming/$target_filename
EOF
#
bsub  < ncks.bsub
