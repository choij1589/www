#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/TopHNT_Muon_v0.py NUM_Mu17Leg1_DEN_TopHNT_2018 --step fit --set 0 --member 0 --sim --bin $1 --no-condor
exit $?
