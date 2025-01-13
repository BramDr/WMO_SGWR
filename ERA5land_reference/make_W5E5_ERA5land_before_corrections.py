import pathlib as pl
import xarray as xr

w5e5_dir = pl.Path('/scratch/depfg/sutan101/data/isimip_forcing/w5e5_version_2.0/downloaded_on_2021-06-09')
w5e5_monthly_dir = pl.Path('saves/corrections/monthly')
era5land_monthly_dir = pl.Path('saves/corrections/before-monthly')
out_dir = pl.Path('saves/corrections')

factor_out = out_dir / 'w5e5-era5land_before-factor_1981-2019.nc'
threshold_out = out_dir / 'w5e5_threshold_1981-2019.nc'

w5e5_monthly_file = out_dir / 'w5e5_pr_1981-2019_monthly.nc'
era5land_monthly_file = out_dir / 'era5land_before-tp_1981-2019_monthly.nc'

if not w5e5_monthly_file.exists():
    print(f'processing w5e5_monthly_file: {w5e5_monthly_file}')
    
    w5e5_files = list(w5e5_monthly_dir.glob('w5e5_pr_*.nc'))
    with xr.open_mfdataset(w5e5_files) as ds:
        w5e5 = ds['pr']
        w5e5 = w5e5.sel(time=slice('1981-01-01', '2019-12-31'))
    
    w5e5_monthly = w5e5.groupby('time.month').mean()
    # w5e5_monthly.mean('month').plot()

    # Save
    w5e5_monthly_tmp = w5e5_monthly_file.with_suffix('.tmp.nc')
    w5e5_monthly_tmp.parent.mkdir(parents=True, exist_ok=True)
    w5e5_monthly.to_netcdf(w5e5_monthly_tmp)
    w5e5_monthly_tmp.rename(w5e5_monthly_file)

if not era5land_monthly_file.exists():
    print(f'processing era5land_monthly_file: {era5land_monthly_file}')

    era5land_files = list(era5land_monthly_dir.glob('era5land_tp_*.nc'))
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

if not threshold_out.exists():
    print(f'processing drizzle_out: {threshold_out}')
    
    w5e5_files = list(w5e5_dir.glob('pr_*.nc'))
    with xr.open_mfdataset(w5e5_files) as ds:
        w5e5 = ds['pr']
        w5e5 = w5e5.sel(time=slice('1981-01-01', '2019-12-31'))
        w5e5 = w5e5 * 86400 * 1e-3 # convert from mm/s to m/day
        
    drizzle_threshold = w5e5.where(w5e5 > 0).min('time')
    drizzle_threshold = xr.where(drizzle_threshold < 0.0001, 0.0001, drizzle_threshold)
    # drizzle_threshold.plot()
    
    with xr.open_dataarray(era5land_monthly_file) as era5land_monthly:
        pass
    
    drizzle_threshold = drizzle_threshold.rename({'lon': 'longitude', 'lat': 'latitude'})
    drizzle_threshold = drizzle_threshold.interp_like(era5land_monthly, method='nearest')
    drizzle_threshold = drizzle_threshold.load()
    # drizzle_threshold.plot()

    # Save
    threshold_tmp = threshold_out.with_suffix('.tmp.nc')
    threshold_tmp.parent.mkdir(parents=True, exist_ok=True)
    drizzle_threshold.to_netcdf(threshold_tmp)
    threshold_tmp.rename(threshold_out)
