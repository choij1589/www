#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py config/reproducePOG_v1.py POGMVANoIsoWP90_2017 --step fit --set 0 --member 0 --sim --bin $1 --no-condor
exit $?
