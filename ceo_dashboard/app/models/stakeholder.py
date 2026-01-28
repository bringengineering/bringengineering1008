"""
이해관계자 관련 모델
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, generate_uuid


class Stakeholder(Base, TimestampMixin):
    """이해관계자"""
    __tablename__ = "stakeholders"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    industry_code = Column(String(50), nullable=False, index=True)

    name = Column(String(255), nullable=False)
    title = Column(String(255))
    organization = Column(String(255))
    department = Column(String(255))

    stakeholder_type = Column(String(50))  # individual, role

    # Power-Interest Grid (1-5)
    power_level = Column(Integer)
    interest_level = Column(Integer)
    influence_level = Column(Integer)

    # 보유 권한
    has_budget = Column(Boolean, default=False)
    has_decision_power = Column(Boolean, default=False)
    has_data_access = Column(Boolean, default=False)
    has_technical_authority = Column(Boolean, default=False)

    # 분류 결과
    strategy = Column(String(50))  # manage_closely, keep_satisfied, keep_informed, monitor
    priority = Column(Integer)

    # 관계
    relationship_status = Column(String(50))  # strong, moderate, weak, none

    # 연락처
    contact_info = Column(JSON)
    notes = Column(Text)

    # Relations
    relations_from = relationship(
        "StakeholderRelation",
        foreign_keys="StakeholderRelation.from_stakeholder_id",
        back_populates="from_stakeholder"
    )
    relations_to = relationship(
        "StakeholderRelation",
        foreign_keys="StakeholderRelation.to_stakeholder_id",
        back_populates="to_stakeholder"
    )


class StakeholderRelation(Base, TimestampMixin):
    """이해관계자 간 관계"""
    __tablename__ = "stakeholder_relations"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    from_stakeholder_id = Column(String(36), ForeignKey("stakeholders.id"), nullable=False)
    to_stakeholder_id = Column(String(36), ForeignKey("stakeholders.id"), nullable=False)

    relation_type = Column(String(50), nullable=False)  # reports_to, influences, collaborates
    strength = Column(Float, default=0.5)  # 0-1
    description = Column(Text)

    from_stakeholder = relationship("Stakeholder", foreign_keys=[from_stakeholder_id], back_populates="relations_from")
    to_stakeholder = relationship("Stakeholder", foreign_keys=[to_stakeholder_id], back_populates="relations_to")
