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

regridded_dir = pl.Path(f'data/regridded/{date_pattern}')
out_dir = pl.Path(f'data/adjusted/{date_pattern}')

regridded_files = list(regridded_dir.rglob('*.nc'))
regridded_files = sorted(regridded_files)

regridded_file = regridded_files[0]
for regridded_file in regridded_files:
    print(f'regridded_file: {regridded_file}')
    
    adjusted_out = out_dir / regridded_file.relative_to(regridded_dir)
    if adjusted_out.exists():
        print(f'adjusted_out exists: {adjusted_out}')
        continue

    # Load
    with xr.open_dataarray(regridded_file) as regridded:
        pass

    # Remove antarctica
    regridded = regridded.where(regridded.latitude > -60)

    # Adjust longitudes
    # From range (0 : 360) to (-180 : 180)
    longitudes = regridded.longitude.values
    longitudes[longitudes > 180] -= 360
    regridded['longitude'] = longitudes
    regridded = regridded.sortby('longitude')

    # Adjust time
    # From D+1 00:00 to D 00:00 (only for hourly data type)
    regridded = regridded.rename({'valid_time': 'time'})
    if regridded_file.parent.stem == 'hourly':
        times = regridded.time.values
        times = times - pd.Timedelta('1D')
        regridded['time'] = times

    # Store
    adjusted_tmp = adjusted_out.with_suffix('.tmp.nc')
    adjusted_tmp.parent.mkdir(parents=True, exist_ok=True)
    encoding = {regridded.name: {'zlib': True,
                                 'complevel': 3,
                                 '_FillValue': np.nan,
                                 'missing_value': np.nan,
                                 'chunksizes': (1, regridded.shape[1], regridded.shape[2])}}
    regridded.to_netcdf(adjusted_tmp, encoding=encoding)
    adjusted_tmp.rename(adjusted_out)
