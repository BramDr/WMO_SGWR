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
    python clean_ERA5land.py $pyear $pmonth
    echo "ERA5land already completed for $year $month"
    exit 0
fi

echo "ERA5land starting for $year $month"
python submit_ERA5land.py $year $month
python retrieve_ERA5land.py $year $month
python regrid_ERA5land.py $year $month
python adjust_ERA5land.py $year $month
python correct_first_ERA5land.py $year $month
python correct_second_ERA5land.py $year $month
python combine_ERA5land.py $year $month
python clean_ERA5land.py $pyear $pmonth
