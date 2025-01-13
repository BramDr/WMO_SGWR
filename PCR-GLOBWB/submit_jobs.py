import sys
import pathlib as pl
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

job_dir = pl.Path(f'job/{date_pattern}')

job_files = list(job_dir.rglob('*.sh'))
job_files = sorted(job_files)

for job_file in job_files:    
    os.system(f'sbatch {job_file}')