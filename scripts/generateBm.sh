#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR/../shared/data/bm"

for i in {0..4}
do
    sed -i "s/^ignore=.*/ignore=$(((i+1)*3600)).0/g" template_industrial.params
    sed -i "s/^randomSeed=.*/randomSeed=$(((i+1)*8765))/g" template_static.params
    
    bm -f "industrial$i" -I template_industrial.params ManhattanGrid
    bm -f "static$i" -I template_static.params Static
    bm CSVFile -f "industrial$i"
    bm CSVFile -f "static$i"
    bm NSFile -f "industrial$i"
    rm "static$i.movements.gz"
    rm "industrial$i.movements.gz"
    rm "industrial$i.ns_params"
done
