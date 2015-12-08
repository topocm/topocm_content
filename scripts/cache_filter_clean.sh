temp_out=$(mktemp)
cat > $temp_out.ipynb
jupyter nbconvert --to notebook --config scripts/convert_config.py $temp_out.ipynb --output $temp_out.ipynb 1>&2
jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True $temp_out.ipynb --output $temp_out.ipynb 1>&2
cat $temp_out.ipynb
