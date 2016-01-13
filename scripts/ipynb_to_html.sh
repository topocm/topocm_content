cd ..
p="$PWD"
mkdir generated; mkdir generated/html;
jupyter nbconvert --to html --config scripts/links_config.py *.ipynb 1>&2 && mv *.html "$p/generated/html/";

find ./* -type d | while read -r line;
do
        STR="$p${line//.}"
        cd "$STR" && jupyter nbconvert --to html --config scripts/links_config.py "$STR"/*.ipynb 1>&2 && \
	{ mkdir "$p/generated/html/${line//.}"; mv *.html "$p/generated/html/${line//.}"; \
	mkdir "$p/generated/html/${line//.}/figures"; \
	rsync -avz "$STR/figures/" "$p/generated/html/${line//.}/figures"; \
	echo "$p/generated/html/${line//.}/figures"; }
done;
