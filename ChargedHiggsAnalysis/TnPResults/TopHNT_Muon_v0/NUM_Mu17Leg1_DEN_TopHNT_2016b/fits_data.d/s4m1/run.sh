#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/TopHNT_Muon_v0.py NUM_Mu17Leg1_DEN_TopHNT_2016b --step fit --set 4 --member 1 --data --bin $1 --no-condor
exit $?
