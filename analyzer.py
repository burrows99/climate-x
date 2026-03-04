"""Risk Analyzer - Open/Closed Principle (extensible for new analysis)"""

from typing import Dict, Any, List
from models import Hazard, Asset, Portfolio
import config


class RiskAnalyzer:
    """Analyzes API responses - Single Responsibility"""
    
    def parse_response(self, response_data: Dict[str, Any], asset_name: str) -> Asset:
        """
        Parse API response into Asset model
        Page 5-7: {asset, hazards, losses, conditions}
        """
        # Extract hazards (Page 6)
        hazards = []
        hazards_data = response_data.get("hazards", {})
        for htype, hdata in hazards_data.items():
            if hdata and isinstance(hdata, dict):
                score = hdata.get("score")
                if isinstance(score, (int, float)):
                    hazards.append(Hazard(type=htype, score=score))
        
        # Calculate risk score (average of hazard scores)
        risk_score = sum(h.score for h in hazards) / len(hazards) if hazards else 0.0
        
        # Extract loss (Page 7: API returns "physical_loss" field)
        losses = response_data.get("losses", {})
        annual_loss = losses.get("physical_loss", 0.0)  # Actual field name from API
        
        # Build location string
        asset_info = response_data.get("asset", {})
        location_parts = [
            asset_info.get("city", ""),
            asset_info.get("postcode", "")
        ]
        location = ", ".join([p for p in location_parts if p]) or "Unknown"
        
        return Asset(
            name=asset_name,
            location=location,
            risk_score=risk_score,
            hazards=hazards,
            annual_loss=annual_loss
        )
    
    def analyze_portfolio(self, assets: List[Asset], total: int, failed: int) -> Portfolio:
        """Aggregate portfolio metrics"""
        return Portfolio(
            total=total,
            successful=len(assets),
            failed=failed,
            assets=sorted(assets, key=lambda a: a.risk_score, reverse=True)
        )
    
    def get_high_risk_assets(self, portfolio: Portfolio) -> List[Asset]:
        """Filter assets above threshold (Page 5-6: 1-5 scale)"""
        return [a for a in portfolio.assets if a.risk_score >= config.HIGH_RISK_THRESHOLD]
    
    def get_hazard_concentration(self, portfolio: Portfolio) -> Dict[str, int]:
        """Count hazard occurrence across portfolio"""
        concentration = {}
        for asset in portfolio.assets:
            for hazard in asset.hazards:
                if hazard.score >= config.HIGH_RISK_THRESHOLD:
                    concentration[hazard.type] = concentration.get(hazard.type, 0) + 1
        return dict(sorted(concentration.items(), key=lambda x: x[1], reverse=True))
