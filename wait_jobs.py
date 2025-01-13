import sys
import pathlib as pl
import re
import os

if len(sys.argv) < 2:
    print(f'Usage: python {sys.argv[0]} <year> [<month>]')
    sys.exit(1)

year = int(sys.argv[1])
month = None
if len(sys.argv) > 2:
    month = int(sys.argv[2])

date_pattern = f'{year:04d}'
if month is not None:
    date_pattern += f'_{month:02d}'

job_dir = pl.Path(f'PCR-GLOBWB/job/{date_pattern}')

base_configuration_dir = pl.Path('PCR-GLOBWB')
base_output_dir = pl.Path('PCR-GLOBWB')

running_jobs = ['initial']
while len(running_jobs) > 0:
    
    running_jobs = []
    uncompleted_jobs = []

    running_job_names = running = os.popen(f'squeue --format="%.30j" --me').read().split('\n')
    running_job_names = [n.strip() for n in running_job_names if n != '' and n.strip() != 'NAME']

    job_files = list(job_dir.rglob('*.sh'))
    job_files = sorted(job_files)

    for job_file in job_files:
        
        with open(job_file, 'r') as f:
            job = f.read()
        job_name = re.search(pattern=r'#SBATCH --job-name="(.*)"', string=job).group(1)
        
        if job_name in running_job_names:
            running_jobs.append(job_file)

    for job_file in job_files:
        
        with open(job_file, 'r') as f:
            job = f.read()
        configuration_file = re.search(pattern=r'configuration_file=(.*)', string=job).group(1)
        configuration_file = base_configuration_dir / configuration_file
        
        with open(configuration_file, 'r') as f:
            configuration = f.read()
        output_dir = re.search(pattern=r'outputDir += +(.*)', string=configuration).group(1)
        output_dir = base_output_dir / output_dir
        end_time = re.search(pattern=r'endTime += +(.*)', string=configuration).group(1)
        
        log_dir = output_dir / 'log'
        log_files = list(log_dir.rglob('*.log'))
        if len(log_files) == 0:
            uncompleted_jobs.append(job_file)
            continue
        
        log_file = log_files[0]
        with open(log_file, 'r') as f:
            log = f.read()
        
        if re.search(pattern=fr'reporting INFO reporting for time {end_time}', string=log) is None:
            uncompleted_jobs.append(job_file)
            continue

    print(f'{len(running_jobs)} running jobs ({len(uncompleted_jobs)} not completed)')
    
    if len(running_jobs) > 0:
        print('Sleeping for 60 seconds')
        os.system('sleep 60')

print('All jobs finished running')
if len(uncompleted_jobs) > 0:
    print('The following jobs are not completed:')
    for job_file in uncompleted_jobs:
        print(job_file)
    sys.exit(1)

