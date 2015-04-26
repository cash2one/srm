#!/bin/sh
echo "START"
source virtualenvwrapper.sh
workon  django16
export PYTHONPATH=$PYTHONPATH:/home/dsyhan/srm
cd /home/dsyhan/srm/rank_engine
echo "executing rank_monitor"
python rank_monitor.py
deactivate
echo "END"