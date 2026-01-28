"""
산업 분석 관련 모델
- 산업 분석 (IndustryAnalysis)
- 시장 규모 (MarketSize)
- 정책 아이템 (PolicyItem)
- 경쟁사 (Competitor)
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, generate_uuid


class IndustryAnalysis(Base, TimestampMixin):
    """산업 분석 (5 Forces 포함)"""
    __tablename__ = "industry_analyses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    industry_code = Column(String(50), nullable=False, index=True)  # civil_infra, insurance_risk, etc.

    # Porter's 5 Forces (1-5)
    supplier_power = Column(Integer)
    buyer_power = Column(Integer)
    competitive_rivalry = Column(Integer)
    threat_of_substitution = Column(Integer)
    threat_of_new_entry = Column(Integer)

    # 상세 분석
    forces_details = Column(JSON)  # 각 Force별 상세 요소
    analysis_notes = Column(Text)

    # 산업 매력도 점수 (계산됨)
    attractiveness_score = Column(Float)
    attractiveness_grade = Column(String(5))  # A, B, C, D, E


class MarketSize(Base, TimestampMixin):
    """시장 규모 분석"""
    __tablename__ = "market_sizes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    industry_code = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    base_year = Column(Integer, nullable=False)

    # TAM
    tam_value = Column(Float)
    tam_unit = Column(String(20), default="억원")
    tam_method = Column(String(50))  # top_down, bottom_up
    tam_assumptions = Column(JSON)
    tam_sources = Column(JSON)  # List of sources

    # SAM
    sam_value = Column(Float)
    sam_unit = Column(String(20), default="억원")
    sam_assumptions = Column(JSON)

    # SOM
    som_value = Column(Float)
    som_unit = Column(String(20), default="억원")
    som_assumptions = Column(JSON)
    som_target_year = Column(Integer)

    # 성장률
    cagr_percent = Column(Float)
    growth_rationale = Column(Text)

    # 상태
    status = Column(String(50), default="draft")  # draft, reviewed, approved

    # Relations
    evidences = relationship("MarketEvidence", back_populates="market", cascade="all, delete-orphan")


class MarketEvidence(Base, TimestampMixin):
    """시장 규모 근거 자료"""
    __tablename__ = "market_evidences"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    market_id = Column(String(36), ForeignKey("market_sizes.id"), nullable=False)

    evidence_type = Column(String(50), nullable=False)  # accident_stat, policy_budget, etc.
    title = Column(String(500), nullable=False)
    description = Column(Text)

    data_value = Column(String(255))
    data_year = Column(Integer)
    data_source = Column(String(255))
    source_url = Column(Text)

    reliability = Column(String(20), default="medium")  # high, medium, low

    market = relationship("MarketSize", back_populates="evidences")


class PolicyItem(Base, TimestampMixin):
    """정책 아이템"""
    __tablename__ = "policy_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    industry_code = Column(String(50), nullable=False, index=True)

    # 기본 정보
    title = Column(String(1000), nullable=False)
    source_org = Column(String(255), nullable=False)
    source_type = Column(String(50))  # ministry, agency, local_gov
    policy_type = Column(String(50))  # law, plan, budget, press_release

    source_url = Column(Text)
    published_at = Column(DateTime)

    # 본문
    content_raw = Column(Text)

    # AI 분석
    summary = Column(Text)
    key_points = Column(JSON)
    ai_analysis = Column(JSON)

    # 연관성
    relevance_score = Column(Float)
    relevance_grade = Column(Integer)  # 1-5
    matched_keywords = Column(JSON)

    # 사용자 분류
    is_bookmarked = Column(Boolean, default=False)
    is_read = Column(Boolean, default=False)
    user_notes = Column(Text)
    tags = Column(JSON)

    crawled_at = Column(DateTime)
    analyzed_at = Column(DateTime)


class Competitor(Base, TimestampMixin):
    """경쟁사"""
    __tablename__ = "competitors"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    industry_code = Column(String(50), nullable=False, index=True)

    name = Column(String(255), nullable=False)
    name_en = Column(String(255))
    country = Column(String(100))
    website = Column(Text)

    competitor_type = Column(String(50), nullable=False)  # direct, indirect, potential
    description = Column(Text)
    approach_difference = Column(Text)

    # 포지셔닝 (0-1)
    position_price = Column(Float)
    position_technology = Column(Float)
    position_quality = Column(Float)
    position_coverage = Column(Float)
    position_innovation = Column(Float)
    position_service = Column(Float)

    # SWOT
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    opportunities = Column(JSON)
    threats = Column(JSON)

    data_confidence = Column(String(20), default="medium")


class TechItem(Base, TimestampMixin):
    """기술 Radar 아이템"""
    __tablename__ = "tech_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    industry_code = Column(String(50), nullable=False, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text)

    quadrant = Column(String(50), nullable=False)  # techniques, tools, platforms, languages
    ring = Column(String(50), nullable=False)  # adopt, trial, assess, hold

    # 평가 요소 (0-1)
    maturity_score = Column(Float)
    adoption_rate = Column(Float)
    our_experience = Column(Float)
    strategic_fit = Column(Float)
    risk_level = Column(Float)

    # 대체 가능성
    is_replaceable = Column(Boolean)
    replaceability_score = Column(Float)

    # 우리 기술과의 관계
    our_position = Column(Text)

    is_new = Column(Boolean, default=True)
