#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/TopHNT_v1.py HLTEl23_2018 --step hist --set 2 --njob 100 --ijob $1 --reduction 1 --no-condor
exit $?
