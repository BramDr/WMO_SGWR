import pathlib as pl
import pickle as pkl
import sys

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

save_dir = pl.Path(f'saves/responses/{date_pattern}') 
out_dir = pl.Path(f'data/retrieved/{date_pattern}')

response_files = list(save_dir.rglob('*.pkl'))
response_files = sorted(response_files)

response_file = response_files[0]
for response_file in response_files:
    print(f'response_file: {response_file}')
    
    data_out = out_dir / response_file.relative_to(save_dir).with_suffix('.nc')
    if data_out.exists():
        print(f'data_out exists: {data_out}')
        continue
    
    with open(response_file, 'rb') as f:
        response = pkl.load(f)
    
    data_tmp = data_out.with_suffix('.tmp.nc')
    data_tmp.parent.mkdir(parents=True, exist_ok=True)
    response.download(target=data_tmp)
    data_tmp.rename(data_out)