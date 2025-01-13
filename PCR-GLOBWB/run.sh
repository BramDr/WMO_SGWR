#!/bin/bash

set -e

year=$1
month=$2

if [ -z "$year" ]; then
    echo "Usage: $0 <year> [<month>]"
    exit 1
fi

pyear=$year
pmonth=$month
if [ -z "$month" ]; then
    pyear=$((year-1))
else
    pmonth=$((month-1))
    if [ $pmonth -eq 0 ]; then
        pmonth=12
        pyear=$((year-1))
    fi
fi

if python is_completed.py $year $month; then
    python clean_PCR-GLOBWB.py $pyear $pmonth
    echo "PCR-GLOBWB already completed for $year $month"
    exit 0
fi

echo "PCR-GLOBWB starting for $year $month"
python setup_configurations.py $year $month
python setup_jobs.py $year $month
python submit_jobs.py $year $month
python clean_PCR-GLOBWB.py $pyear $pmonth
