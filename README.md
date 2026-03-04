# Climate X Spectra API - Portfolio Risk Analysis

Solutions Engineer Challenge for Climate X

## Project Structure

```
climate-x/
├── src/
│   ├── api/
│   │   └── climate_client.py    # API client wrapper
│   ├── models/
│   │   └── schemas.py            # Data models and schemas
│   ├── services/
│   │   ├── analyzer.py           # Risk analysis logic
│   │   └── reporter.py           # Report generation
│   └── utils/
│       ├── logger.py             # Logging configuration
│       └── validators.py         # Input validation
├── config/
│   └── settings.py               # Configuration management
├── data/
│   └── portfolio_assets.py       # Asset data definitions
├── output/                       # Generated reports and data
├── task-context/                 # Challenge documentation
├── main.py                       # Application entry point
└── README.md
```

## Features

- **Production-grade architecture** with separation of concerns
- **Comprehensive logging** with timestamps and detailed request tracking
- **Error handling** with retry logic and graceful degradation
- **Data validation** ensuring API compliance
- **Modular design** for easy testing and maintenance
- **Performance optimized** with configurable rate limiting

## Installation

```bash
# Run with uv (recommended)
uv run --with requests main.py

# Or install dependencies manually
pip install requests
python main.py
```

## API Configuration

API Key: `jdy9bAWZON50rODZqyUpc6Z6J3CGtNry`  
Endpoint: `https://apis.climate-x.com/main/assets/v2/single-asset`  
Documentation Reference: Climate_X_Spectra_API_v2.0.md

## Output

- `output/climate_risk_report.md` - Executive summary (1-2 pages)
- `output/api_responses.json` - Raw API data for reference

## Analysis Parameters

- **Year**: 2050
- **Scenario**: SSP5-8.5 (High emissions)
- **Defended**: True (flood defenses enabled)
- **Country**: GBR (United Kingdom)

## Success Metrics

- 8/10 assets successfully analyzed (80% success rate)
- Average API response time: ~13-15 seconds per asset
- Total analysis time: ~2.2 minutes
