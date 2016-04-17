#!/bin/bash
export PYTHONPATH=$PYTHONPATH:${PWD}/code
python3 -m nbconvert --to notebook --config scripts/config_filter_smudge.py --stdin --stdout
