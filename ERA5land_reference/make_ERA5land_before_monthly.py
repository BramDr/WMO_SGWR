import pathlib as pl
import xarray as xr

era5land_dir = pl.Path('data/adjusted')
out_dir = pl.Path('saves/corrections/before-monthly')

year = 1981
for year in range(1981, 2020):
    print(f'year: {year}')

    era5land_out = out_dir / f'era5land_tp_{year}_monthly.nc'
    if era5land_out.exists():
        continue
    
    era5land_file = list(era5land_dir.glob(f'ERA5land_tp_{year}.nc'))[0]
    with xr.open_dataset(era5land_file) as ds:
        era5land = ds['tp']
    
    era5land_monthly = era5land.groupby('time.month').sum(min_count=1)
    era5land_monthly['month'] = xr.cftime_range(str(year), periods=12, freq='MS')
    era5land_monthly = era5land_monthly.rename({'month': 'time'})
    # era5land_monthly.mean('time').plot()

    # Save
    era5land_monthly_tmp = era5land_out.with_suffix('.tmp.nc')
    era5land_monthly_tmp.parent.mkdir(parents=True, exist_ok=True)
    era5land_monthly.to_netcdf(era5land_monthly_tmp)
    era5land_monthly_tmp.rename(era5land_out)