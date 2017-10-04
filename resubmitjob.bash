#!/bin/bash

sed -e "s|/gpfs/hps3/nwc/noscrub/Cham.Pham/nwtest/nwm.v1.1/ecf/model_envir.h|/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.1/ecf/model_envir_run_use.h|" -e "s/# CALL executable job script here/export PDY=20171001\n# CALL executable job script here/" -e s/cyc=\%CYC\%/cyc=12/ -e "s|/gpfs/hps3/ptmp/Cham.Pham|/gpfs/hps3/ptmp/Zhengtao.Cui|"  -e s/\\\(q\ \"dev\"\\\)\\\|\\\(q\ dev\\\)/q\ devonprod/ /gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.1/ecf/test/jnwm_medium_range.ecf | bsub
