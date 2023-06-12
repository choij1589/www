#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/ele_TopHNT_v1.py HLTEl23_2018 --step fit --set 1 --member 0 --data --bin $1 --no-condor
exit $?
