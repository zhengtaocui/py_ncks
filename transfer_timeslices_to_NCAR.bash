#!/bin/bash

if [ ! -e "/gpfs/hps3/ptmp/Zhengtao.Cui/transfer_timeslices" ]; then mkdir -p /gpfs/hps3/ptmp/Zhengtao.Cui/transfer_timeslices; fi

cd /gpfs/hps3/ptmp/Zhengtao.Cui/transfer_timeslices

if [ -e "ts_trnsfr.bsub" ]; then rm -f "ts_trnsfr.bsub";  fi

pre_pdy=`date --date 'now 1 day ago' +%Y%m%d` 
timeslices_pre=/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/usgs_canadian_timeslices/com/nwm/test/nwm.${pre_pdy}

pdy=`date +%Y%m%d` 
timeslices_today=/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/usgs_canadian_timeslices/com/nwm/test/nwm.${pdy}

#tarfilename=/gpfs/hps/ptmp/Zhengtao.Cui/dailySumThin/nwm.fe_long_range_thin_daily_rainrate.20160905/nwm.fe_long_range_thin_daily_rainrate.20160905.tar

#echo "tarfilename is $tarfilename"
#target_filename=`basename $tarfilename`.`date +%Y%m%d:%H%M%S.%N`
#echo "target_filename is $target_filename"

cat > ts_trnsfr.bsub << EOF
#!/bin/bash
#BSUB -J timeslicestransfer    # Job name
#BSUB -o timeslicestransfer.out.%J                    # output filename
#BSUB -e timeslicestransfer.err.%J                     # error filename
#BSUB -L /bin/sh                     # shell script
#BSUB -q "dev_transfer"                       # queue
#BSUB -cwd /gpfs/hps3/ptmp/Zhengtao.Cui/transfer_timeslices
#BSUB -W 01:00                  # wallclock time - timing require to complete run
#BSUB -P "NWM-T2O"                   # Project name
##BSUB  -R 'span[ptile=10]'
#BSUB -M 12288                 # where ## is memory in MB

#source $HOME/.bashrc

ftp -inv ftp.rap.ucar.edu << END_SCRIPT
user anonymous anonymous
cd /incoming/irap/nwm/$(basename $timeslices_today)/usgs_timeslices
mdel *
cd /incoming/irap/nwm/$(basename $timeslices_today)/usace_timeslices
mdel *
cd /incoming/irap/nwm/$(basename $timeslices_today)/canada_timeslices
mdel *
cd /incoming/irap/nwm/$(basename $timeslices_today)/merged_usgs_and_ca_timeslices
mdel *
cd /incoming/irap/nwm/$(basename $timeslices_today)/rfc_timeseries
mdel *
quit
END_SCRIPT

for f in ${timeslices_today}/*/*.ncdf
do
   echo \${f}
   echo \$(basename \$(dirname \${f%/*}))/\$(basename \$(dirname \$f))/\${f##*}
   curl -u anonymous:anonymous -T \${f} --ftp-create-dirs \
   ftp://ftp.rap.ucar.edu/incoming/irap/nwm/\$(basename \$(dirname \${f%/*}))/\$(basename \$(dirname \$f))/\${f##*}
done

hr=`date +%H`
if [[ "\$hr" -le 4 ]]
then

ftp -inv ftp.rap.ucar.edu << END_SCRIPT2
user anonymous anonymous
cd /incoming/irap/nwm/$(basename $timeslices_pre)/usgs_timeslices
mdel *
cd /incoming/irap/nwm/$(basename $timeslices_pre)/usace_timeslices
mdel *
cd /incoming/irap/nwm/$(basename $timeslices_pre)/canada_timeslices
mdel *
cd /incoming/irap/nwm/$(basename $timeslices_pre)/merged_usgs_and_ca_timeslices
mdel *
cd /incoming/irap/nwm/$(basename $timeslices_pre)/rfc_timeseries
mdel *
quit
END_SCRIPT2

   for f in ${timeslices_pre}/*/*.ncdf
   do
      echo \${f}
      echo \$(basename \$(dirname \${f%/*}))/\$(basename \$(dirname \$f))/\${f##*}
      curl -u anonymous:anonymous -T \${f} --ftp-create-dirs \
      ftp://ftp.rap.ucar.edu/incoming/irap/nwm/\$(basename \$(dirname \${f%/*}))/\$(basename \$(dirname \$f))/\${f##*}
   done
fi

EOF
bsub  < ts_trnsfr.bsub
