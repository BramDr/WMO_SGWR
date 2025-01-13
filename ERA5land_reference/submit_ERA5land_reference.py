import pathlib as pl
import pickle as pkl

from cdsapi_utils import submit_ERA5land

out_dir = pl.Path('saves/responses')
variable = 'total_precipitation'
variable_name = 'tp'
dataset_type = 'hourly'

years = list(range(1981, 2020))

year = years[0]
for year in years:

    name = f'ERA5land_{variable_name}_{year:04d}'
    response_out = out_dir / name / f'{name}_response.pkl'
    if response_out.exists():
        print(f'response_out exists: {response_out}')
        continue
    
    respose = submit_ERA5land(variable=variable,
                              dataset_type=dataset_type,
                              year=year)
    
    response_out.parent.mkdir(parents=True, exist_ok=True)
    with open(response_out, 'wb') as f:
        pkl.dump(respose, f)