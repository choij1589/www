#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/TopHNT_Muon_v0.py NUM_TopHNT_DEN_TrackerMuons_2018 --step fit --set 0 --member 0 --data --bin $1 --no-condor
exit $?
