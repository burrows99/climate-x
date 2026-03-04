# Climate X Spectra API - Response Structure Analysis

## Overview
Analysis of actual API responses to verify correct usage and identify any inconsistencies.

## Response Structure

### Top-Level Keys
All successful responses contain these 4 keys:
```json
{
  "asset": {},
  "hazards": {},
  "losses": {},
  "conditions": {}
}
```
✅ **Status:** Consistent across all 8/8 successful responses

---

## 1. Asset Data

### Available Fields
```json
{
  "asset_id": "78219984",
  "street": null,
  "city": null,              // ⚠️ Often null for coordinate-only inputs
  "postcode": null,          // ⚠️ Often null for coordinate-only inputs
  "building_number": null,
  "building_name": null,
  "region": "London",        // ✅ Always present
  "country": "United Kingdom",
  "latitude": 51.5074,       // ✅ Always present
  "longitude": -0.1278,      // ✅ Always present
  "property_identifier": null,
  "name": null               // ⚠️ ALWAYS null - API doesn't return asset names
}
```

### Our Handling
**Location String Priority (analyzer.py):**
1. City + Postcode (e.g., "Leeds, LS1 2DE") - most specific
2. Postcode only
3. City only
4. Region + Coordinates (e.g., "London (51.5074, -0.1278)") - for coordinate-only assets
5. Coordinates only
6. "Unspecified location" (fallback)

✅ **Status:** Correctly handles all null city/postcode cases

**Asset Name:**
- API returns `name: null` for all requests
- We pass `asset_name` from our input data (portfolio_data.py)
- This is intentional - we control naming

---

## 2. Hazards Data

### Structure
```json
{
  "river_flood": {
    "score": 1.0,             // ✅ Present when hazard applies
    "severity_value": 0.0,
    "severity_min": null,
    "severity_max": null,
    "likelihood": null,
    "climate_reliability": null,
    "hazard_reliability": null,
    "severity_metric": "maximum depth (m)"
  },
  "tropical_cyclones": {
    "score": null             // ⚠️ Can be null for non-applicable hazards
  },
  "storm_surge": {
    "score": null             // ⚠️ Can be null for non-applicable hazards
  }
}
```

### Hazard Types (10 total)
1. `river_flood`
2. `surface_flood`
3. `coastal_flood`
4. `droughts`
5. `extreme_heat_days`
6. `storms`
7. `subsidence`
8. `wildfires`
9. `tropical_cyclones` - ⚠️ Often null (not applicable to UK)
10. `storm_surge` - ⚠️ Often null

### Our Handling (analyzer.py:19-22)
```python
for htype, hdata in hazards_data.items():
    if hdata and isinstance(hdata, dict):
        score = hdata.get("score")
        if isinstance(score, (int, float)):  # ✅ Filters out None scores
            hazards.append(Hazard(type=htype, score=score))
```

✅ **Status:** Correctly filters out null scores

### Issues Found in Responses
- Response 1: `tropical_cyclones.score = None`, `storm_surge.score = None`
- Response 2: `coastal_flood.score = None`, `tropical_cyclones.score = None`, `storm_surge.score = None`

**Impact:** None - our code safely ignores these via type checking

---

## 3. Losses Data

### Structure (38 fields total)
```json
{
  // Building metadata
  "age_category": "1945-1964",
  "structure_category": "C_4",
  "asset_use": "commercial",
  "asset_type": "OFFICE",
  "total_structure_cost": 500000.0,
  "building_replacement_cost": 500000.0,
  "gross_premise_area": 1000.0,
  "num_addresses": 1.0,
  "num_basement_floors": 0.0,
  
  // Loss by hazard type
  "river_flood_loss": 0.0,
  "surface_flood_loss": 0.0,
  "coastal_flood_loss": 0.0,
  "landslide_loss": 0.0,
  "subsidence_loss": 648.0,
  "wildfires_loss": 0.0,
  "storms_loss": 245.0,
  "tropical_cyclones_loss": 0.0,
  "storm_surge_loss": null,        // ⚠️ ALWAYS null (8/8 responses)
  
  // Total loss
  "physical_loss": 893.0,          // ✅ ALWAYS present - this is what we use
  "physical_loss_per_unit_or_flat": 893.0,
  "physical_loss_percentage": 0.001786,
  
  // Energy efficiency
  "actual_epc": 3.0,
  "potential_epc": 2.0,
  "epc_flag": "D",
  
  // Retrofit costs
  "retrofit_a": 480.97,
  "retrofit_b": 245.89,
  "retrofit_c": 0.0,
  "retro_a_flag": "D",
  "retro_b_flag": "D",
  "retro_c_flag": "D",
  
  // Emissions
  "current_co2_emissions": 32.17,
  "potential_co2_emissions": 15.55,
  "co2_emissions_flag": "D",
  
  // Energy consumption
  "current_energy_consumption": 183288.59,
  "potential_energy_consumption": 86891.64,
  "energy_consumption_flag": "D"
}
```

