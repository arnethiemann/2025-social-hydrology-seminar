# Processing and plotting scripts used in the 2025 seminar "Social Hydrology: Focus Central Asia"

My codes for processing and visualizing data for the seminar paper "Social Hydrology: Central Asia", 2025. **Use at your own risk, no warranty of any kind.**

## 1. FAOSTAT

## 2. MODIS


## 3. ERA5


## 4. CMIP6

`cmip6_cds_downloader.py` downloads CMIP6 data from the Copernicus Climate Data Store (CDS) using the cdsapi Python package.

The script iterates through all combinations of model, scenario, and variable, downloads the ZIP archive as provided by CDS, extracts contained files, removes any additional auxiliary files, and removes the ZIP if successful. Errors are logged to 'error.log'.

Please use this responsibly to avoid unneccessary server load.

Usage (instructions for Linux, other OS might differ):
1. Install the cdsapi Python package. On Linux: `pip install cdsapi`.
2. Configure your ~/.cdsapirc with your CDS-API credentials. Detailed instructions can be found here: [https://cds.climate.copernicus.eu/how-to-api](https://cds.climate.copernicus.eu/how-to-api)
3. Open `cmip6_cds_downloader.py` with a text editor and adjust the lists `variables`, `models`, `scenarios`, and `years` to your needs, resp. comment out what you don't need.
4. Run: Open a terminal and run `python3 cmip6_cds_downloader.py`.

