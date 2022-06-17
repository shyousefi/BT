#!/bin/bash
#

BUND_DIRECTORY="/ukp-storage-1/krause/Thesis/data/Bundestagsprotokolle"
REICHS_DIRECTORY="/storage/nllg/compute-share/bodensohn/deuparl/DeuParl/data/5_postprocessed/Reichstag"
SENTENCE="Erfüllung dieser Aufgabe der Mitwirkung"

#echo "Checking BUND..."
output=$(grep -i -R -I "$1" $BUND_DIRECTORY)
if [ ! -z "$output" -a "$output" != " " ]; then
    file=$(grep -i -R -I -l "$1" $BUND_DIRECTORY)
    date=$(grep -oPm1 "(?<=<DATUM>)[^<]+" $file)
    echo "$output"
    echo "$date"
    exit
fi
#echo "Checking REICH..."
grep -i -R -I "$1" $REICHS_DIRECTORY
#echo "Done"