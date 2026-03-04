# Climate_X_-_Spectra_API_v2.0.pdf

---

## Page 1

 
 
1 
Highly Confidential 
Not for further distribution 
 
Highly Confidential 
Not for further distribution 
API Documentation 
Version 2.0 


---

## Page 2

 
 
2 
Highly Confidential 
Not for further distribution 
Version Control 
 
Version 
Date 
Details 
2.0 
26 Feb 2026 
• 
Return Period inclusion 
1.20 
9 Feb 2026 
• 
Single asset API update 
1.19 
11 Aug 2025 
• 
LatAm inclusion 
1.18 
9 Jul 2025 
• 
Status option inclusion 
1.17 
5 Jun 2025 
• 
Country list update 
1.16 
7 May 2025 
• 
Africa inclusion 
1.15 
31 Jan 2025 
• 
Middle East inclusion 
• 
Updated country list 
• 
Updated appendix 
1.14 
6 Dec 2024 
• 
Corrected accepted country codes table 
1.13 
27 Sep 2024 
• 
Fixed incorrect single asset API endpoint path 
1.12 
24 Sep 2024 
• 
Updated Data Dictionary and Template 
1.11 
14 Aug 2024 
• 
Added SSPs 
1.10 
15 Apr 2024 
• 
Added appendix to specify acceptable country names 
1.9 
26 Feb 2024 
• 
Added detail for single-asset API call 
• 
Updated formatting 
• 
Added a version control table 
 
CONTENTS 
CONTENTS ............................................................................................................... 2 
BACKGROUND & FUNCTIONALITY ........................................................................... 3 
EXAMPLE: SINGLE-ASSET API CALL ......................................................................... 4 
EXAMPLE: CSV API CALL .......................................................................................... 9 
Appendices ............................................................................................................. 12 
 
 


---

## Page 3

 
 
3 
Highly Confidential 
Not for further distribution 
BACKGROUND & FUNCTIONALITY 
How the API works  
The Climate X Spectra platform features an external REST API, the access of which requires a 
configured Spectra subscription and a machine with an internet connection. The IP address range 
of this connection should have already been provided to Climate X by your organisation to ensure 
secure access to the Spectra platform. 
The API can be accessed programmatically from any command line or programming language 
that can make HTTP calls.  
There are 2 ways in which you can use the API: 
Option 1: Single-Asset Search 
This option allows you to send a single API call, with details of the desired location, asset 
characteristics, and climate scenario, among other things, in the message body (subject to the 
user’s region and scenario access permissions). Users will then get a comprehensive output, 
including hazard and loss data, from the Spectra platform in a single message. 
Option 2: CSV Upload 
This option allows the user to upload any number of assets (in the regions you have subscription 
access to), in CSV format, using our template structure. Users can check the status of the upload 
as it happens. Statuses include ‘INACTIVE’, ‘TODO’, ‘IN-PROGRESS’, ‘COMPLETED’ and ‘FAILED’. 
Accepted naming conventions for each country are outlined in Appendix 3. 
Your Credentials 
API access information will be provided from Climate X’s support team to you in the following 
structure. We’ll use the details contained in this table to populate the relevant fields of our 
example API calls (using the curl command-line tool) below. 
 
User Name / E-mail 
API Key 
Organisation Name 
User_1@company-x.com 
AR07Wzv8xuaBpBcXcTqnDbQVnMdK
JsEz 
Company-X 
User_2@company-x.com 
52aLoeNxSB0gG8baQfdtCA9kTP69U
q27 
User_3@company-x.com 
aP5Ag8RLvaKdUMOcZHpIUBX4fnP95
cOq 
User_4@company-x.com 
bzKMlrhDn9Dlhs8AZcnbqVDTFtBVo3v
1 
User_5@company-x.com 
8cXQkrkdw623cM3pSJME40QXRo0D
Rknh 
 
 


---

## Page 4

 
 
