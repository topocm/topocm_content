#!/bin/bash
export PYTHONPATH=$PYTHONPATH:${PWD}/code
temp_out=$(mktemp)
cat > $temp_out
jupyter nbconvert --to notebook --config scripts/config_filter_smudge.py $temp_out --stdout
rm $temp_out
