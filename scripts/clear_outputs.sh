cd ..
p="$PWD"
jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True *.ipynb;
for file in *.nbconvert.ipynb;
do
        mv "$file" "${file//.nbconvert}";
done;

find ./* -type d | while read -r line;
do
        STR="$p$line";
        cd "${STR//.}" && jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True *.ipynb;
        for file in *.nbconvert.ipynb;
                do
                        mv "$file" "${file//.nbconvert}";
                done;
done;
