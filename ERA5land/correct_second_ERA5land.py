import pathlib as pl
import sys
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

corrected_dir = pl.Path(f'data/corrected-first/{date_pattern}')
corrections_dir = pl.Path('../ERA5land_reference/saves/corrections')
out_dir = pl.Path(f'data/corrected-second/{date_pattern}')

factor_file = corrections_dir / f'w5e5-era5land_after-factor_1981-2019.nc'

with xr.open_dataarray(factor_file) as correction_factor:
    pass

corrected_files = list(corrected_dir.rglob('*.nc'))
corrected_files = sorted(corrected_files)

corrected_file = corrected_files[0]
for corrected_file in corrected_files:
    print(f'corrected_file: {corrected_file}')
    
    corrected_out = out_dir / corrected_file.relative_to(corrected_dir)
    if corrected_out.exists():
        print(f'corrected_out exists: {corrected_out}')
        continue

    # Load
    with xr.open_dataarray(corrected_file) as corrected:
        pass
    
    correction_factor_corrected = correction_factor.sel(month=corrected.time.dt.month)
    
    # Correct
    corrected = corrected * correction_factor_corrected.values
    
    # Save
    corrected_tmp = corrected_out.with_suffix('.tmp.nc')
    corrected_tmp.parent.mkdir(parents=True, exist_ok=True)
    encoding = {corrected.name: {'zlib': True,
                                 'complevel': 3,
                                 '_FillValue': np.nan,
                                 'missing_value': np.nan,
                                 'chunksizes': (1, corrected.shape[1], corrected.shape[2])}}
    corrected.to_netcdf(corrected_tmp, encoding=encoding)
    corrected_tmp.rename(corrected_out)