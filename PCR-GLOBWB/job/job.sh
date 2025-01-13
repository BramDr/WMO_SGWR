#!/bin/bash

#SBATCH --job-name="{date_pattern}_{domain}"
#SBATCH --ntasks=1
#SBATCH --output=log/{date_pattern}/{domain}/log.out
#SBATCH --error=log/{date_pattern}/{domain}/log.err
#SBATCH --time=12:00:00 
#SBATCH --partition=defq

echo "SBATCH job"
echo "Started $(date '+%d/%m/%Y %H:%M:%S')"
echo "Working directory $(pwd)"

#export PCRASTER_NR_WORKER_THREADS=32

configuration_file=./configuration/{date_pattern}/{domain}/configuration.ini
runner=~/PCR-GLOBWB_model/model/deterministic_runner.py

if [ ! -f $configuration_file ]; then
    echo "Configuration file not found: $configuration_file"
    exit 1
fi
if [ ! -f $runner ]; then
    echo "Runner not found: $runner"
    exit 1
fi

# Check if run is already finished
output_dir=$(cat $configuration_file |  grep "outputDir" | sed -e "s+outputDir[[:space:]]*=[[:space:]]*++")
endTime=$(cat $configuration_file |  grep "endTime" | sed -e "s+endTime[[:space:]]*=[[:space:]]*++")

log_dir=$output_dir/log
log_file=$(find $log_dir -type f -name "*.log")

if [ -f $log_file ]; then
    echo "Log file found: $log_file"
    if grep -q "reporting INFO reporting for time $endTime" $log_file; then
        echo "Simulation already finished"
        exit 0
    fi
fi

conda run -n pcrglobwb_py3 --no-capture-output python $runner $configuration_file

echo "Finished $(date '+%d/%m/%Y %H:%M:%S')"