4 
Highly Confidential 
Not for further distribution 
EXAMPLE: SINGLE-ASSET API CALL 
The following is an example single-asset API call. As stated above, there is only one input message 
needed for this method. The user specifies the asset details in the input message and receives a 
comprehensive output also returned in a single message. Note: the detail returned in the output 
messages depends on user permissions. EPCs are only available in the UK, Ireland, and Italy. 
 
Input - template: 
 
curl -X 'POST' \ 
  'https://apis.climate-x.com/main/assets/v2/single-asset' \ 
  -H 'accept: application/json' \ 
  -H 'Content-Type: application/json' \ 
  -H 'x-api-key: user-1-api-key' \ 
  -d '{ 
    "data": { 
        "country_id": "USA", 
        "city": "Washington DC", 
        "street_name": "Pennsylvania Avenue NW", 
        "postcode": "DC 20500", 
        "building_number": "1600 ", 
        "property_identifier": "", 
 
        "age_category": "pre-1919", 
        "asset_use": "residential", 
        "asset_type": "SINGLE_RES", 
        "building_replacement_cost": 10000000, 
        "structure_category": "C_4", 
        "premise_area": 10000, 
        "floor_count": 2 
    }, 
    "options": { 
        "year": custom-export-parameter, 
        "scenario": custom-export-parameter, 
        "defended": custom-export-parameter 
    }' 
 
Input - example: 
 
curl -X 'POST' \ 
  'https://apis.climate-x.com/main/assets/v2/single-asset' \ 
  -H 'accept: application/json' \ 
  -H 'Content-Type: application/json'\ 
  -H 'x-api-key: AR07Wzv8xuaBpBcXcTqnDbQVnMdKJsEz'\ 
  -d '{ 
    "data": { 
        "country_id": "GBR", 
        "city": "London", 
        "street_name": " Great Winchester Street", 
        "postcode": " EC2N 2JA", 
        "building_number": "21", 
        "age_category": "1945-1964", 
        "asset_use": "commercial", 
        "asset_type": "OFFICE", 
        "building_replacement_cost": 100000, 
        "structure_category": "C_4", 
        "premise_area": 250, 


---

## Page 5

 
 
5 
Highly Confidential 
Not for further distribution 
        "floor_count": 2 
    }, 
    "options": { 
        "year": 2050, 
        "scenario": "ssp585", 
        "defended": true 
    }' 
 
