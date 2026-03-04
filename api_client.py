"""API Client - Page 3-4, Single Responsibility Principle"""

import requests
import time
from typing import Dict, Any

import config
from logger import get_logger
from validator import validate_asset

logger = get_logger()


class ClimateAPI:
    """HTTP client - only handles API communication"""
    
    def __init__(self):
        self.api_key = config.API_KEY
        self.url = config.API_URL
        self.timeout = config.TIMEOUT
    
    def fetch_risk(self, asset: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch risk for single asset
        Page 4-8: POST with data{} and options{}
        Returns: {"success": bool, "data": dict, "error": str}
        """
        asset_id = asset.get("id", "?")
        logger.info(f"Asset {asset_id}: API call starting")
        
        # Validate
        is_valid, error = validate_asset(asset)
        if not is_valid:
            logger.error(f"Asset {asset_id}: {error}")
            return {"success": False, "error": error}
        
        # Request
        start = time.time()
        try:
            response = requests.post(
                self.url,
                headers=self._headers(),
                json=self._payload(asset),
                timeout=self.timeout
            )
            duration = time.time() - start
            
            response.raise_for_status()
            
            logger.info(f"Asset {asset_id}: Success ({duration:.2f}s)")
            return {"success": True, "data": response.json(), "duration": duration}
            
        except requests.exceptions.Timeout:
            logger.error(f"Asset {asset_id}: Timeout")
            return {"success": False, "error": "Timeout"}
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Asset {asset_id}: HTTP {e.response.status_code}")
            return {"success": False, "error": f"HTTP {e.response.status_code}"}
            
        except Exception as e:
            logger.error(f"Asset {asset_id}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _headers(self):
        """Page 4: Required headers"""
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
    
    def _payload(self, asset):
        """Page 4: {data, options} structure"""
        data = {"country_id": config.COUNTRY_ID}
        
        # Location (Page 4: multiple options)
        if asset.get("latitude") is not None:
            data["latitude"] = asset["latitude"]
            data["longitude"] = asset["longitude"]
        if asset.get("uprn"):
            data["property_identifier"] = asset["uprn"]
        for key in ["city", "postcode", "building_number"]:
            if asset.get(key):
                data[key] = asset[key]
        if asset.get("street"):
            data["street_name"] = asset["street"]
        
        # Building defaults (Page 12-13)
        data.update({
            "age_category": config.AGE_CATEGORY,
            "asset_use": config.ASSET_USE,
            "asset_type": config.ASSET_TYPE,
            "structure_category": config.STRUCTURE_CATEGORY,
            "building_replacement_cost": config.REPLACEMENT_COST,
            "premise_area": config.PREMISE_AREA,
            "floor_count": config.FLOOR_COUNT
        })
        
        return {
            "data": data,
            "options": {
                "year": config.YEAR,
                "scenario": config.SCENARIO,
                "defended": config.DEFENDED
            }
        }
