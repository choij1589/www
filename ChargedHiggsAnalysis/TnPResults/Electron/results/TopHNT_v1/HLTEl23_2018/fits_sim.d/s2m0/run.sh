#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/TopHNT_v1.py HLTEl23_2018 --step fit --set 2 --member 0 --sim --bin $1 --no-condor
exit $?
