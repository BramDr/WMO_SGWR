import sys
import pathlib as pl

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
    
output_dir = pl.Path(f'output/{date_pattern}')

domains = [f'M{m:02d}' for m in range(1, 54)]

uncompleted_domains = []

domain = domains[0]
for domain in domains:
    
    output_domain_dir = output_dir / domain
    
    states_dir = output_domain_dir / 'states'
    
    if not states_dir.exists():
        uncompleted_domains.append(domain)
        continue
    
    state_files = list(states_dir.rglob('*.map'))
    state_files = sorted(state_files)
    
    if len(state_files) == 0:
        uncompleted_domains.append(domain)
        continue

if len(uncompleted_domains) > 0:
    print(f'Uncompleted domains: {uncompleted_domains}')
    sys.exit(1)

