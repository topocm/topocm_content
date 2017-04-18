#!/bin/bash
export MPLCONFIGDIR=$(mktemp -d)
jupyter nbconvert --to notebook --inplace --config scripts/config_filter_smudge.py $1
