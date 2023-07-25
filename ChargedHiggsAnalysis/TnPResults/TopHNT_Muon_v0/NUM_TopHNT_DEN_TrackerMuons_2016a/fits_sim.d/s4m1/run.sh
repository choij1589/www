#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/TopHNT_Muon_v0.py NUM_TopHNT_DEN_TrackerMuons_2016a --step fit --set 4 --member 1 --sim --bin $1 --no-condor
exit $?
