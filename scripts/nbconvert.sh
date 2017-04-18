#!/bin/bash
export MPLCONFIGDIR=$(mktemp -d)
jupyter nbconvert --HistoryManager.enabled=False --to notebook --inplace --config scripts/config_filter_smudge.py $1
