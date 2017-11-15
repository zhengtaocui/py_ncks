#!/bin/bash

cyc=00
mem=04
PDY=20171101

jobid=`sed -e "s|/gpfs/hps3/nwc/noscrub/Cham.Pham/nwtest/nwm.v1.1/ecf/model_envir.h|/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.1/ecf/model_envir_run_use.h|" -e "s/# CALL executable job script here/export PDY=${PDY}\n# CALL executable job script here/" -e s/cyc=\%CYC\%/cyc=${cyc}/ -e s/mem=\%MEM\%/mem=${mem}/ -e "s/nwm_forcing_long_range_mem\%MEM\%/nwm_forcing_long_range_mem${mem}/"  -e "s|/gpfs/hps3/ptmp/Cham.Pham|/gpfs/hps3/ptmp/Zhengtao.Cui|"  -e "s/\\\(q\ \"dev\"\\\)\\\|\\\(q\ dev\\\)/q\ devonprod/" /gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.1/ecf/test/jnwm_forcing_long_range.ecf | bsub | grep "Job <" | cut -c6-11`

echo "jobid=${jobid}"

sed -e "s|/gpfs/hps3/nwc/noscrub/Cham.Pham/nwtest/nwm.v1.1/ecf/model_envir.h|/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.1/ecf/model_envir_run_use.h|" -e "s/# CALL executable job script here/export PDY=${PDY}\n# CALL executable job script here/" -e s/cyc=\%CYC\%/cyc=${cyc}/ -e s/mem=\%MEM\%/mem=${mem}/ -e "s/nwm_long_range_mem\%MEM\%/nwm_long_range_mem${mem}/"  -e "s|/gpfs/hps3/ptmp/Cham.Pham|/gpfs/hps3/ptmp/Zhengtao.Cui|"  -e s/\\\(q\ \"dev\"\\\)\\\|\\\(q\ dev\\\)/q\ devonprod/ /gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.1/ecf/test/jnwm_long_range.ecf | bsub -w "(done(${jobid})||exit(${jobid},1))"
