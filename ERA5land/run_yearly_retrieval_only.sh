#!/bin/bash

set -e

years=$(seq 1950 2020)

for year in $years; do
    echo "Running year $year"
    echo "ERA5land starting for $year $month"
    python submit_ERA5land.py $year $month
    python retrieve_ERA5land.py $year $month
done