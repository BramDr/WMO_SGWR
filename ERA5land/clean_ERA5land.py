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

data_dir = pl.Path(f'data')
out_dir = pl.Path(f'data')
remove_info = {pl.Path(f'regridded/{date_pattern}'): ['d2m', 'sp', 't2m', 'u10', 'v10', 'ssrd', 'strd', 'tp'],
               pl.Path(f'adjusted/{date_pattern}'): ['d2m', 'sp', 't2m', 'u10', 'v10', 'ssrd', 'strd', 'tp'],
               pl.Path(f'corrected-first/{date_pattern}'): ['d2m', 'sp', 't2m', 'u10', 'v10', 'ssrd', 'strd', 'tp'],
               pl.Path(f'corrected-second/{date_pattern}/daily'): ['d2m', 'sp', 't2m', 'u10', 'v10']}

remove_dir, remove_vars = next(iter(remove_info.items()))
for remove_dir, remove_vars in remove_info.items():
    print(f'remove_dir: {remove_dir}')
    
    data_remove_dir = data_dir / remove_dir
    
    data_files = []
    for remove_var in remove_vars:
        var_name = f'ERA5land_{remove_var}.nc'
        var_files = list(data_remove_dir.rglob(var_name))
        var_files = sorted(var_files)
        data_files += var_files
        
    if len(data_files) == 0:
        continue
    
    for data_file in data_files:
        print(f'data_file: {data_file}')
        data_file.unlink()
    
    remaining_files = list(data_remove_dir.rglob('*.nc'))
    if len(remaining_files) == 0:
        sh.rmtree(data_remove_dir)
        print(f'removed data_remove_dir: {data_remove_dir}')
