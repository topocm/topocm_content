cd ..
p="$PWD"
ipython nbconvert --to=notebook --inplace *.ipynb
find ./* -type d | while read -r line;
do
	STR="$p$line";
	cd "${STR//.}" && ipython nbconvert --to=notebook --inplace *.ipynb;
done;
