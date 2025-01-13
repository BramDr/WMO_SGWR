import pathlib as pl
import pickle as pkl

save_dir = pl.Path('saves/responses') 
out_dir = pl.Path('data/retrieved')

response_files = list(save_dir.glob('*.pkl'))
response_files = sorted(response_files)

response_file = response_files[0]
for response_file in response_files:
    print(f'response_file: {response_file.stem}')
    
    data_out = out_dir / f'{response_file.stem}.nc'
    if data_out.exists():
        print(f'data_out exists: {data_out}')
        continue
    
    with open(response_file, 'rb') as f:
        response = pkl.load(f)
    
    data_tmp = data_out.with_suffix('.tmp.nc')
    data_tmp.parent.mkdir(parents=True, exist_ok=True)
    response.download(target=data_tmp)
    data_tmp.rename(data_out)