Output - example: 
 
    "asset": { 
        "asset_id": "60910860", 
        "street": "Great Winchester Street", 
        "city": "London", 
        "postcode": "EC2N 2JA", 
        "building_number": "21", 
        "building_name": null, 
        "region": "London", 
        "country": "United Kingdom", 
        "latitude": 51.5161117, 
        "longitude": -0.0855275, 
        "property_identifier": null 
    }, 
    "conditions": { 
        "year": 2050, 
        "scenario": "ssp585", 
        "defended": true 
    }, 
    "hazards": { 
        "river_flood": { 
            "score": 1.0, 
            "severity_value": 0.0, 
            "severity_min": null, 
            "severity_max": null, 
            "likelihood": null, 
            "climate_reliability": 0.9353354, 
            "hazard_reliability": 0.66, 
            "severity_metric": "maximum depth (m)" 
        }, 
        "surface_flood": { 
            "score": 1.0, 
            "severity_value": 0.0, 
            "severity_min": null, 
            "severity_max": null, 
            "likelihood": null, 
            "climate_reliability": 0.9353354, 
            "hazard_reliability": null, 
            "severity_metric": "maximum depth (m)" 
        }, 
        "coastal_flood": { 
            "score": 1.0, 
            "severity_value": 0.0, 
            "severity_min": null, 


---

## Page 6

 
 
6 
Highly Confidential 
Not for further distribution 
            "severity_max": null, 
            "likelihood": 0.0, 
            "climate_reliability": 0.65, 
            "hazard_reliability": 0.65, 
            "severity_metric": "maximum depth (m)" 
        }, 
        "wildfires": { 
            "score": 1.0, 
            "severity_value": 6.464035511016846, 
            "severity_min": 0.0, 
            "severity_max": 19.669172287, 
            "likelihood": 0.0, 
            "climate_reliability": 0.9353354, 
            "hazard_reliability": 0.75, 
            "severity_metric": "No of fire weather days" 
        }, 
        "storms": { 
            "score": 5.0, 
            "severity_value": 157.5, 
            "severity_min": null, 
            "severity_max": null, 
            "likelihood": null, 
            "climate_reliability": 0.83, 
            "hazard_reliability": 0.83, 
            "severity_metric": "3s gust wind speed (km/h)" 
        }, 
        "tropical_cyclones": { 
            "score": 1.0, 
            "severity_value": 0.0, 
            "severity_min": null, 
            "severity_max": null, 
            "likelihood": null, 
            "climate_reliability": null, 
            "hazard_reliability": null, 
            "severity_metric": "3s gust wind speed (km/h)" 
        }, 
        "subsidence": { 
            "score": 3.0, 
            "severity_value": 1.2686457633972168, 
            "severity_min": 1.1499999762, 
            "severity_max": 1.2999999523, 
            "likelihood": null, 
            "climate_reliability": 0.9361328, 
            "hazard_reliability": 0.75, 
            "severity_metric": "indicator [0,2]" 
        }, 
        "extreme_heat_days": { 
            "score": 4.0, 
            "severity_value": 15.858333587646484, 
            "severity_min": 6.0, 
            "severity_max": 32.0999984741, 
            "likelihood": null, 


---

## Page 7

 
 
7 
Highly Confidential 
Not for further distribution 
            "climate_reliability": 0.8968716, 
            "hazard_reliability": 0.8968716, 
            "severity_metric": "No of heatwave days" 
        }, 
        "droughts": { 
            "score": 3.0, 
            "severity_value": 4.659953594207764, 
            "severity_min": 1.1129157543, 
            "severity_max": 10.3556098938, 
            "likelihood": 0.1703445464, 
            "climate_reliability": 0.65, 
            "hazard_reliability": 0.65, 
            "severity_metric": "Magnitude" 
        }, 
        "storm_surge": { 
            "score": null, 
            "severity_value": null, 
            "severity_min": null, 
            "severity_max": null, 
            "likelihood": null, 
            "climate_reliability": null, 
            "hazard_reliability": null, 
            "severity_metric": null 
        } 
    }, 
    "losses": { 
        "age_category": "1945-1964", 
        "age_category_flag": "U", 
        "structure_category": "C_4", 
        "building_replacement_cost": 129770.6, 
        "gross_premise_area_flag": "U", 
        "gross_premise_area": 500.0, 
        "river_flood_loss": 0.0, 
        "surface_flood_loss": 0.0, 
        "coastal_flood_loss": 0.0, 
        "landslide_loss": 0.0, 
        "subsidence_loss": 363.35768, 
        "wildfires_loss": 0.0, 
        "storms_loss": 205.03754800000002, 
        "tropical_cyclones_loss": 0.0, 
        "storm_surge_loss": null, 
        "physical_loss": 568.395228, 
        "physical_loss_per_unit_or_flat": 568.395228, 
        "physical_loss_percentage": 0.00438, 
        "num_addresses": 1.0, 
        "num_basement_floors": 0.0, 
        "actual_epc": 2.0, 
        "potential_epc": 2.0, 
        "epc_flag": "A", 
        "retrofit_a": 119.315255, 
        "retrofit_b": 0.0, 
        "retrofit_c": 0.0, 


---

## Page 8

 
 
8 
Highly Confidential 
Not for further distribution 
        "retro_a_flag": "modelled", 
        "retro_b_flag": "modelled", 
        "retro_c_flag": "modelled", 
        "current_co2_emissions": 6.8464029172, 
        "potential_co2_emissions": 6.8464029172, 
        "co2_emissions_flag": "weak_filled", 
        "current_energy_consumption": 39351.230025413, 
        "potential_energy_consumption": 39351.230025413, 
        "energy_consumption_flag": "weak_filled", 
        "asset_use": "commercial", 
        "asset_type": "OFFICE" 
    } 
 
 
