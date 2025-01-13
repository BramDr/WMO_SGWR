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
remove_info = {pl.Path(f'corrected-second/{date_pattern}/hourly'): ['ssrd', 'strd', 'tp'],
               pl.Path(f'combined/{date_pattern}/daily'): ['d2m', 'sp', 't2m', 'u10', 'v10'],}

uncompleted_info = []

remove_dir, remove_vars = next(iter(remove_info.items()))
for remove_dir, remove_vars in remove_info.items():
    
    data_remove_dir = data_dir / remove_dir
    
    for remove_var in remove_vars:
        var_name = f'ERA5land_{remove_var}.nc'
        var_files = list(data_remove_dir.rglob(var_name))
        var_files = sorted(var_files)
        
        if len(var_files) == 0:
            uncompleted_info.append((remove_dir, var_name))
            continue

if len(uncompleted_info) > 0:
    print(f'Uncompleted info: {uncompleted_info}')
    sys.exit(1)
