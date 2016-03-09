#!/bin/bash
jupyter nbconvert --to notebook --config scripts/config_filter_clean.py --stdin --stdout
