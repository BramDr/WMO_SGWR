import pathlib as pl
import xarray as xr

adjusted_dir = pl.Path('data/adjusted')
corrections_dir = pl.Path('saves/corrections')
out_dir = pl.Path('data/corrected-first')

factor_file = corrections_dir / f'w5e5-era5land_before-factor_1981-2019.nc'
threshold_file = corrections_dir / f'w5e5_threshold_1981-2019.nc'

with xr.open_dataarray(factor_file) as correction_factor:
    pass
with xr.open_dataarray(threshold_file) as drizzle_threshold:
    pass

adjusted_files = list(adjusted_dir.glob('*.nc'))
adjusted_files = sorted(adjusted_files)

adjusted_file = adjusted_files[0]
for adjusted_file in adjusted_files:
    print(f'adjusted_file: {adjusted_file.stem}')
    
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
    adjusted = xr.where(adjusted < drizzle_threshold_adjusted.values, 0, adjusted)

    # Save
    corrected_tmp = corrected_out.with_suffix('.tmp.nc')
    corrected_tmp.parent.mkdir(parents=True, exist_ok=True)
    adjusted.to_netcdf(corrected_tmp)
    corrected_tmp.rename(corrected_out)