The following options are available for the single-asset API (options in bold are used as a default 
if the user does not specify an option). EPCs are only available in the UK, Ireland, and Italy.  
 
In addition, building characteristics (which are usually modelled, or taken from Climate X’s 
buildings database) can be overwritten by a user. The full list of available overrides is available in 
Appendix 1.
 
Variable 
Description 
Options 
year 
Spectra modelling 
output year. 
2020, 2025, 2030, 2035, 2040, 2045, 
2050, 2060, 2070, 2080, 2090, 2100 
scenario 
Climate scenario to be 
used for modelling 
“ssp126”, “ssp245”, “ssp370”, 
“ssp585” 
defended 
Toggle flood defences 
true, false  


---

## Page 9

 
 
9 
Highly Confidential 
Not for further distribution 
EXAMPLE: CSV API CALL 
The following is an example csv-API call for “User-1” (User_1@company-x.com) using the curl 
command-line tool. The call is structure in 4 steps, these allow you to (1) upload a csv, and (2) 
check the status of the upload, before (3) setting parameters and exporting a csv which can be 
(4) downloaded from AWS s3. 
 
Data Upload Structure examples 
Appendix 2 shows the latest CSV data template structure the Spectra API will expect you to 
upload before it can accurately process your records. This template can be downloaded from 
the Spectra platform. Note: all columns from ID to Premise Identifier must be included, even 
if blank. 
Once uploaded, users can specify the desired climate scenarios (subject to permissions) they 
wish to apply to their portfolio. The API will process the request and return the relevant hazards 
and losses via secure download links. Each returned CSV file is limited to 6GB in size, and larger 
files will be available in clearly labelled parts. 
Step 1: Upload your CSV project to Spectra 
 
Input - template: 
 
curl -X 'POST' \ 
  'https://apis.climate-x.com/main/external-upload-csv/' \ 
  -H 'accept: application/json' \ 
  -H 'x-api-key: user-1-api-key' \ 
  -F 'file=@"/absolute-system-path-to-csv-file"' 
 
Input - example: 
 
curl -X 'POST' \ 
  'https://apis.climate-x.com/main/external-upload-csv/' \ 
  -H 'accept: application/json' \ 
  -H 'x-api-key: AR07Wzv8xuaBpBcXcTqnDbQVnMdKJsEz' \ 
  -F  
'file=@"/Users/johnsmith/Desktop/external_api_testing/united_kingdom_addresses.
csv"' 
 
Output - example: 
 
"project_id": 23, 
"job_id": 20 
 
 
Step 2: Check processing status of Project 
 
Input - template: 
 
curl -X 'GET' \ 
  'https://apis.climate-x.com/main/import-assets/<job_id>' \ 
  -H 'x-api-key: user-1-api-key' 
 
Input - example: 
 
curl -X 'GET' \ 
  'https://apis.climate-x.com/main/import-assets/20' \ 
  -H 'x-api-key: AR07Wzv8xuaBpBcXcTqnDbQVnMdKJsEz' 
 


---

## Page 10

 
 
10 
Highly Confidential 
Not for further distribution 
Output - example: 
 
"job_id": 20, 
"status": "COMPLETED", 
"progress": 100 
 
Statuses include ‘INACTIVE’, ‘TODO’, ‘IN-PROGRESS’, ‘COMPLETED’ and ‘FAILED’. 
Step 3: Export CSV output data using select parameters 
 
Input - template: 
 
