from typing import Literal
import pathlib as pl
import pickle as pkl

import cdsapi


def submit_request(dataset: str,
                   request: dict):
    client = cdsapi.Client(wait_until_complete=False)
    response = client.retrieve(name=dataset, request=request)
    return response


def build_request(variable: str,
                  year: int,
                  month: int | None = None):

    months = [f'{m:02d}' for m in range(1, 13)]
    if month is not None:
        months = f'{int(month):02d}'

    request = {}
    request['variable'] = [variable]
    request['year'] = f'{year:04d}'
    request['month'] = months
    request['data_format'] = 'netcdf'
    request['download_format'] = 'unarchived'

    return request


def submit_ERA5land_hourly(variable: str,
                           year: int,
                           month: int | None = None):

    dataset = 'reanalysis-era5-land'
    days = [f'{d:02d}' for d in range(1, 32)]
    time = '00:00'

    request = build_request(variable=variable,
                            year=year,
                            month=month,)
    request['day'] = days
    request['time'] = [time]

    response = submit_request(dataset=dataset,
                              request=request)
    return response


def submit_ERA5land_daily(variable: str,
                          year: int,
                          month: int | None = None):

    dataset = 'derived-era5-land-daily-statistics'
    days = [f'{d:02d}' for d in range(1, 32)]
    daily_statistic = 'daily_mean'
    time_zone = 'utc+00:00'
    frequency = '1_hourly'

    request = build_request(variable=variable,
                            year=year,
                            month=month,)
    request['day'] = days
    request['daily_statistic'] = daily_statistic
    request['time_zone'] = time_zone
    request['frequency'] = frequency

    response = submit_request(dataset=dataset,
                              request=request)
    return response


def submit_ERA5land(variable: str,
                    dataset_type: Literal['hourly', 'daily'],
                    year: int,
                    month: int | None = None):

    submit_fn = None
    if dataset_type == 'hourly':
        submit_fn = submit_ERA5land_hourly
    elif dataset_type == 'daily':
        submit_fn = submit_ERA5land_daily
    else:
        raise ValueError(f'Invalid dataset type \'{dataset_type}\'')

    response = submit_fn(variable=variable,
                         year=year,
                         month=month)
    return response
