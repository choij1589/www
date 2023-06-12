#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/ele_TopHNT_v1.py HLTEl23_2016b --step fit --set 2 --member 0 --sim --bin $1 --no-condor
exit $?
