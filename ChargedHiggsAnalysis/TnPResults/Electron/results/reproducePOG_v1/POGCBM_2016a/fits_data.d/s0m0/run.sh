#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/reproducePOG_v1.py POGCBM_2016a --step fit --set 0 --member 0 --data --bin $1 --no-condor
exit $?
