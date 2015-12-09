#!/bin/bash
temp_out=$(mktemp)
cat > $temp_out
jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True $temp_out --stdout
rm $temp_out
