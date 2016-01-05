#!/bin/bash
temp_out=$(mktemp)
mv $temp_out $temp_out.ipynb
cat > $temp_out.ipynb
jupyter nbconvert --to notebook --config scripts/convert_config.py $temp_out.ipynb --output $temp_out.ipynb 1>&2
jupyter trust $temp_out.ipynb > /dev/null
cat $temp_out.ipynb
rm $temp_out.ipynb
