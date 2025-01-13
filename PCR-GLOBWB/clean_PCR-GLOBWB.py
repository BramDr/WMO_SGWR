import pathlib as pl
import sys
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

pcrglobwb_dir = pl.Path(f'.')
out_dir = pl.Path(f'.')
remove_info = {pl.Path(f'configuration/{date_pattern}'): ['configuration.ini'],
               pl.Path(f'job/{date_pattern}'): ['job.sh']}

remove_dir, remove_vars = next(iter(remove_info.items()))
for remove_dir, remove_vars in remove_info.items():
    print(f'remove_dir: {remove_dir}')
    
    pcrglobwb_remove_dir = pcrglobwb_dir / remove_dir
    
    pcrglobwb_files = []
    for remove_var in remove_vars:
        var_files = list(pcrglobwb_remove_dir.rglob(remove_var))
        var_files = sorted(var_files)
        pcrglobwb_files += var_files
        
    if len(pcrglobwb_files) == 0:
        continue
    
    for pcrglobwb_file in pcrglobwb_files:
        print(f'pcrglobwb_file: {pcrglobwb_file}')
        pcrglobwb_file.unlink()
    
    remaining_files = list(pcrglobwb_remove_dir.rglob('*.nc'))
    if len(remaining_files) == 0:
        sh.rmtree(pcrglobwb_remove_dir)
        print(f'removed pcrglobwb_remove_dir: {pcrglobwb_remove_dir}')
