"""
Timing Thesis 관련 모델
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, JSON, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, generate_uuid


class TimingFactor(Base, TimestampMixin):
    """Timing Factor (왜 지금인가 요소)"""
    __tablename__ = "timing_factors"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    industry_code = Column(String(50), nullable=False, index=True)

    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # technology, policy, market, social, economic

    description = Column(Text)
    current_state = Column(Text)

    # 트렌드
    trend_direction = Column(String(50))  # accelerating, stable, decelerating
    maturity_level = Column(Float)  # 0-1

    # 기회 창
    window_start = Column(Date)
    window_peak = Column(Date)
    window_end = Column(Date)

    # 영향도
    impact_score = Column(Float)  # 0-1
    confidence = Column(Float)  # 0-1

    # Relations
    evidences = relationship("TimingEvidence", back_populates="factor", cascade="all, delete-orphan")


class TimingEvidence(Base, TimestampMixin):
    """Timing Factor 근거"""
    __tablename__ = "timing_evidences"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    factor_id = Column(String(36), ForeignKey("timing_factors.id"), nullable=False)

    title = Column(String(500), nullable=False)
    description = Column(Text)
    data_point = Column(String(255))

    source_url = Column(Text)
    source_name = Column(String(255))
    source_date = Column(Date)

    evidence_type = Column(String(50))  # statistic, news, report, event

    factor = relationship("TimingFactor", back_populates="evidences")


class TimingThesis(Base, TimestampMixin):
    """Timing Thesis (왜 지금인가 문장)"""
    __tablename__ = "timing_theses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    industry_code = Column(String(50), nullable=False, index=True)

    version = Column(Integer, default=1)
    target_audience = Column(String(100))  # investor, government, partner

    thesis_statement = Column(Text, nullable=False)
    one_liner = Column(Text)

    # AI 생성
    is_ai_generated = Column(Boolean, default=False)
    ai_model = Column(String(100))

    status = Column(String(50), default="draft")  # draft, reviewed, approved

    # 연결된 Factor IDs
    factor_ids = Column(JSON)
