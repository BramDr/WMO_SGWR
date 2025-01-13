#!/bin/bash

set -e

years=$(seq 1950 2020)

for year in $years; do
    echo "Running year $year"

    cd ERA5land
    ./run.sh $year
    cd ..
        
    if [ ! -z "$pyear" ]; then
        python wait_jobs.py $pyear
    fi

    cd PCR-GLOBWB
    ./run.sh $year
    cd ..
    
    pyear=$year
done