#!/bin/bash

set -e

years=$(seq 1950 2020)
months=$(seq 1 12)

for year in $years; do
    for month in $months; do
        echo "Running year $year month $month"

        cd ERA5land
        ./run.sh $year $month
        cd ..
        
        if [ ! -z "$pyear" ] -a [ ! -z "$pmonth"]; then
            python wait_jobs.py $pyear $pmonth
        fi

        cd PCR-GLOBWB
        ./run.sh $year $month
        cd ..

        pmonth=$month
    done
    pyear=$year
done