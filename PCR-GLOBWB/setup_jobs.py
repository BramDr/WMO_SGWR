import pathlib as pl
import sys
import re
import shutil as sh

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

job_file = pl.Path('job/job.sh')
out_dir = pl.Path(f'job/{date_pattern}')

base_log_dir = pl.Path('.')
domains = [f'M{i:02d}' for i in range(1, 54)]

domain = domains[0]
for domain in domains:
    
    out_domain_dir = out_dir / domain    
    job_out = out_domain_dir / job_file.name
    
    job_out.parent.mkdir(parents=True, exist_ok=True)
    sh.copy(job_file, job_out)
    
    # Adjust job
    with open(job_out, 'r') as f:
        job = f.read()
    
    job = job.format(date_pattern=date_pattern,
                     domain=domain)
    
    log_out_file = re.search(pattern=r'#SBATCH --output=(.*)', string=job).group(1)
    log_out_file = base_log_dir / log_out_file
    log_out_file.parent.mkdir(parents=True, exist_ok=True)
    
    log_err_file = re.search(pattern=r'#SBATCH --error=(.*)', string=job).group(1)
    log_err_file = base_log_dir / log_err_file
    log_err_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(job_out, 'w') as f:
        f.write(job)
        

