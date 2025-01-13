import pathlib as pl
import sys
import cdo

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

retrieved_dir = pl.Path(f'data/retrieved/{date_pattern}')
grid_file = pl.Path('5arcmin_grid.txt')
out_dir = pl.Path(f'data/regridded/{date_pattern}')

retrieved_files = list(retrieved_dir.rglob('*.nc'))
retrieved_files = sorted(retrieved_files)

retrieved_file = retrieved_files[0]
for retrieved_file in retrieved_files:
    print(f'retrieved_file: {retrieved_file}')
    
    regridded_out = out_dir / retrieved_file.relative_to(retrieved_dir)
    if regridded_out.exists():
        print(f'regridded_out exists: {regridded_out}')
        continue

    operator = cdo.Cdo()
    
    regridded_tmp = regridded_out.with_suffix('.tmp.nc')
    regridded_tmp.parent.mkdir(parents=True, exist_ok=True)
    if retrieved_file.parent.stem == 'daily':
        operator.remapbil(str(grid_file),
                          input=str(retrieved_file),
                          output=str(regridded_tmp),
                          options='-z zip_4')
    elif retrieved_file.parent.stem == 'hourly':
        operator.remapcon(str(grid_file),
                          input=str(retrieved_file),
                          output=str(regridded_tmp),
                          options='-z zip_4')
    else:
        raise ValueError(f'Unknown parent: {retrieved_file.parent.stem}')
    regridded_tmp.rename(regridded_out)