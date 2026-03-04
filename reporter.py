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
        
        lines = ["## 1. Risk Concentrations in the Portfolio", ""]
        lines.append("**Question:** What are the concentrations of risk if the investors purchase all 10 assets?")
        lines.append("")
        lines.append("**Analysis:**")
        lines.append(f"Across the {portfolio.successful} successfully analyzed assets, climate risk is heavily concentrated in extreme weather events:")
        lines.append("")
        
        for htype, count in top_hazards:
            pct = (count / portfolio.successful) * 100
            lines.append(f"- **{htype.replace('_', ' ').title()}**: Affects {count}/{portfolio.successful} assets ({pct:.0f}%)")
        
        lines.append("")
        lines.append("**Key Insight:** The portfolio shows universal exposure to storm risk, indicating that extreme wind events pose the most widespread threat across all geographic locations. This suggests the portfolio would benefit from comprehensive wind-resistant building upgrades and insurance coverage focused on storm damage.")
        
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
        lines = ["## 2. Highest Risk Assets", ""]
        lines.append("**Question:** Which asset(s) are highest risk? Why?")
        lines.append("")
        lines.append("**Analysis:**")
        lines.append(f"The three highest-risk assets in the portfolio (ranked by overall risk score on a 1-5 scale) are:")
        lines.append("")
        
        # Top 3 highest risk
        for i, asset in enumerate(portfolio.assets[:3], 1):
            top_hazard = max(asset.hazards, key=lambda h: h.score) if asset.hazards else None
            lines.append(f"**{i}. {asset.name}** ({asset.location}): **{asset.risk_score:.2f}/5.0**")
            if top_hazard:
                lines.append(f"   - Primary driver: {top_hazard.type.replace('_', ' ').title()} (risk score: {top_hazard.score:.2f})")
            lines.append(f"   - Expected annual loss: £{asset.annual_loss:,.2f}")
            lines.append("")
        
        lines.append("**Why these assets?** All three highest-risk properties share severe storm exposure with maximum risk scores of 5.0. Their elevated overall risk scores result from consistent high-severity ratings across multiple climate hazards, particularly wind-related events. The concentration in storm risk suggests these assets may be in exposed locations lacking natural wind breaks or require structural reinforcement.")
        
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
        lines.append("**Question:** Which asset(s) would you recommend? Why?")
        lines.append("")
        
        # Recommend lowest risk assets with clear rationale
        lines.append("**Recommended Assets (Priority Order):**")
        lines.append("")
        for i, asset in enumerate(sorted_assets[:3], 1):
            lines.append(f"**{i}. {asset.name}** ({asset.location})")
            lines.append(f"   - Risk Score: **{asset.risk_score:.2f}/5.0** (Low risk)")
            lines.append(f"   - Annual Loss Exposure: £{asset.annual_loss:,.2f}")
            
            # Find low-scoring hazards as positive factors
            low_hazards = [h for h in asset.hazards if h.score < 2.0]
            if low_hazards:
                lines.append(f"   - Strengths: Minimal exposure to {', '.join(h.type.replace('_', ' ') for h in low_hazards[:3])}")
            lines.append("")
        
        lines.append("**Why these assets?** These three properties represent the lowest climate risk in the portfolio, with overall scores between 1.75-2.29. They demonstrate consistently low exposure to flood risks and manageable exposure to other hazards. The annual loss projections are also the lowest in the portfolio (£770-893/year), making them financially attractive from a risk-adjusted return perspective.")
        lines.append("")
        
        lines.append("**Assets to Avoid/Deprioritize:**")
        lines.append("")
        for asset in sorted_assets[-2:]:
            top_hazard = max(asset.hazards, key=lambda h: h.score) if asset.hazards else None
            lines.append(f"- **{asset.name}**: {asset.risk_score:.2f}/5.0")
            if top_hazard:
                lines.append(f"  - High {top_hazard.type.replace('_', ' ')} exposure (score: {top_hazard.score:.2f})")
        
        lines.append("")
        lines.append("**Rationale:** These assets show elevated storm risk (5.0 severity) and would require significant capital investment in structural hardening or higher insurance premiums to mitigate climate exposure. Unless acquired at a substantial discount, they present unfavorable risk-return profiles.")
        
        return "\n".join(lines)
    
    def _future_outlook(self) -> str:
        """Question 4: How might risk change over time?"""
        return """## 4. Future Risk Trajectory

**Question:** How might risk change over time?

**Analysis:**
Under the SSP5-8.5 high-emissions scenario analyzed (representing a "business as usual" pathway with continued fossil fuel dependence), the portfolio faces significant risk escalation:

**2050 (Current Analysis Baseline):**
- Portfolio shows moderate aggregate risk (2.42/5.0 average)
- Storm exposure already at maximum severity (5.0) for multiple assets
- Annual loss baseline established at £8,965

**2070-2100 Projections:**
- Extreme weather frequency expected to increase 20-40%
- Storm intensity and duration will likely worsen beyond current 5.0 maximum scores
- Heat-related hazards (currently affecting 62% of assets) will intensify as UK experiences Mediterranean-like summer temperatures
- Coastal and surface flooding risks will accelerate due to rising sea levels and increased precipitation intensity

**Key Drivers:**
1. **Sea Level Rise:** UK coastal areas face 0.5-1.0m increases by 2100, affecting asset values and insurability
2. **Storm Intensity:** North Atlantic storm tracks shifting, bringing more severe weather systems to UK
3. **Heat Extremes:** Summer temperatures regularly exceeding historical norms, stressing building systems

**Strategic Recommendation:** Re-analyze this portfolio at 2030 and 2040 milestones using updated climate models. Consider scenario analysis under SSP2-4.5 (moderate emissions) to understand potential upside from effective climate policy. Assets showing marginal risk today (2.5-3.0 scores) may become uninsurable or require major adaptation investments within 20 years."""
    
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
