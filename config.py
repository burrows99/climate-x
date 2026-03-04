"""Configuration - Climate_X_Spectra_API_v2.0.md"""

# Page 3-4: API credentials and endpoint
API_KEY = "jdy9bAWZON50rODZqyUpc6Z6J3CGtNry"
API_URL = "https://apis.climate-x.com/main/assets/v2/single-asset"
TIMEOUT = 30

# Page 8: Analysis options (year, scenario, defended)
YEAR = 2050
SCENARIO = "ssp585"  # High emissions pathway
DEFENDED = True  # Include flood defenses
COUNTRY_ID = "GBR"  # Page 16: UK code

# Page 12-13 Appendix 1: Building defaults
AGE_CATEGORY = "1945-1964"
ASSET_USE = "commercial"
ASSET_TYPE = "OFFICE"
STRUCTURE_CATEGORY = "C_4"
REPLACEMENT_COST = 500000
PREMISE_AREA = 500
FLOOR_COUNT = 2

# Analysis threshold (Page 5-6: scores 1.0-5.0)
HIGH_RISK_THRESHOLD = 4.0

# Output paths
REPORT_FILE = "output/climate_risk_report.md"
RAW_DATA_FILE = "output/api_responses.json"
