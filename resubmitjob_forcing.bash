#!/bin/bash

cyc=18
PDY=20171228

jobid=`sed -e "s|/gpfs/hps3/nwc/noscrub/Cham.Pham/nwtest/nwm.v1.2.0/ecf/model_envir.h|/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.2.0/ecf/model_envir_run_use.h|" -e "s/# CALL executable job script here/export PDY=${PDY}\n# CALL executable job script here/" -e s/cyc=\%CYC\%/cyc=${cyc}/ -e "s|/gpfs/hps3/ptmp/Cham.Pham|/gpfs/hps3/ptmp/Zhengtao.Cui|"  -e "s/\\\(q\ \"dev\"\\\)\\\|\\\(q\ dev\\\)/q\ devonprod/" /gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.2.0/ecf/test/jnwm_forcing_medium_range.ecf | bsub  | grep "Job <" | sed -r 's/.* <([0-9]+)>.*/\1/'`

echo "jobid=${jobid}"

sed -e "s|/gpfs/hps3/nwc/noscrub/Cham.Pham/nwtest/nwm.v1.2.0/ecf/model_envir.h|/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.2.0/ecf/model_envir_run_use.h|" -e "s/# CALL executable job script here/export PDY=${PDY}\n# CALL executable job script here/" -e s/cyc=\%CYC\%/cyc=${cyc}/ -e "s|/gpfs/hps3/ptmp/Cham.Pham|/gpfs/hps3/ptmp/Zhengtao.Cui|"  -e s/\\\(q\ \"dev\"\\\)\\\|\\\(q\ dev\\\)/q\ devonprod/ /gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.2.0/ecf/test/jnwm_medium_range.ecf | bsub -w "(done(${jobid})||exit(${jobid},1))"

