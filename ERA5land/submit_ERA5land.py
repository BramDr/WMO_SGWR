import sys
import pathlib as pl
import pickle as pkl

from cdsapi_utils import submit_ERA5land

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

out_dir = pl.Path(f'saves/responses/{date_pattern}')

hourly_variables: dict = {
    "surface_solar_radiation_downwards": 'ssrd',
    # "surface_thermal_radiation_downwards": 'strd',
    "total_precipitation": 'tp',
}
daily_variables: dict = {
    "2m_dewpoint_temperature": 'd2m',
    "2m_temperature": 't2m',
    "10m_u_component_of_wind": 'u10',
    "10m_v_component_of_wind": 'v10',
    "surface_pressure": 'sp',
}

for variable in hourly_variables.keys():
    print(f'variable: {variable}')
    
    variable_name = hourly_variables[variable]
    
    response_out = out_dir / 'hourly' / f'ERA5land_{variable_name}.pkl'
    if response_out.exists():
        print(f'response_out exists: {response_out}')
        continue
    
    respose = submit_ERA5land(variable=variable,
                              dataset_type='hourly',
                              year=year,
                              month=month)
    
    response_out.parent.mkdir(parents=True, exist_ok=True)
    with open(response_out, 'wb') as f:
        pkl.dump(respose, f)

for variable in daily_variables.keys():
    print(f'variable: {variable}')
    
    variable_name = daily_variables[variable]
    
    response_out = out_dir / 'daily' / f'ERA5land_{variable_name}.pkl'
    if response_out.exists():
        print(f'response_out exists: {response_out}')
        continue
    
    respose = submit_ERA5land(variable=variable,
                              dataset_type='daily',
                              year=year,
                              month=month)
    
    response_out.parent.mkdir(parents=True, exist_ok=True)
    with open(response_out, 'wb') as f:
        pkl.dump(respose, f)