curl -X 'POST' \ 
  'https://apis.climate-x.com/main/export-csv/' \ 
  -H 'accept: application/json' \ 
  -H 'x-api-key: user-1-api-key' \ 
  -H 'Content-Type: application/json' \ 
  -d '{ 
  "project_id": project_id 
  "defended": custom-export-parameter, 
  "scenario": custom-export-parameter, 
  "one_in_x": [return-period-years] 
}' 
 
Input - example: 
 
curl -X 'POST' \ 
  'https://apis.climate-x.com/main/export-csv/' \ 
  -H 'accept: application/json' \ 
  -H 'x-api-key: AR07Wzv8xuaBpBcXcTqnDbQVnMdKJsEz' \ 
  -H 'Content-Type: application/json' \ 
  -d '{ 
  "project_id": 23, 
  "defended": true, 
  "scenario": "ssp585", 
  "one_in_x": [50, 200] 
}' 
 
Output - example: 
 
"message": "Job started", 
"export_job_id": 3 
 
 
The following export parameters are set: 
 
However, some parameters can be customised based on the desired scenario/conditions 
(options in bold are used as a default if the user does not specify an option). EPCs are only 
available in the UK, Ireland, and Italy. 
 
If the one_in_x variable is not defined, a standard CSV containing average annual losses and 
risks for all hazards will be exported. If one or more one_in_x (return period) values are provided, 
a return period CSV will be exported containing only the return period hazards and their 
corresponding return period–specific risks and losses. 
year 
2020, 2025, 2030, 2035, 2040, 2045, 2050, 2060, 2070, 2080, 2090, 2100 
one_in_x (if not 
specified) 
100 


---

## Page 11

 
 
11 
Highly Confidential 
Not for further distribution 
 
 
Step 4: Querying the export job ID from the previous step 
 
Input - template: 
 
curl -X 'GET' \  
  'https://apis.climate-x.com/main/export-csv/<export_job_id>' \  
  -H 'accept: application/json' \  
  -H 'x-api-key: user-1-api-key' 
 
Input - example: 
 
curl -X 'GET' \  
  'https://apis.climate-x.com/main/export-csv/3' \  
  -H 'accept: application/json' \  
  -H 'x-api-key: AR07Wzv8xuaBpBcXcTqnDbQVnMdKJsEz' 
 
Output - example: 
 
"progress": 100.0,  
"status": "COMPLETED",  
"url": "https://dev-services-bucket-application-
storage.s3.amazonaws.com/export_csv/<rest of url removed>"  
 
 
 
Variable 
Description 
Options 
scenario 
Climate scenario to be 
used for modelling 
“ssp126”, “ssp245”, “ssp370”, 
“ssp585” 
defended 
Toggle flood defences 
true, false  
one_in_x (optional) 
Export hazard risk and 
losses for the specified 
return periods 
10, 50, 100, 200, 500 


---

## Page 12

 
 
12 
Highly Confidential 
Not for further distribution 
Appendices 
Appendix 1 – Single-asset API asset overrides 
 
The following building characteristics can be overridden when using the single-asset API. If not 
overridden, the API will use the information held in Climate X’s buildings database, or use 
regional default values: 
 
Variable 
Description 
Options 
age_category 
Period in 
which the 
asset was 
built 
“pre-1919”, “1919-1944”, “1945-1964”, 
“1965-1974”, “1975-1985”, “post-1985” 
asset_use 
High level 
use 
category of 
building 
“commercial”, “residential”, “energy”, 
“agriculture”, “industrial”, 
“infrastructure”, “mixed_use” 
asset_type 
More 
granular 
specification 
of building 
use. 
 
Must be 
used in 
conjunction 
with a 
suitable 
asset_use 
category 
If asset_use = “commercial”: 
“DATA_CENTER”, “EDUCATION”, 
“HEALTHCARE”, “HIGH_ST”, HOTEL”, 
“OFFICE”, “PUBLIC”, “RELIGION”, 
“RESTAURANT”, “SHOPPING”, 
“RECREATIONAL”, “PARKING”, 
“OTHER” 
 
