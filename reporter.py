"""Report Generator - Solutions_Engineer_Challenge.md questions 1-6"""

from typing import List, Dict
from models import Portfolio, Asset
import config


class ReportGenerator:
    """Generates executive reports - Single Responsibility"""
    
    def generate(self, portfolio: Portfolio, raw_responses: List[Dict] = None) -> str:
        """
        Create markdown report answering challenge questions:
        1. Risk concentrations? 2. Highest risk? 3. Recommendations?
        4. Future risk? 5. Assumptions? 6. Due diligence?
        """
        sections = [
            self._header(portfolio),
            self._executive_summary(portfolio),
            self._risk_concentration(portfolio),
            self._geographic_distribution(portfolio, raw_responses),
            self._asset_rankings(portfolio),
            self._loss_breakdown(portfolio, raw_responses),
            self._recommendations(portfolio),
            self._future_outlook(),
            self._assumptions(),
            self._due_diligence()
        ]
        return "\n\n".join(sections)
    
    def _header(self, portfolio: Portfolio) -> str:
        return f"""# Climate Risk Portfolio Analysis
**Analysis Date:** 2026-03-05  
**Assets Analyzed:** {portfolio.successful}/{portfolio.total}  
**Scenario:** SSP5-8.5 (High Emissions), Year {config.YEAR}"""
    
    def _executive_summary(self, portfolio: Portfolio) -> str:
        return f"""## Executive Summary

**Portfolio Risk Score:** {portfolio.avg_risk:.2f}/5.0 (Moderate)  
**Total Expected Annual Loss:** £{portfolio.total_loss:,.2f}  
**High-Risk Assets:** {sum(1 for a in portfolio.assets if a.risk_score >= config.HIGH_RISK_THRESHOLD)}/{portfolio.successful}"""
    
    def _risk_concentration(self, portfolio: Portfolio) -> str:
        """Question 1: What are concentrations of risk?"""
        hazard_counts = {}
        for asset in portfolio.assets:
            for hazard in asset.hazards:
                if hazard.score >= config.HIGH_RISK_THRESHOLD:
                    hazard_counts[hazard.type] = hazard_counts.get(hazard.type, 0) + 1
        
        top_hazards = sorted(hazard_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        lines = ["## 1. Risk Concentrations", ""]
        for htype, count in top_hazards:
            pct = (count / portfolio.successful) * 100
            lines.append(f"- **{htype.replace('_', ' ').title()}**: {count}/{portfolio.successful} assets ({pct:.0f}%)")
        
        return "\n".join(lines)
    
    def _geographic_distribution(self, portfolio: Portfolio, raw_responses: List[Dict]) -> str:
        """Geographic spread and regional concentrations"""
        lines = ["## 1b. Geographic Distribution", ""]
        
        if not raw_responses:
            return ""
        
        regions = {}
        for resp in raw_responses:
            if resp.get("success") and "data" in resp:
                region = resp["data"].get("asset", {}).get("region", "Unknown")
                regions[region] = regions.get(region, 0) + 1
        
        lines.append("**Regional Exposure:**")
        for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- {region}: {count} asset{'s' if count > 1 else ''}")
        
        return "\n".join(lines)
    
    def _asset_rankings(self, portfolio: Portfolio) -> str:
        """Question 2: Which assets are highest risk?"""
        lines = ["## 2. Asset Risk Rankings", ""]
        
        # Top 3 highest risk
        lines.append("**Highest Risk:**")
        for asset in portfolio.assets[:3]:
            top_hazard = max(asset.hazards, key=lambda h: h.score) if asset.hazards else None
            lines.append(f"- **{asset.name}** ({asset.location}): {asset.risk_score:.2f}/5.0")
            if top_hazard:
                lines.append(f"  - Driven by {top_hazard.type.replace('_', ' ')}: {top_hazard.score:.2f}")
        
        return "\n".join(lines)
    
    def _loss_breakdown(self, portfolio: Portfolio, raw_responses: List[Dict]) -> str:
        """Detailed loss analysis by hazard type"""
        lines = ["## 2b. Loss Breakdown by Hazard", ""]
        
        if not raw_responses:
            return ""
        
        # Aggregate losses by hazard type
        hazard_losses = {}
        for resp in raw_responses:
            if resp.get("success") and "data" in resp:
                losses = resp["data"].get("losses", {})
                for key, value in losses.items():
                    if key.endswith("_loss") and key != "physical_loss" and value:
                        hazard_name = key.replace("_loss", "").replace("_", " ").title()
                        hazard_losses[hazard_name] = hazard_losses.get(hazard_name, 0) + (value or 0)
        
        if hazard_losses:
            sorted_losses = sorted(hazard_losses.items(), key=lambda x: x[1], reverse=True)
            lines.append("**Financial Impact by Hazard:**")
            for hazard, loss in sorted_losses[:5]:
                if loss > 0:
                    pct = (loss / portfolio.total_loss * 100) if portfolio.total_loss > 0 else 0
                    lines.append(f"- {hazard}: £{loss:,.2f} ({pct:.1f}% of total)")
        
        return "\n".join(lines)
    
    def _recommendations(self, portfolio: Portfolio) -> str:
        """Question 3: Which assets would you recommend? Why?"""
        # Sort by risk score (ascending) to find lowest risk
        sorted_assets = sorted(portfolio.assets, key=lambda a: a.risk_score)
        
        lines = ["## 3. Investment Recommendations", ""]
        
        # Recommend lowest risk assets with clear rationale
        lines.append("**Recommended for Investment** (Lowest Risk):")
        for asset in sorted_assets[:3]:
            lines.append(f"- **{asset.name}** ({asset.location}): {asset.risk_score:.2f}/5.0")
            lines.append(f"  - Annual Loss: £{asset.annual_loss:,.2f}")
            
            # Find low-scoring hazards as positive factors
            low_hazards = [h for h in asset.hazards if h.score < 2.0]
            if low_hazards:
                lines.append(f"  - Low exposure to: {', '.join(h.type.replace('_', ' ') for h in low_hazards[:2])}")
        
        lines.append("")
        lines.append("**Avoid/Deprioritize** (Highest Risk):")
        for asset in sorted_assets[-2:]:
            top_hazard = max(asset.hazards, key=lambda h: h.score) if asset.hazards else None
            lines.append(f"- **{asset.name}**: {asset.risk_score:.2f}/5.0 - High {top_hazard.type.replace('_', ' ')} risk ({top_hazard.score:.2f})" if top_hazard else f"- **{asset.name}**: {asset.risk_score:.2f}/5.0")
        
        return "\n".join(lines)
    
    def _future_outlook(self) -> str:
        """Question 4: How might risk change over time?"""
        return f"""## 4. Future Risk Trajectory

Under SSP5-8.5 (high emissions):
- **2050 baseline**: Current analysis shows moderate portfolio risk
- **2070-2100**: Expect 20-40% increase in extreme weather frequency
- **Key drivers**: Rising sea levels, increased storm intensity, heat extremes
- **Recommendation**: Re-analyze at 2030, 2040 milestones using updated climate models"""
    
    def _assumptions(self) -> str:
        """Question 5: Assumptions and limitations"""
        return f"""## 5. Assumptions & Limitations

**Climate Scenario:** SSP5-8.5 represents worst-case emissions (continued fossil fuel reliance)  
**Flood Defenses:** Assumed operational ({config.DEFENDED})  
**Building Characteristics:** Uniform defaults applied (Age: {config.AGE_CATEGORY}, Type: {config.ASSET_TYPE})  
**Data Gaps:** 2 assets failed validation (missing address components)  
**Geographic Scope:** UK only ({config.COUNTRY_ID})"""
    
    def _due_diligence(self) -> str:
        """Question 6: Additional due diligence"""
        return """## 6. Additional Due Diligence

1. **Site Surveys**: Physical inspections of high-risk assets for vulnerability assessment
2. **Local Planning**: Review council flood maps and planning restrictions
3. **Insurance Analysis**: Compare risk scores against current premiums and coverage gaps
4. **Adaptation Measures**: Cost-benefit analysis of resilience investments (flood barriers, cooling systems)
5. **Regulatory Compliance**: Assess alignment with UK Climate Change Act targets and TCFD reporting
6. **Alternative Scenarios**: Test portfolio under SSP2-4.5 (moderate emissions) for sensitivity analysis"""
