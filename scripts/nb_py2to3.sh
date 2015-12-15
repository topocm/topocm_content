cd ..
p="$PWD"
script_path="$p/scripts/ipython3-versioncontrol"
point_dash="./"; dash="/"

find ./* -type d | while read -r line;
do
        STR="$p$line";
        cd "${STR//$point_dash/$dash}"
	for file in *.ipynb;
		do
		if [ "$file" != "*.ipynb" ]; then
			python $script_path/notebook_v4_to_py.py -f "$file";
			py_file_path="${file//.ipynb/.py}"
			data=$(<"$py_file_path")
			echo "${data//%run/#%run}" > $py_file_path
			2to3 -w -n "$py_file_path";
			data=$(<"$py_file_path")
			echo "${data//#%run/%run}" > $py_file_path
			python $script_path/py_to_notebook_v4.py -f "$py_file_path" --overwrite;
			rm "$py_file_path";
		fi;
		done;
done;
