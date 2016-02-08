#!/bin/bash
export PYTHONPATH=$PYTHONPATH:${PWD}/code
temp_out=$(mktemp)
mv $temp_out $temp_out.ipynb
cat > $temp_out.ipynb
jupyter nbconvert --to notebook --config scripts/config_filter_smudge.py $temp_out.ipynb --output $temp_out.ipynb 1>&2
jupyter trust $temp_out.ipynb > /dev/null
sed -i '' -e '$a\' $temp_out.ipynb
cat $temp_out.ipynb
rm $temp_out.ipynb
