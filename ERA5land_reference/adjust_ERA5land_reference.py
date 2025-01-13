import pathlib as pl
import pandas as pd
import xarray as xr

regridded_dir = pl.Path('data/regridded')
out_dir = pl.Path('data/adjusted')

regridded_files = list(regridded_dir.glob('*.nc'))
regridded_files = sorted(regridded_files)

regridded_file = regridded_files[0]
for regridded_file in regridded_files:
    print(f'regridded_file: {regridded_file.stem}')
    
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
    times = regridded.time.values
    times = times - pd.Timedelta('1D')
    regridded['time'] = times

    # Store
    adjusted_tmp = adjusted_out.with_suffix('.tmp.nc')
    adjusted_tmp.parent.mkdir(parents=True, exist_ok=True)
    regridded.to_netcdf(adjusted_tmp, encoding={regridded.name: {'zlib': True, 'complevel': 1}})
    adjusted_tmp.rename(adjusted_out)
