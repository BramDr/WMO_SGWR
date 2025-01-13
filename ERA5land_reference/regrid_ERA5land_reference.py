import pathlib as pl
import cdo

retrieved_dir = pl.Path('data/retrieved')
grid_file = pl.Path('5arcmin_grid.txt')
out_dir = pl.Path('data/regridded')

retrieved_files = list(retrieved_dir.glob('*.nc'))
retrieved_files = sorted(retrieved_files)

retrieved_file = retrieved_files[0]
for retrieved_file in retrieved_files:
    print(f'retrieved_file: {retrieved_file.stem}')
    
    regridded_out = out_dir / retrieved_file.relative_to(retrieved_dir)
    if regridded_out.exists():
        print(f'regridded_out exists: {regridded_out}')
        continue

    operator = cdo.Cdo()
    
    regridded_tmp = regridded_out.with_suffix('.tmp.nc')
    regridded_tmp.parent.mkdir(parents=True, exist_ok=True)
    operator.remapcon(str(grid_file),
                      input=str(retrieved_file),
                      output=str(regridded_tmp),
                      options='-z zip_4')
    regridded_tmp.rename(regridded_out)