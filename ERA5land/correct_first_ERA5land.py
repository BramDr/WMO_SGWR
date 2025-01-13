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

adjusted_dir = pl.Path(f'data/adjusted/{date_pattern}')
corrections_dir = pl.Path('../ERA5land_reference/saves/corrections')
out_dir = pl.Path(f'data/corrected-first/{date_pattern}')
dataset_type = 'hourly'

factor_file = corrections_dir / f'w5e5-era5land_before-factor_1981-2019.nc'
threshold_file = corrections_dir / f'w5e5_threshold_1981-2019.nc'

with xr.open_dataarray(factor_file) as correction_factor:
    pass
with xr.open_dataarray(threshold_file) as drizzle_threshold:
    pass

adjusted_files = list(adjusted_dir.rglob('*.nc'))
adjusted_files = sorted(adjusted_files)

adjusted_file = adjusted_files[0]
for adjusted_file in adjusted_files:
    print(f'adjusted_file: {adjusted_file}')
    
    corrected_out = out_dir / adjusted_file.relative_to(adjusted_dir)
    if corrected_out.exists():
        print(f'corrected_out exists: {corrected_out}')
        continue

    # Load
    with xr.open_dataarray(adjusted_file) as adjusted:
        pass
    
    correction_factor_adjusted = correction_factor.sel(month=adjusted.time.dt.month)
    drizzle_threshold_adjusted = drizzle_threshold.expand_dims({'time': adjusted.time})
    
    # Correct
    adjusted = adjusted * correction_factor_adjusted.values
    adjusted = xr.where(adjusted < drizzle_threshold.values, 0, adjusted)

    # Save
    corrected_tmp = corrected_out.with_suffix('.tmp.nc')
    corrected_tmp.parent.mkdir(parents=True, exist_ok=True)
    encoding = {adjusted.name: {'zlib': True,
                                 'complevel': 3,
                                 '_FillValue': np.nan,
                                 'missing_value': np.nan,
                                 'chunksizes': (1, adjusted.shape[1], adjusted.shape[2])}}
    adjusted.to_netcdf(corrected_tmp, encoding=encoding)
    corrected_tmp.rename(corrected_out)