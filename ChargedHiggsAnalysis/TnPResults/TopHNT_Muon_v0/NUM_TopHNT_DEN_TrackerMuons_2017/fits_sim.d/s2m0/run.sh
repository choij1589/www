#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/TopHNT_Muon_v0.py NUM_TopHNT_DEN_TrackerMuons_2017 --step fit --set 2 --member 0 --sim --bin $1 --no-condor
exit $?
