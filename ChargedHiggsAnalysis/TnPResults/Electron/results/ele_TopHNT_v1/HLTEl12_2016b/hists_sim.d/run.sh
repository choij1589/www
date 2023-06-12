#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/ele_TopHNT_v1.py HLTEl12_2016b --step hist --set 1 --njob 100 --ijob $1 --reduction 1 --no-condor
exit $?
