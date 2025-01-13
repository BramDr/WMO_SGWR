import pathlib as pl
import xarray as xr

era5land_dir = pl.Path('saves/corrections/after-monthly')
out_dir = pl.Path('saves/corrections')

factor_out = out_dir / 'w5e5-era5land_after-factor_1981-2019.nc'

w5e5_monthly_file = out_dir / 'w5e5_pr_1981-2019_monthly.nc'
era5land_monthly_file = out_dir / 'era5land_after-tp_1981-2019_monthly.nc'

if not era5land_monthly_file.exists():
    print(f'processing era5land_monthly_file: {era5land_monthly_file}')

    era5land_files = sorted(list(era5land_dir.glob('era5land_tp_*.nc')))
    with xr.open_mfdataset(era5land_files) as ds:
        era5land = ds['tp']
        era5land = era5land.sel(time=slice('1981-01-01', '2019-12-31'))
    
    era5land_monthly = era5land.groupby('time.month').mean()
    # era5land_monthly.mean('month').plot()

    # Save
    era5land_monthly_tmp = era5land_monthly_file.with_suffix('.tmp.nc')
    era5land_monthly_tmp.parent.mkdir(parents=True, exist_ok=True)
    era5land_monthly.to_netcdf(era5land_monthly_tmp)
    era5land_monthly_tmp.rename(era5land_monthly_file)

if not factor_out.exists():
    print(f'processing factor_out: {factor_out}')
    
    with xr.open_dataarray(w5e5_monthly_file) as w5e5_monthly:
        pass
    with xr.open_dataarray(era5land_monthly_file) as era5land_monthly:
        pass
    
    w5e5_monthly = w5e5_monthly.rename({'lon': 'longitude', 'lat': 'latitude'})
    w5e5_monthly = w5e5_monthly.interp_like(era5land_monthly, method='nearest')
    w5e5_monthly = w5e5_monthly.load()
    
    correction_factor = w5e5_monthly.values / era5land_monthly
    correction_factor = xr.where(correction_factor > 100, 100, correction_factor)
    correction_factor = correction_factor.fillna(1)
    # correction_factor.mean('month').plot()

    # Save
    factor_tmp = factor_out.with_suffix('.tmp.nc')
    factor_tmp.parent.mkdir(parents=True, exist_ok=True)
    correction_factor.to_netcdf(factor_tmp)
    factor_tmp.rename(factor_out)
