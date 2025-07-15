import os
import zipfile
from itertools import product
import cdsapi

# configuration

variables = [
    'near_surface_air_temperature',
    'precipitation',
    'evaporation_including_sublimation_and_transpiration',
    'total_runoff'
]

models = [
    'access_cm2',
    'access_esm1_5',
    'awi_esm_1_1_lr',
    'cesm2',
    'cesm2_waccm',
    'ec_earth3_cc',
    'ec_earth3_veg_lr',
    'hadgem3_gc31_mm',
    'inm_cm4_8',
    'inm_cm5_0',
    'mpi_esm1_2_hr',
    'noresm2_mm',
    'mpi_esm1_2_lr',
    'hadgem3_gc31_ll'
]

scenarios = [
    'historical',
    'ssp1_1_9',
    'ssp1_2_6',
    'ssp2_4_5',
    'ssp3_7_0',
    'ssp4_3_4',
    'ssp4_6_0',
    'ssp5_8_5',
    'ssp5_3_4os'
]

years = {
    'historical': [str(y) for y in range(1850, 2015)],
    'ssp1_1_9':    [str(y) for y in range(2015, 2101)],
    'ssp1_2_6':    [str(y) for y in range(2015, 2101)],
    'ssp2_4_5':    [str(y) for y in range(2015, 2101)],
    'ssp3_7_0':    [str(y) for y in range(2015, 2101)],
    'ssp4_3_4':    [str(y) for y in range(2015, 2101)],
    'ssp4_6_0':    [str(y) for y in range(2015, 2101)],
    'ssp5_8_5':    [str(y) for y in range(2015, 2101)],
    'ssp5_3_4os':    [str(y) for y in range(2015, 2101)]
}

# choose dataset
dataset_id = 'projections-cmip6'
temporal_resolution = 'monthly'
months = [f"{m:02d}" for m in range(1, 13)]

# create error logfile
default_error_log = 'error.log'

# initiaize cdsapi client
client = cdsapi.Client()

# make sure error log can be opened
open(default_error_log, 'a').close()

for model, scenario, variable in product(models, scenarios, variables):
    out_dir = os.path.join('data', model, scenario)
    os.makedirs(out_dir, exist_ok=True)

    base_name = f"{model}_{scenario}_{variable}"
    zip_path = os.path.join(out_dir, base_name + '.zip')
    nc_target_dir = out_dir

    print(f"Requesting {variable} | model={model} | scenario={scenario}...")

    request = {
        'temporal_resolution': temporal_resolution,
        'experiment': scenario,
        'variable': variable,
        'model': model,
        'month': months,
        'year': years[scenario],
    }

    try:
        # download zip archive
        result = client.retrieve(dataset_id, request)
        result.download(zip_path)

        # extract and cleanup
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # extract only .nc
            for member in zf.namelist():
                if member.endswith('.nc'):
                    zf.extract(member, nc_target_dir)
                    src = os.path.join(nc_target_dir, member)
                    dst = os.path.join(nc_target_dir, base_name + '.nc')
                    os.replace(src, dst)
                    print(f"  >> Extracted NetCDF: {dst}")
                    break
        # remove any additional files if they were extracted
        for fname in os.listdir(nc_target_dir):
            if fname.endswith('.json') or fname.endswith('.png'):
                try:
                    os.remove(os.path.join(nc_target_dir, fname))
                    print(f"  -- Removed: {fname}")
                except OSError:
                    pass
        # remove zip file after successful extraction
        os.remove(zip_path)
        print(f"  ** Removed ZIP: {zip_path}")
        print()

    except Exception as e:
        err_msg = f"ERROR processing {variable} for {model}/{scenario}: {e}\n"
        print(f"  !! {err_msg}")
        # log error centrally
        with open(default_error_log, 'a') as elog:
            elog.write(err_msg)
        continue

print("All done. Downloaded files are in 'data/'.")
