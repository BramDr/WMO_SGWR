import sys
import pathlib as pl
import re
import shutil as sh
import pandas as pd
import xarray as xr

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

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
    
pyear = year
pmonth = month
if pmonth is None:
    pyear -= 1
else:
    pmonth -= 1
    if pmonth == 0:
        pyear -= 1
        pmonth = 12

pdate_pattern = f'{pyear:04d}'
if pmonth is not None:
    pdate_pattern += f'_{pmonth:02d}'

configuration_file = pl.Path('configuration/configuration.ini')
out_dir = pl.Path(f'configuration/{date_pattern}')

base_forcing_dir = pl.Path('.')
default_initialization_path = pl.Path('parameters/global_05min_release/initialConditions/non-natural/1999_master')
domains = [f'M{i:02d}' for i in range(1, 54)]

domain = domains[0]
for domain in domains:
    
    out_domain_dir = out_dir / domain
    configuration_out = out_domain_dir / configuration_file.name
    
    configuration_out.parent.mkdir(parents=True, exist_ok=True)
    sh.copy(configuration_file, configuration_out)
    
    # Adjust configuration
    with open(configuration_out, 'r') as f:
        configuration = f.read()
    
    configuration = configuration.format_map(SafeDict(date_pattern=date_pattern,
                                                      domain=domain))
    
    forcing_file = re.search(pattern=r'temperatureNC += +(.*)',
                             string=configuration).group(1)
    forcing_file = base_forcing_dir / forcing_file
    
    with xr.open_dataset(forcing_file) as forcing:
        times = forcing.time.dt.date.values
        
    sdate = times[0]
    syear = sdate.year
    smonth = sdate.month
    sday = sdate.day
    
    edate = times[-1]
    eyear = edate.year
    emonth = edate.month
    eday = edate.day
    
    output_dir = re.search(pattern=r'outputDir += +(.*)',
                           string=configuration).group(1)
    
    if year == 1950 and (month is None or month == 1):
        initialization_path = default_initialization_path
        isyear=1999
        ismonth=12
        isday=31
    else:
        isdate = sdate - pd.Timedelta('1D')
        isyear = isdate.year
        ismonth = isdate.month
        isday = isdate.day
        initialization_path = pl.Path(str(output_dir).replace(f'/{date_pattern}/',
                                                              f'/{pdate_pattern}/'))
        initialization_path = initialization_path / 'states'
    
    configuration = configuration.format(syear=f'{syear:04d}',
                                         smonth=f'{smonth:02d}',
                                         sday=f'{sday:02d}',
                                         eyear=f'{eyear:04d}',
                                         emonth=f'{emonth:02d}',
                                         eday=f'{eday:02d}',
                                         iyear=f'{isyear:04d}',
                                         imonth=f'{ismonth:02d}',
                                         iday=f'{isday:02d}',
                                         initialization_path=initialization_path)
    
    with open(configuration_out, 'w') as f:
        f.write(configuration)
        

