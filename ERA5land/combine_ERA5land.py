import pathlib as pl
import sys
import pandas as pd
import numpy as np
import xarray as xr

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

previous_year = year
previous_month = month
if previous_month is None:
    previous_year -= 1
else:
    previous_month -= 1
    if previous_month == 0:
        previous_year -= 1
        previous_month = 12

previous_date_pattern = f'{previous_year:04d}'
if previous_month is not None:
    previous_date_pattern += f'_{previous_month:02d}'

corrected_dir = pl.Path(f'data/corrected-second/{date_pattern}')
out_dir = pl.Path(f'data/combined/{date_pattern}')

corrected_files = list(corrected_dir.rglob('*.nc'))
corrected_files = [f for f in corrected_files if f.parent.stem == 'daily']
corrected_files = sorted(corrected_files)

corrected_file = corrected_files[0]
for corrected_file in corrected_files:
    print(f'corrected_file: {corrected_file}')
    
    combined_out = out_dir / corrected_file.relative_to(corrected_dir)
    if combined_out.exists():
        print(f'combined_out exists: {combined_out}')
        continue
    
    with xr.open_dataarray(corrected_file) as corrected:
        pass
    
    corrected_time = corrected.time.values
    stime = corrected_time[0] - pd.Timedelta(1, 'D')
    etime = corrected_time[-1] - pd.Timedelta(1, 'D')
    
    # Daily datasets have to be combined due to the time shift in the hourly datasets
    # Hourly datasets is shifted by 1 day
    # Thus the last day of the previous month (or year) needs to be added
    # And the last day of the current month (or year) needs to be removed
    
    if year != 1950 or month != 1:
        previous_corrected_dir = corrected_dir.parent / f'{previous_date_pattern}'
        previous_corrected_file = previous_corrected_dir / corrected_file.relative_to(corrected_file.parent.parent)
        
        if not previous_corrected_file.exists():
            raise FileNotFoundError(f'previous_corrected_file does not exist: {previous_corrected_file}')
        
        with xr.open_dataarray(previous_corrected_file) as previous_corrected:
            pass
        
        corrected = xr.concat([previous_corrected, corrected], dim='time')
    
    corrected = corrected.sel(time=slice(stime, etime))
        
    combined_tmp = combined_out.with_suffix('.tmp.nc')
    combined_tmp.parent.mkdir(parents=True, exist_ok=True)
    encoding = {corrected.name: {'zlib': True,
                                 'complevel': 3,
                                 '_FillValue': np.nan,
                                 'missing_value': np.nan,
                                 'chunksizes': (1, corrected.shape[1], corrected.shape[2])}}
    corrected.to_netcdf(combined_tmp, encoding=encoding)
    combined_tmp.rename(combined_out)