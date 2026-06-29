import cenpy
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("census_api_key")

try:
    cenpy.set_sitekey(api_key)
except Exception:
    pass

# 1. Connect to the ACS API
conn = cenpy.remote.APIConnection('ACSDT5Y2022')

# 2. Define variables
variables_to_pull = [
    'B25070_010E',   # Rent is 50.0% or more of income
    'B08301_001E',   # Total Workers 16+
    'B08301_010E',   # Workers who commute via Public Transportation
    'B28002_001E',   # Total Households
    'B28002_004E',   # Households with Broadband of any type
    'B19013_001E',   # Median Household Income
    'B01003_001E',   # Total Population
    'B03002_003E',   # Non-Hispanic White alone
    'B03002_004E',   # Non-Hispanic Black or African American alone
    'B03002_006E',   # Non-Hispanic Asian alone
    'B03002_012E'    # Hispanic or Latino (Any race)
]

# 3. Define the exact FIPS codes
nc_cities_fips = {
    'Chapel Hill': '11800',
    'Carrboro': '10620',
    'Hillsborough': '31620',
    'Mebane': '42240'
}
state_fips = '37'
orange_county_fips = '135'

all_geographies_data = []

# --- FETCH COUNTY BASELINE ---
print("Fetching baseline data for Orange County (FIPS: 135)...")
try:
    county_data = conn.query(
        cols=variables_to_pull, 
        geo_unit=f"county:{orange_county_fips}", 
        geo_filter={"state": state_fips}
    )
    county_data['city_name'] = 'Orange County (Baseline)'
    all_geographies_data.append(county_data)
except Exception as e:
    print(f"!!! Error fetching Orange County: {e}")

# --- FETCH CITIES ---
for city_name, place_fips in nc_cities_fips.items():
    print(f"Fetching data for {city_name} (FIPS: {place_fips})...")
    try:
        city_data = conn.query(
            cols=variables_to_pull, 
            geo_unit=f"place:{place_fips}", 
            geo_filter={"state": state_fips}
        )
        city_data['city_name'] = city_name
        all_geographies_data.append(city_data)
    except Exception as e:
        print(f"!!! Error fetching {city_name}: {e}")

# --- COMBINE AND CLEAN ---
if all_geographies_data:
    final_df = pd.concat(all_geographies_data, ignore_index=True)
    
    # Convert all API strings to numeric floats so you can do math on them later
    for col in variables_to_pull:
        final_df[col] = pd.to_numeric(final_df[col], errors='coerce')
        
    # Save the master dataset
    final_df.to_csv("acs_demographics.csv", index=False)
    print("\nData collection complete! Master CSV saved.")
else:
    print("No data was collected.")