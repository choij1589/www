#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/TopHNT_v1.py TopHNT_2018 --step fit --set 3 --member 0 --data --bin $1 --no-condor
exit $?