If asset_use = “residential”: 
“SINGLE_RES”, “MULTI_RES” 
 
If asset_use = “agriculture”: 
“AGRICULTURE” 
 
If asset_use = “industrial”: 
“INDUSTRIAL”, “WAREHOUSE”, 
“ALUMINIUM_PRODUCTION_PLANT”, 
“BAUXITE_MINE" 𝟏, 
“CEMENT_PRODUCTION_PLANT”, 
“CHEMICALS_PRODUCTION_PLANT”, 
“COPPER_MINE” 𝟏, “IRON_MINE” 𝟏, 
“MANUFACTURING”, 
“PULP_PAPER_PRODUCTION_PLANT”, 
“SEWAGE_TREATMENT_PLANT” 𝟏, 
“STEEL_PRODUCTION_PLANT”, 
“WASTE_INCINERATION_PLANT”, 
“WATER_UTILITY” 
 
 
 


---

## Page 13

 
 
13 
Highly Confidential 
Not for further distribution 
 
 𝟏 Losses Not Calculated 
 
If asset_use = “energy”: 
“BATTERY_STORAGE_PLANT”, 
“BIOENERGY_POWER_PLANT”, 
“COAL_MINE” 𝟏, 
“COAL_POWER_PLANT”, 
“COAL_TERMINAL” 𝟏, 
“GAS_POWER_PLANT”, “GAS_UTILITY”, 
“GEOTHERMAL_POWER_PLANT”, 
“HYDROPOWER” 𝟏, 
“LIQUID_NATURAL_GAS”, 
“NUCLEAR_POWER_PLANT”, 
“OIL_GAS_EXTRACTION” 𝟏, 
“OIL_GAS_POWER_PLANT”, 
“OIL_GAS_REFINERY”, “OIL_UTILITY”, 
“ONSHORE_WIND” 𝟏, 
“POWER_UTILITY”, “SOLAR” 𝟏, 
“SUBSTATION” 
 
If asset_use = “infrastructure”: 
“TRANSPORT”, “AIRPORT”, 
“SHIPPING_PORT” 𝟏, “TRAIN_STATION” 
 
If asset_use = “mixed_use”:  
Any of the above 
structure_category 
Signifies the 
strength of 
the asset.  
“C_2”, (weakest) 
“C_3”, 
“C_4”, 
“C_5” (strongest) 
building_replacement_cost 
Total cost to 
replace the 
building 
[User-defined integer] 
premise_area 
Footprint of 
building 
[User-defined integer] 
floor_count 
Number of 
floors 
[User-defined integer] 


---

## Page 14

 
 
14 
Highly Confidential 
Not for further distribution 
Appendix 2 – Spectra csv upload template 
 
 
 
