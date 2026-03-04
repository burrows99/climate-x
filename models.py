"""Data models - Only fields used from Page 5-7"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Hazard:
    """Page 6: {type, score}"""
    type: str
    score: float  # 1.0-5.0


@dataclass
class Asset:
    """Single asset risk profile"""
    name: str
    location: str
    risk_score: float
    hazards: List[Hazard] = field(default_factory=list)
    annual_loss: float = 0.0


@dataclass
class Portfolio:
    """Portfolio aggregation"""
    total: int
    successful: int
    failed: int
    assets: List[Asset] = field(default_factory=list)
    
    @property
    def avg_risk(self):
        return sum(a.risk_score for a in self.assets) / len(self.assets) if self.assets else 0.0
    
    @property
    def total_loss(self):
        return sum(a.annual_loss for a in self.assets)
