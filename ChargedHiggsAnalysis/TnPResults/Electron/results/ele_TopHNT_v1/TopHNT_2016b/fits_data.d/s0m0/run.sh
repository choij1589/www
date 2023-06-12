#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/ele_TopHNT_v1.py TopHNT_2016b --step fit --set 0 --member 0 --data --bin $1 --no-condor
exit $?
