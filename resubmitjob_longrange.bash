#!/bin/bash

sed -e "s|/gpfs/hps3/nwc/noscrub/Cham.Pham/nwtest/nwm.v1.1/ecf/model_envir.h|/gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.1/ecf/model_envir_run_use.h|" -e "s/# CALL executable job script here/export PDY=20171001\n# CALL executable job script here/" -e s/cyc=\%CYC\%/cyc=12/ -e s/mem=\%MEM\%/mem=04/ -e "s/nwm_long_range_mem\%MEM\%/nwm_long_range_mem4/"  -e "s|/gpfs/hps3/ptmp/Cham.Pham|/gpfs/hps3/ptmp/Zhengtao.Cui|"  -e s/\\\(q\ \"dev\"\\\)\\\|\\\(q\ dev\\\)/q\ devonprod/ /gpfs/hps3/nwc/noscrub/Zhengtao.Cui/nwtest/nwm.v1.1/ecf/test/jnwm_long_range.ecf | bsub
