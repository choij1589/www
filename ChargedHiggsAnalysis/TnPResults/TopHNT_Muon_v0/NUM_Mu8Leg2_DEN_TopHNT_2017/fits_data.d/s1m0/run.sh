#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/TopHNT_Muon_v0.py NUM_Mu8Leg2_DEN_TopHNT_2017 --step fit --set 1 --member 0 --data --bin $1 --no-condor
exit $?
