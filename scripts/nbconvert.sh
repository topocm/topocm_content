#!/bin/bash
export MPLCONFIGDIR=$(mktemp -d)
jupyter nbconvert --HistoryManager.hist_file=$(mktemp) --to notebook --inplace --config scripts/config_filter_smudge.py $1