Appendix 3 – Accepted country codes 
Region 
Country 
Accepted entries 
Africa 
Egypt 
['Egypt', 'EG', 'EGY'] 
Africa 
Ethiopia 
['Ethiopia', 'ET', 'ETH'] 
Africa 
Ghana 
['Ghana', 'GH', 'GHA'] 
Africa 
Kenya 
['Kenya', 'KE', 'KEN'] 
Africa 
Nigeria 
['Nigeria', 'NG', 'NGA'] 
Africa 
South Africa 
['South Africa', 'ZA', 'ZAF'] 
APAC 
Australia 
['Australia', 'AU', 'AUS'] 
APAC 
Bangladesh 
['Bangladesh', 'BD', 'BGD'] 
APAC 
Bhutan 
['Bhutan', 'BT', 'BTN'] 
APAC 
Brunei 
['Brunei Darussalam', 'Brunei', 'BN', 'BRN'] 
APAC 
Cambodia 
['Cambodia', 'KH', 'KHM'] 
APAC 
China 
['China', 'CN', 'CHN'] 
APAC 
Hong Kong 
['Hong Kong', 'China - Hong Kong', 'HK', 'HKG'] 
APAC 
India 
['India', 'IN', 'IND'] 
APAC 
Indonesia 
['Indonesia', 'ID', 'IDN'] 
APAC 
Japan 
['Japan', 'JP', 'JPN'] 
APAC 
Laos 
['Lao PDR', 'Laos', 'Lao', 'LA', 'LAO'] 
APAC 
Malaysia 
['Malaysia', 'MY', 'MYS'] 
APAC 
Mongolia 
['Mongolia', 'MN', 'MNG'] 
APAC 
Myanmar 
['Myanmar', 'Myanmar/Burma', 
'Burma/Myanmar', 'Burma', 'MM', 'MMR'] 
APAC 
Nepal 
['Nepal', 'NP', 'NPL'] 
APAC 
New Zealand 
['New Zealand', 'NewZealand', 'NZ', 'NZL'] 
APAC 
Pakistan 
['Pakistan', 'PK', 'PAK'] 
APAC 
Papua New Guinea 
['Papua New Guinea', 'PG', 'PNG'] 
APAC 
Philippines 
['Philippines', 'PH', 'PHL'] 
APAC 
Singapore 
['Singapore', 'SG', 'SGP'] 
APAC 
South Korea 
['South Korea', 'S Korea', 'Korea', 'KR', 'KOR'] 
APAC 
Sri Lanka 
['Sri Lanka', 'LK', 'LKA'] 


---

## Page 15

 
 
15 
Highly Confidential 
Not for further distribution 
APAC 
Taiwan 
['Taiwan', 'TW', 'TWN'] 
APAC 
Thailand 
['Thailand', 'TH', 'THA'] 
APAC 
Vietnam 
['Viet Nam', 'VietNam', 'Vietnam', 'VN', 'VNM'] 
Europe 
Albania 
['Albania', 'AL', 'ALB'] 
Europe 
Andorra 
['Andorra', 'AD', 'AND'] 
Europe 
Austria 
['Austria', 'AT', 'AUT'] 
Europe 
Belarus 
['Belarus', 'BY', 'BLR'] 
Europe 
Belgium 
['Belgium', 'BE', 'BEL'] 
Europe 
Bosnia and Herzegovina 
['Bosnia and Herzegovina', 'BA', 'BIH'] 
Europe 
Bulgaria 
['Bulgaria', 'BG', 'BGR'] 
Europe 
Croatia 
['Croatia', 'HR', 'HRV'] 
Europe 
Czech Republic 
['Czech Republic', 'CZ', 'Czechia', 'CZE'] 
Europe 
Denmark 
['Denmark', 'DK', 'DNK'] 
Europe 
Estonia 
['Estonia', 'EE', 'EST'] 
Europe 
Faroe Islands 
['Faroe Islands', 'FO', 'FRO'] 
Europe 
Finland 
['Finland', 'FI', 'FIN'] 
Europe 
France 
['France', 'FR', 'FRA'] 
Europe 
Germany 
['Germany', 'DE', 'DEU'] 
Europe 
Greece 
['Greece', 'GR', 'GRC'] 
Europe 
Guernsey 
['Guernsey', 'GG', 'GGY'] 
Europe 
Hungary 
['Hungary', 'HU', 'HUN'] 
Europe 
Iceland 
['Iceland', 'IS', 'ISL'] 
Europe 
Ireland 
['Ireland', 'IE', 'IRL'] 
Europe 
Isle of Man 
['Isle of Man', 'IM', 'IMN'] 
Europe 
Italy 
['Italy', 'IT', 'ITA'] 
Europe 
Jersey 
['Jersey', 'JE', 'JEY'] 
Europe 
Kosovo 
['Kosovo', 'XK', 'XXK'] 
Europe 
Latvia 
['Latvia', 'LV', 'LVA'] 
Europe 
Liechtenstein 
['Liechtenstein', 'LI', 'LIE'] 
Europe 
Lithuania 
['Lithuania', 'LT', 'LTU'] 
Europe 
Luxembourg 
['Luxembourg', 'LU', 'LUX'] 
Europe 
Malta 
['Malta', 'MT', 'MLT'] 
Europe 
Moldova 
['Moldova', 'MD', 'MDA'] 
Europe 
Monaco 
['Monaco', 'MC', 'MCO'] 
Europe 
Montenegro 
['Montenegro', 'ME', 'MNE'] 
Europe 
Netherlands 
['Netherlands', 'NL', 'NLD'] 
Europe 
North Macedonia 
['Macedonia', 'North Macedonia', 
'North_Macedonia', 'MK', 'MKD'] 
Europe 
Norway 
['Norway', 'NO', 'NOR'] 


