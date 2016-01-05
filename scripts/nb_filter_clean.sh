#!/bin/bash
temp_out=$(mktemp)
cat > $temp_out
jupyter nbconvert --to notebook --config scripts/config_filter_clean.py $temp_out --stdout
rm $temp_out
