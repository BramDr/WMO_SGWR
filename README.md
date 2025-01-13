# Scripts related to WMO's State of the Global Water Resources report
The aim of these script is to have a setup that can: (1) download ERA5-land forcing from the Climate Data Store, (2) correct this forcing for drizzle days and precipitation biases, and (3) warm-run PCR-GLOBWB with this forcing. Below is a short description on how the scripts are used. All scripts can be run continuously by looping over the required years and (optional) months as shown in _run_yearly.sh_ and _run_monthly.sh_, respectively (requires _wait_jobs.py_). All data can be found on Eejit (/scratch/depfg/dropp003/WMO/SGWR).

## ERA5land_reference
Scripts under ERA5land_reference are used to generate the correction files to correct the ERA5-land precipitation  based on the W5E5 precipitation data. Corrections, after bilinear downcaling, are done per month and in three steps: (1) scaling precipitation to match W5E5, (2) removing precipitation below the W5E5 drizzle threshold, and (3) again scaling precipitation to match W5E5. Scaling and threshold values are determined by comparing ERA5-land and W5E5 over the period 1981 to 2019.

* _submit_ERA5land_reference.py_; submits download requests to the Climate Data Store and stores responses (requires _cdsapi_utils.py_)
* _download ERA5land_reference.py_; downloads data from the Climate Data Store based on stored responsess
* _regrid_ERA5land_reference.py_; downcales data from native grid (~30 arc-minutes) to 5 arc-minutes (requires _make_grid_file.py_ and _5arcmin_grid.txt_)
* _adjust_ERA5land_reference.py_; removes antarctica, adjust longitude ranges (from 0 to 360 to -180 to 180), adjust times for accumulated data
* _make_W5E5_monthly.py_ and _make_ERA5land_before_monthly.py_; stores monthly total precipitation from daily precipitation files before corrections
* _make_W5E5_ERA5land_before_corrections.py_; calculates scaling factors and drizzle thresholds for correction steps (1) and (2)
* _correct_first_ERA5land_reference.py_; applies scaling factors and drizzle thresholds to the data following correction steps (1) and (2)
* _make_ERA5land_after_monthly.py_; stores monthly total precipitation from daily precipitation files after correction steps (1) and (2)
* _make_W5E5_ERA5land_before_corrections.py_; calculates scaling factors for correction step (3)
* _correct_second_ERA5land_reference.py_; applies scaling factors to the data following correction step (3)

## ERA5land
Scripts under ERA5land are used to download, format and correct ERA5-land forcing in a consistent manner. ERA5-land variables are seperated into daily average files (e.g. temperature and pressure) and hourly accumulated files (e.g. precipitation and radiation). Scripts check if their job has already been completed to avoid re-doing work and can be called using the required years and (optional) month. All scripts can be run in sequence as shown in _run.sh_.

* _is_completed.py_; check if the year and (optional) month have already been completed
* _submit_ERA5land.py_; submits download requests to the Climate Data Store and stores responses (requires _cdsapi_utils.py_)
* _retrieve ERA5land.py_; retrieves data from the Climate Data Store based on stored responsess
* _regrid_ERA5land.py_; downcales data from native grid (~30 arc-minutes) to 5 arc-minutes (requires _make_grid_file.py_ and _5arcmin_grid.txt_)
* _adjust_ERA5land.py_; removes antarctica, adjust longitude ranges (from 0 to 360 to -180 to 180), adjust times for accumulated data
* _correct_first_ERA5land.py_; applies scaling factors and drizzle thresholds to the data following correction steps (1) and (2) under ERA5land_reference
* _correct_second_ERA5land.py_; applies scaling factors to the data following correction step (3) under ERA5land_reference
* _combine_ERA5land.py_; adds the first day of the previous year/month and removes the last day of the current year/month for daily variables to match hourly accumulated variables time range
* _clean_ERA5land.py_; cleans regridded, adjusted, corrected-first, and daily corrected-second files

## PCR-GLOBWB
Scripts under PCR-GLOBWB are used to run the PCR-GLOBWB global hydrological model using the corrected ERA5-land data. cripts check if their job has already been completed to avoid re-doing work and can be called using the required years and (optional) month. Configuration and job files are setup such that runs are spin-up using states from previous runs. The first run in spin-up using state files from the original PCR-GLOBWB 2 publication for the year 1999. All scripts can be run in sequence as shown in _run.sh_.

* _is_completed.py_; check if the year and (optional) month have already been completed
* _setup_configuration.py_; sets up the configuration files
* _setup_jobs.py_; sets up the job files
* _submit_jobs.py_; submits job files for all 5 arc-minute domains on the globe
* _clean_PCR-GLOBWB.py_; cleans configuration and job files