---

## Page 16

 
 
16 
Highly Confidential 
Not for further distribution 
 
 
 
Europe 
Poland 
['Poland', 'PL', 'POL'] 
Europe 
Portugal 
['Portugal', 'PT', 'PRT'] 
Europe 
Romania 
['Romania', 'RO', 'ROU'] 
Europe 
San Marino 
['San Marino', 'SM', 'SMR'] 
Europe 
Serbia 
['Serbia', 'RS', 'SRB'] 
Europe 
Slovakia 
['Slovakia', 'SK', 'SVK'] 
Europe 
Slovenia 
['Slovenia', 'SI', 'SVN'] 
Europe 
Spain 
['Spain', 'ES', 'ESP'] 
Europe 
Sweden 
['Sweden', 'SE', 'SWE'] 
Europe 
Switzerland 
['Switzerland', 'CH', 'CHE'] 
Europe 
United Kingdom 
[ 'Great Britain', 'GB', 'United Kingdom', 'UK', 
'England', 'Scotland', 'Wales', 'Northern Ireland', 
'GBR'] 
Europe 
Vatican City 
['Vatican City', 'Vatican', 'VA', 'VAT'] 
North America Canada 
['Canada', 'CA', 'CAN'] 
North America United States 
['United States of America', 'United States', 'US', 
'USA'] 
Middle East 
Bahrain 
['Bahrain', 'BH', 'BHR'] 
Middle East 
Israel 
['Israel', 'IL', 'ISR'] 
Middle East 
Jordan 
['Jordan', 'JO', 'JOR'] 
Middle East 
Kuwait 
['Kuwait', 'KW', 'KWT'] 
Middle East 
Oman 
['Oman', 'OM', 'OMN'] 
Middle East 
Qatar 
['Qatar', 'QA', 'QAT'] 
Middle East 
Saudi Arabia 
['Saudi Arabia', 'SA', 'SAU'] 
Middle East 
United Arab Emirates 
['United Arab Emirates', 'AE', 'ARE'] 
Middle East 
Yemen 
['Yemen', 'YE', 'YEM'] 
Latin America Bolivia 
['Bolivia', 'BO', 'BOL'] 
Latin America Brazil 
['Brazil', 'BR', 'BRA'] 
Latin America Colombia 
['Colombia', 'CO', 'COL'] 
Latin America Costa Rica 
['Costa Rica', 'CR', 'CRI'] 
Latin America Ecuador 
['Ecuador', 'EC', 'ECU'] 
Latin America El Salvador 
['El Salvador', 'SV', 'SLV'] 
Latin America Guatemala 
['Guatemala', 'GT', 'GTM'] 
Latin America Mexico 
['Mexico', 'MX', 'MEX'] 
Latin America Nicaragua 
['Nicaragua', 'NI', 'NIC'] 
Latin America Panama 
['Panama', 'PA', 'PAN'] 
Latin America Peru 
['Peru', 'PE', 'PER'] 
Latin America Venezuela 
['Venezuela', 'VE', 'VEN'] 
Highly Confidential 
Not for further distribution 


---

