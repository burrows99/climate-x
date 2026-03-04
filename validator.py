"""Validation - Page 4: API requires country + (UPRN OR coordinates OR full address)"""

def validate_asset(asset):
    """Returns (is_valid, error_message)"""
    if not asset.get("country"):
        return False, "Missing country"
    
    # Option 1: UPRN
    if asset.get("uprn"):
        return True, ""
    
    # Option 2: Coordinates
    if asset.get("latitude") is not None and asset.get("longitude") is not None:
        return True, ""
    
    # Option 3: Full address
    if all([asset.get("building_number"), asset.get("street"), 
            asset.get("city"), asset.get("postcode")]):
        return True, ""
    
    return False, "Need: UPRN OR coordinates OR complete address"
