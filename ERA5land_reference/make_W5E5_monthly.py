import pathlib as pl
import numpy as np
import xarray as xr

w5e5_dir = pl.Path('/scratch/depfg/sutan101/data/isimip_forcing/w5e5_version_2.0/downloaded_on_2021-06-09')
out_dir = pl.Path('saves/corrections/monthly')

syears = []
eyears = []
w5e5_files = sorted(list(w5e5_dir.glob(f'pr_W5E5v2.0_*.nc')))
for w5e5_file in w5e5_files:
    _, _, date_range = w5e5_file.stem.split('_')
    sdate, edate = date_range.split('-')
    syear = int(sdate[:4])
    eyear = int(edate[:4])
    syears.append(syear)
    eyears.append(eyear)
syears = np.array(syears)
eyears = np.array(eyears)

year = 1982
for year in range(1981, 2020):
    print(f'year: {year}')

    w5e5_out = out_dir / f'w5e5_pr_{year}_monthly.nc'
    if w5e5_out.exists():
        continue
    
    index = np.where((syears <= year) & (eyears >= year))[0][0]
    w5e5_file = w5e5_files[index]
    with xr.open_dataset(w5e5_file) as ds:
        w5e5 = ds['pr']
        w5e5 = w5e5.sel(time=slice(f'{year}-01-01', f'{year}-12-31'))
        w5e5 = w5e5 * 86400 * 1e-3 # convert from mm/s to m/day
    
    w5e5_monthly = w5e5.groupby('time.month').sum(min_count=1)
    w5e5_monthly['month'] = xr.cftime_range(str(year), periods=12, freq='MS')
    w5e5_monthly = w5e5_monthly.rename({'month': 'time'})
    # w5e5_monthly.mean('time').plot()

    # Save
    w5e5_monthly_tmp = w5e5_out.with_suffix('.tmp.nc')
    w5e5_monthly_tmp.parent.mkdir(parents=True, exist_ok=True)
    w5e5_monthly.to_netcdf(w5e5_monthly_tmp)
    w5e5_monthly_tmp.rename(w5e5_out)