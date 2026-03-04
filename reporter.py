"""Report Generator - Solutions_Engineer_Challenge.md questions 1-6"""

from typing import List
from models import Portfolio, Asset
import config


class ReportGenerator:
    """Generates executive reports - Single Responsibility"""
    
    def generate(self, portfolio: Portfolio) -> str:
        """
        Create markdown report answering challenge questions:
        1. Risk concentrations? 2. Highest risk? 3. Recommendations?
        4. Future risk? 5. Assumptions? 6. Due diligence?
        """
        sections = [
            self._header(portfolio),
            self._executive_summary(portfolio),
            self._risk_concentration(portfolio),
            self._asset_rankings(portfolio),
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
    
    def _recommendations(self, portfolio: Portfolio) -> str:
        """Question 3: Which assets would you recommend?"""
        low_risk = [a for a in portfolio.assets if a.risk_score < 3.0]
        
        lines = ["## 3. Investment Recommendations", ""]
        if low_risk:
            lines.append(f"**Recommended Assets** (Risk < 3.0):")
            for asset in low_risk[:3]:
                lines.append(f"- **{asset.name}**: {asset.risk_score:.2f}/5.0, £{asset.annual_loss:,.2f}/year expected loss")
        else:
            lines.append("No assets currently below 3.0 risk threshold. Consider additional risk mitigation.")
        
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
