#!/bin/bash
temp_out=$(mktemp)
mv $temp_out $temp_out.ipynb
cat > $temp_out.ipynb
jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True $temp_out.ipynb --output $temp_out.ipynb 1>&2
jupyter nbconvert --to notebook --config scripts/rmvers_config.py $temp_out.ipynb --stdout
rm $temp_out.ipynb
