#!/bin/sh

REPO=$(git rev-parse --show-toplevel)
git config --local --remove-section filter.nbfilter
git config --local --add filter.nbfilter.clean "python $REPO/scripts/nbstrip.py"
# git config --local --add filter.nbfilter.smudge "python $REPO/scripts/nbtrust.py"
