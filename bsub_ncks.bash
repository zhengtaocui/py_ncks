#!/bin/bash

if [ ! -e "/gpfs/hps/ptmp/Zhengtao.Cui/testncky" ]; then mkdir -p /gpfs/hps/ptmp/Zhengtao.Cui/testncky; fi

if [ ! -e "/gpfs/hps/ptmp/Zhengtao.Cui/testnckylog" ]; then mkdir -p /gpfs/hps/ptmp/Zhengtao.Cui/testnckylog; fi

cd /gpfs/hps/ptmp/Zhengtao.Cui/testnckylog

if [ -e "ncks.bsub" ]; then rm -f "ncks.bsub";  fi

cat > ncks.bsub << EOF
#!/bin/bash
#BSUB -J ncks    # Job name
#BSUB -o ncks.out                     # output filename
#BSUB -e ncks.err                     # error filename
#BSUB -L /bin/sh                     # shell script
#BSUB -q "dev_shared"                       # queue
#BSUB -W 12:00                       # wallclock time - timing require to complete run
#BSUB -P "NWM-T2O"                   # Project name
#BSUB  -R 'span[ptile=10]'
#BSUB -M 12288                 # where ## is memory in MB

source $HOME/.bashrc

#/gpfs/hps/nwc/noscrub/Zhengtao.Cui/py_ncks/ncks.py -i /gpfs/hps/ptmp/Cham.Pham/com/nwm/test -o /gpfs/hps/ptmp/Zhengtao.Cui/testncky > /gpfs/hps/ptmp/Zhengtao.Cui/testnckylog/ncks.log
/gpfs/hps/nwc/noscrub/Zhengtao.Cui/py_ncks/ncks.py -i /gpfs/hps/nco/ops/com/nwm/para -o /gpfs/hps/ptmp/Zhengtao.Cui/testncky > /gpfs/hps/ptmp/Zhengtao.Cui/testnckylog/ncks.log
EOF

bsub  < ncks.bsub
