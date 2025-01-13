import pathlib as pl
import xarray as xr

corrected_dir = pl.Path('data/corrected-first')
corrections_dir = pl.Path('saves/corrections')
out_dir = pl.Path('data/corrected-second')
dataset_type = 'hourly'

factor_file = corrections_dir / f'w5e5-era5land_after-factor_1981-2019.nc'

with xr.open_dataarray(factor_file) as correction_factor:
    pass

corrected_files = list(corrected_dir.glob('*.nc'))
corrected_files = sorted(corrected_files)

corrected_file = corrected_files[0]
for corrected_file in corrected_files:
    print(f'corrected_file: {corrected_file.stem}')
    
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
    corrected.to_netcdf(corrected_tmp)
    corrected_tmp.rename(corrected_out)