### Our Usage
**Primary field (analyzer.py:27):**
```python
annual_loss = losses.get("physical_loss", 0.0)  # ✅ Correct field name
```

**Loss breakdown (reporter.py:30-39):**
```python
for key, value in losses.items():
    if key.endswith("_loss") and key != "physical_loss" and value:  # ✅ Filters None
        hazard_name = key.replace("_loss", "").replace("_", " ").title()
        hazard_losses[hazard_name] = hazard_losses.get(hazard_name, 0) + (value or 0)
```

✅ **Status:** 
- Correctly uses `physical_loss` (not `expected_annual_loss_total`)
- Correctly filters out `storm_surge_loss: null`
- Excludes `physical_loss` from breakdown to avoid double-counting

### Historical Bug (Fixed)
❌ **Previous:** Used `expected_annual_loss_total` → always returned £0
✅ **Current:** Uses `physical_loss` → returns actual values

---

## 4. Data Quality Summary

### Location Data Quality
| Asset | City | Postcode | Region | Coordinates | Quality Score |
|-------|------|----------|--------|-------------|---------------|
| 1 | None | None | London | Yes | 3/5 |
| 2 | Birmingham | B2 4QA | West Midlands | Yes | 5/5 |
| 3 | None | None | Scotland | Yes | 3/5 |
| 4 | None | None | South West | Yes | 3/5 |
| 5 | None | None | North West | Yes | 3/5 |
| 6 | Leeds | LS1 2DE | Yorkshire | Yes | 5/5 |
| 7 | None | None | London | Yes | 3/5 |
| 8 | Bristol | BS1 5NG | South West | Yes | 5/5 |

**Average Quality:** 3.75/5

✅ All assets have enough data for meaningful location identification

---

## 5. Unused API Data (Potential Enhancements)

### Energy Efficiency
- `actual_epc`: Current EPC rating (1-7 scale)
- `potential_epc`: Potential EPC after improvements
- `retrofit_a`, `retrofit_b`, `retrofit_c`: Retrofit cost estimates

### Environmental Impact
- `current_co2_emissions`: CO2 emissions (kg)
- `potential_co2_emissions`: After improvements
- `current_energy_consumption`: kWh/year
- `potential_energy_consumption`: After improvements

### Flags
All flags indicate data source reliability:
- `U`: User provided
- `D`: Derived/estimated
- `M`: Modelled

**Potential use cases:**
1. ESG reporting (CO2 emissions)
2. Retrofit ROI analysis (costs vs energy savings)
3. Data quality indicators (flags)

---

## 6. Inconsistencies & Edge Cases

### ✅ Handled Correctly

1. **Null hazard scores**
   - Issue: Some hazards return `score: null` (tropical_cyclones, storm_surge, coastal_flood)
   - Handling: `isinstance(score, (int, float))` filters them out
   - Impact: These hazards don't contribute to risk score calculation

2. **Null storm_surge_loss**
   - Issue: `storm_surge_loss: null` in 8/8 responses
   - Handling: `if value` check excludes from breakdown
   - Impact: Not shown in loss breakdown (correct)

3. **Missing city/postcode**
   - Issue: 5/8 assets have null city/postcode (coordinate-only inputs)
   - Handling: Fallback to region + coordinates
   - Impact: All assets have meaningful location identifiers

4. **Null asset.name**
   - Issue: API always returns `name: null`
   - Handling: We pass asset_name from our portfolio_data.py
   - Impact: We control asset naming (intentional)

### ⚠️ None Found
No critical issues or incorrect key usage detected.

---

## 7. Verification Checklist

- [x] All top-level keys present (`asset`, `hazards`, `losses`, `conditions`)
- [x] Hazard scores correctly filtered (None values excluded)
- [x] Using correct loss field (`physical_loss`, not `expected_annual_loss_total`)
- [x] Null values in loss breakdown handled
- [x] Location fallback logic working
- [x] Risk score calculation verified (average of valid hazard scores)
- [x] All 8 successful responses have consistent structure

---

## 8. Code Correctness Summary

| Component | Status | Notes |
|-----------|--------|-------|
| API key usage | ✅ | All keys match API structure |
| Hazard parsing | ✅ | Filters None scores correctly |
| Loss extraction | ✅ | Uses `physical_loss` (correct) |
| Location building | ✅ | Handles all null cases |
| Risk calculation | ✅ | Average of valid hazard scores |
| Loss breakdown | ✅ | Excludes None and physical_loss |

**Overall:** 🟢 All API response structures correctly handled, zero critical issues.

---

*Analysis Date: 2026-03-05*
*Portfolio: 8/10 assets analyzed successfully*
*API Version: Climate X Spectra API v2.0*
