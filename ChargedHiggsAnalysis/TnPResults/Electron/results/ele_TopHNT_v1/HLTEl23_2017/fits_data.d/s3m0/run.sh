#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/ele_TopHNT_v1.py HLTEl23_2017 --step fit --set 3 --member 0 --data --bin $1 --no-condor
exit $?
