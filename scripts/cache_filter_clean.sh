data=$(cat)
temp_out=$(mktemp)
echo "$data" > $temp_out
jupyter nbconvert --to notebook --config convert_config.py $temp_out --output $temp_out.ipynb
jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True $temp_out.ipynb --output $temp_out.ipynb
data=$(<$temp_out.ipynb)
echo "$data"
