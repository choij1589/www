#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/TopHNT_Muon_v0.py NUM_Mu8Leg2_DEN_TopHNT_2016b --step fit --set 4 --member 1 --sim --bin $1 --no-condor
exit $?
