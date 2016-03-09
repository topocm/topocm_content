#!/bin/bash
export PYTHONPATH=$PYTHONPATH:${PWD}/code
jupyter nbconvert --to notebook --config scripts/config_filter_smudge.py --stdin --stdout
