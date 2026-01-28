"""
API Request/Response 스키마
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date, datetime
from enum import Enum


# =============================================================================
# Enums
# =============================================================================

class IndustryCode(str, Enum):
    CIVIL_INFRA = "civil_infra"
    INSURANCE_RISK = "insurance_risk"
    LOGISTICS_SCM = "logistics_scm"
    AI_DATA = "ai_data"
    PUBLIC_LAW = "public_law"


# =============================================================================
# 산업 프로필
# =============================================================================

class IndustryProfileResponse(BaseModel):
    code: str
    name_ko: str
    name_en: str
    description: str
    core_concepts: List[str]
    business_connection: str
    keywords: List[Dict]
    tech_categories: List[str]

    class Config:
        from_attributes = True


class AllIndustriesResponse(BaseModel):
    industries: List[IndustryProfileResponse]
    total: int


# =============================================================================
# 시장 규모
# =============================================================================

class MarketSizeCalculateRequest(BaseModel):
    method: str = Field(..., description="top_down or bottom_up")

    # Top-down params
    total_market_budget: Optional[float] = Field(None, description="전체 시장 예산 (억원)")
    relevant_segment_ratio: Optional[float] = Field(None, description="관련 세그먼트 비율 (0-1)")
    target_application_ratio: Optional[float] = Field(None, description="기술 적용 가능 비율 (0-1)")

    # Bottom-up params
    total_potential_customers: Optional[int] = Field(None, description="잠재 고객 수")
    avg_contract_value: Optional[float] = Field(None, description="평균 계약 규모")
    purchase_frequency: Optional[float] = Field(None, description="연간 구매 빈도", default=1.0)

    # SAM params
    geographic_focus_ratio: float = Field(1.0, description="지역 집중 비율")
    technology_fit_ratio: float = Field(1.0, description="기술 적합 비율")

    # SOM params
    target_market_share: float = Field(0.1, description="목표 시장 점유율")
    years_to_achieve: int = Field(5, description="목표 달성 기간")
    yearly_penetration_rate: float = Field(0.3, description="연간 침투율")


class MarketSizeResponse(BaseModel):
    tam: Dict
    sam: Dict
    som: Dict
    projections: Optional[List[Dict]] = None


class MarketEvidenceCreate(BaseModel):
    evidence_type: str
    title: str
    description: Optional[str] = None
    data_value: str
    data_year: Optional[int] = None
    data_source: str
    source_url: Optional[str] = None
    reliability: str = "medium"


# =============================================================================
# Porter's 5 Forces
# =============================================================================

class FiveForcesSaveRequest(BaseModel):
    supplier_power: int = Field(..., ge=1, le=5)
    buyer_power: int = Field(..., ge=1, le=5)
    competitive_rivalry: int = Field(..., ge=1, le=5)
    threat_of_substitution: int = Field(..., ge=1, le=5)
    threat_of_new_entry: int = Field(..., ge=1, le=5)
    analysis_notes: Optional[str] = None


class FiveForcesResponse(BaseModel):
    forces: Dict[str, int]
    total_pressure: int
    attractiveness_score: int
    grade: str
    interpretation: str


# =============================================================================
# 정책 트래킹
# =============================================================================

class PolicyRelevanceRequest(BaseModel):
    text: str
    source_authority: str = "ministry"
    policy_type: str = "press_release"


class PolicyRelevanceResponse(BaseModel):
    total_score: float
    grade: int
    label: str
    action: str
    matched_keywords: List[str]


class PolicyItemResponse(BaseModel):
    id: str
    industry_code: str
    title: str
    source_org: str
    policy_type: Optional[str]
    source_url: Optional[str]
    published_at: Optional[datetime]
    summary: Optional[str]
    relevance_score: Optional[float]
    relevance_grade: Optional[int]
    is_bookmarked: bool
    tags: Optional[List[str]]

    class Config:
        from_attributes = True


# =============================================================================
# 기술 Radar
# =============================================================================

class TechClassifyRequest(BaseModel):
    name: str
    maturity_score: float = Field(..., ge=0, le=1)
    adoption_rate: float = Field(..., ge=0, le=1)
    our_experience: float = Field(..., ge=0, le=1)
    strategic_fit: float = Field(..., ge=0, le=1)
    risk_level: float = Field(..., ge=0, le=1)


class TechClassifyResponse(BaseModel):
    name: str
    ring: str
    score: float
    reason: str
    factors: Dict[str, float]


class TechRadarResponse(BaseModel):
    quadrants: List[Dict]
    rings: List[Dict]
    items: List[Dict]


# =============================================================================
# 경쟁사 분석
# =============================================================================

class CompetitorCreate(BaseModel):
    name: str
    name_en: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    competitor_type: str = "direct"
    description: Optional[str] = None
    approach_difference: Optional[str] = None

    # 포지셔닝 (0-1)
    position_price: Optional[float] = None
    position_technology: Optional[float] = None
    position_quality: Optional[float] = None

    # SWOT
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None


class CompetitiveMatrixRequest(BaseModel):
    our_features: Dict[str, int]  # {feature: 0-2}
    competitor_features: Dict[str, Dict[str, int]]  # {competitor: {feature: score}}
    feature_weights: Dict[str, float]  # {feature: weight}
    differentiator_features: List[str]


class CompetitiveMatrixResponse(BaseModel):
    our_score: float
    competitor_scores: Dict[str, float]
    differentiators: List[str]
    gaps: List[Dict]


# =============================================================================
# 이해관계자
# =============================================================================

class StakeholderCreate(BaseModel):
    name: str
    title: Optional[str] = None
    organization: Optional[str] = None
    power_level: int = Field(..., ge=1, le=5)
    interest_level: int = Field(..., ge=1, le=5)
    has_budget: bool = False
    has_decision_power: bool = False
    notes: Optional[str] = None


class StakeholderClassifyResponse(BaseModel):
    strategy: str
    priority: int
    actions: List[str]


class PowerInterestGridResponse(BaseModel):
    manage_closely: List[Dict]
    keep_satisfied: List[Dict]
    keep_informed: List[Dict]
    monitor: List[Dict]
    statistics: Dict


# =============================================================================
# Timing Thesis
# =============================================================================

class TimingFactorCreate(BaseModel):
    name: str
    category: str  # technology, policy, market, social, economic
    description: Optional[str] = None
    current_state: Optional[str] = None
    trend_direction: str = "stable"  # accelerating, stable, decelerating
    maturity_level: float = Field(0.5, ge=0, le=1)
    impact_score: float = Field(0.5, ge=0, le=1)
    confidence: float = Field(0.5, ge=0, le=1)
    window_start: Optional[date] = None
    window_peak: Optional[date] = None
    window_end: Optional[date] = None


class TimingScoreResponse(BaseModel):
    total_score: float
    grade: str
    message: str
    factor_scores: List[Dict]


class TimingThesisGenerateRequest(BaseModel):
    product_name: str
    industry_name: str
    factor_ids: Optional[List[str]] = None


class TimingThesisResponse(BaseModel):
    thesis_statement: str
    supporting_points: List[Dict]
    one_liner: str


# =============================================================================
# Dashboard
# =============================================================================

class DashboardHealthResponse(BaseModel):
    total_score: float
    grade: str
    status: str
    breakdown: Dict[str, float]
    recommendations: List[str]


class DashboardSummaryResponse(BaseModel):
    industry_code: str
    industry_name: str
    market: Optional[Dict]
    forces: Optional[Dict]
    policy_count: int
    competitor_count: int
    stakeholder_count: int
    timing_score: Optional[float]
    health: DashboardHealthResponse
