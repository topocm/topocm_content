#!/bin/bash
python3 -m nbconvert --to notebook --config scripts/config_filter_clean.py --stdin --stdout
