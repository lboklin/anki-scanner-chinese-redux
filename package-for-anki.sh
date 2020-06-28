#!/usr/bin/env bash
exclusions=('./__pycache__' './models' './orig_lib' './templates' './config_saved.json')
zipfilename="chinese-text-scanner-$1.zip"
rm $zipfilename
cd ./chinese
for i in ./*; do
    doit="T"
    for ex in "${exclusions[@]}"; do
        if [[ "$i" == "$ex" ]]; then
            doit="F"
            echo "$i $ex"
        fi
    done
    if [[ $doit == "T" ]]; then
        zip -r "../${zipfilename}" $i -x "*.mp3" -x "*__pycache__*"
    fi
done
mv ../$zipfilename ../build/$zipfilename
echo "done"
