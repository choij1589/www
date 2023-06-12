#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/reproducePOG_v1.py POGCBM_2016b --step fit --set 2 --member 0 --sim --bin $1 --no-condor
exit $?
