"""
CEO 전략 분석 대시보드 API 라우터
5개 산업 지원
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date

from app.core.industries import (
    IndustryCode,
    INDUSTRY_PROFILES,
    get_industry,
    get_all_industries,
    get_industry_keywords,
    get_cross_industry_keywords
)
from app.services.algorithms import (
    calculate_tam_topdown,
    calculate_tam_bottomup,
    calculate_sam,
    calculate_som,
    project_market_growth,
    calculate_five_forces,
    calculate_policy_relevance,
    classify_tech_ring,
    calculate_competitive_score,
    classify_stakeholder,
    calculate_timing_score,
    generate_timing_thesis,
    calculate_dashboard_health
)
from app.schemas.industry import (
    IndustryProfileResponse,
    AllIndustriesResponse,
    MarketSizeCalculateRequest,
    MarketSizeResponse,
    FiveForcesSaveRequest,
    FiveForcesResponse,
    PolicyRelevanceRequest,
    PolicyRelevanceResponse,
    TechClassifyRequest,
    TechClassifyResponse,
    CompetitiveMatrixRequest,
    CompetitiveMatrixResponse,
    StakeholderCreate,
    StakeholderClassifyResponse,
    TimingFactorCreate,
    TimingScoreResponse,
    TimingThesisGenerateRequest,
    TimingThesisResponse,
    DashboardHealthResponse,
    DashboardSummaryResponse
)

router = APIRouter()


# =============================================================================
# 산업 프로필 API
# =============================================================================

@router.get("/industries", response_model=AllIndustriesResponse, tags=["Industries"])
async def list_industries():
    """
    5개 산업 목록 조회

    - civil_infra: 건설 및 인프라 자산 관리
    - insurance_risk: 보험 및 리스크 금융
    - logistics_scm: 물류 및 공급망 관리
    - ai_data: AI 및 데이터 엔지니어링
    - public_law: 공공 행정 및 법률
    """
    industries = []
    for code, profile in INDUSTRY_PROFILES.items():
        industries.append(IndustryProfileResponse(
            code=profile.code.value,
            name_ko=profile.name_ko,
            name_en=profile.name_en,
            description=profile.description,
            core_concepts=profile.core_concepts,
            business_connection=profile.business_connection,
            keywords=[{"keyword": k.keyword, "category": k.category, "weight": k.weight}
                      for k in profile.keywords],
            tech_categories=profile.tech_categories
        ))

    return AllIndustriesResponse(industries=industries, total=len(industries))


@router.get("/industries/{industry_code}", response_model=IndustryProfileResponse, tags=["Industries"])
async def get_industry_profile(industry_code: str):
    """특정 산업 프로필 조회"""
    try:
        code = IndustryCode(industry_code)
        profile = get_industry(code)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Industry '{industry_code}' not found")

    return IndustryProfileResponse(
        code=profile.code.value,
        name_ko=profile.name_ko,
        name_en=profile.name_en,
        description=profile.description,
        core_concepts=profile.core_concepts,
        business_connection=profile.business_connection,
        keywords=[{"keyword": k.keyword, "category": k.category, "weight": k.weight}
                  for k in profile.keywords],
        tech_categories=profile.tech_categories
    )


@router.get("/industries/keywords/cross", tags=["Industries"])
async def get_cross_keywords():
    """
    산업 간 교차 키워드 조회
    2개 이상 산업에서 공통으로 중요한 키워드
    """
    cross_keywords = get_cross_industry_keywords()
    return {
        "cross_keywords": [
            {"keyword": k, "industries": [i.value for i in v]}
            for k, v in cross_keywords.items()
        ],
        "total": len(cross_keywords)
    }


# =============================================================================
# 시장 규모 API
# =============================================================================

@router.post("/industries/{industry_code}/market/calculate", response_model=MarketSizeResponse, tags=["Market"])
async def calculate_market_size(
    industry_code: str,
    request: MarketSizeCalculateRequest
):
    """
    TAM/SAM/SOM 계산

    - method: 'top_down' 또는 'bottom_up'
    - 필요한 파라미터만 입력
    """
    # TAM 계산
    if request.method == "top_down":
        if not all([request.total_market_budget, request.relevant_segment_ratio, request.target_application_ratio]):
            raise HTTPException(status_code=400, detail="Top-down method requires: total_market_budget, relevant_segment_ratio, target_application_ratio")

        tam_result = calculate_tam_topdown(
            request.total_market_budget,
            request.relevant_segment_ratio,
            request.target_application_ratio
        )
    else:
        if not all([request.total_potential_customers, request.avg_contract_value]):
            raise HTTPException(status_code=400, detail="Bottom-up method requires: total_potential_customers, avg_contract_value")

        tam_result = calculate_tam_bottomup(
            request.total_potential_customers,
            request.avg_contract_value,
            request.purchase_frequency or 1.0
        )

    # SAM 계산
    sam_result = calculate_sam(
        tam_result.value,
        request.geographic_focus_ratio,
        request.technology_fit_ratio
    )

    # SOM 계산
    som_result = calculate_som(
        sam_result.value,
        request.target_market_share,
        request.years_to_achieve,
        request.yearly_penetration_rate
    )

    # 성장 예측
    projections = project_market_growth(tam_result.value, 0.1, 5)  # 10% CAGR, 5년

    return MarketSizeResponse(
        tam={
            "value": tam_result.value,
            "unit": tam_result.unit,
            "calculation": tam_result.calculation,
            "method": tam_result.method
        },
        sam={
            "value": sam_result.value,
            "unit": sam_result.unit,
            "calculation": sam_result.calculation
        },
        som={
            "value": som_result.value,
            "unit": som_result.unit,
            "calculation": som_result.calculation,
            "target_year": date.today().year + request.years_to_achieve
        },
        projections=projections
    )


# =============================================================================
# Porter's 5 Forces API
# =============================================================================

@router.get("/industries/{industry_code}/forces/default", response_model=FiveForcesResponse, tags=["5 Forces"])
async def get_default_forces(industry_code: str):
    """산업별 기본 5 Forces 조회"""
    try:
        code = IndustryCode(industry_code)
        profile = get_industry(code)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Industry '{industry_code}' not found")

    forces = profile.default_forces
    result = calculate_five_forces(
        forces.get("supplier_power", 3),
        forces.get("buyer_power", 3),
        forces.get("competitive_rivalry", 3),
        forces.get("threat_of_substitution", 3),
        forces.get("threat_of_new_entry", 3)
    )

    return FiveForcesResponse(
        forces=result.forces,
        total_pressure=result.total_pressure,
        attractiveness_score=result.attractiveness_score,
        grade=result.grade,
        interpretation=result.interpretation
    )


@router.post("/industries/{industry_code}/forces/analyze", response_model=FiveForcesResponse, tags=["5 Forces"])
async def analyze_forces(industry_code: str, request: FiveForcesSaveRequest):
    """커스텀 5 Forces 분석"""
    result = calculate_five_forces(
        request.supplier_power,
        request.buyer_power,
        request.competitive_rivalry,
        request.threat_of_substitution,
        request.threat_of_new_entry
    )

    return FiveForcesResponse(
        forces=result.forces,
        total_pressure=result.total_pressure,
        attractiveness_score=result.attractiveness_score,
        grade=result.grade,
        interpretation=result.interpretation
    )


# =============================================================================
# 정책 트래킹 API
# =============================================================================

@router.post("/industries/{industry_code}/policy/relevance", response_model=PolicyRelevanceResponse, tags=["Policy"])
async def check_policy_relevance(industry_code: str, request: PolicyRelevanceRequest):
    """
    정책 문서 연관성 점수 계산

    text에 정책 제목/본문을 입력하면 해당 산업 키워드 기반으로 연관성 점수 계산
    """
    try:
        code = IndustryCode(industry_code)
        keywords = get_industry_keywords(code)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Industry '{industry_code}' not found")

    keyword_dicts = [
        {"keyword": k.keyword, "category": k.category, "weight": k.weight}
        for k in keywords
    ]

    result = calculate_policy_relevance(
        request.text,
        keyword_dicts,
        request.source_authority,
        request.policy_type
    )

    return PolicyRelevanceResponse(
        total_score=result.total_score,
        grade=result.grade,
        label=result.label,
        action=result.action,
        matched_keywords=result.matched_keywords
    )


# =============================================================================
# 기술 Radar API
# =============================================================================

@router.post("/industries/{industry_code}/tech/classify", response_model=TechClassifyResponse, tags=["Tech Radar"])
async def classify_technology(industry_code: str, request: TechClassifyRequest):
    """
    기술 Ring 분류 (Adopt/Trial/Assess/Hold)
    """
    result = classify_tech_ring(
        request.maturity_score,
        request.adoption_rate,
        request.our_experience,
        request.strategic_fit,
        request.risk_level
    )

    return TechClassifyResponse(
        name=request.name,
        ring=result.ring.value,
        score=result.score,
        reason=result.reason,
        factors=result.factors
    )


@router.get("/industries/{industry_code}/tech/categories", tags=["Tech Radar"])
async def get_tech_categories(industry_code: str):
    """산업별 기술 카테고리 조회"""
    try:
        code = IndustryCode(industry_code)
        profile = get_industry(code)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Industry '{industry_code}' not found")

    return {
        "industry": industry_code,
        "categories": profile.tech_categories
    }


# =============================================================================
# 경쟁사 분석 API
# =============================================================================

@router.post("/industries/{industry_code}/compete/matrix", response_model=CompetitiveMatrixResponse, tags=["Competitive"])
async def calculate_competitive_matrix(industry_code: str, request: CompetitiveMatrixRequest):
    """
    경쟁력 비교 매트릭스 계산

    - our_features: {"기능명": 점수(0-2)}
    - competitor_features: {"경쟁사명": {"기능명": 점수}}
    - feature_weights: {"기능명": 가중치}
    - differentiator_features: ["차별화 기능 목록"]
    """
    result = calculate_competitive_score(
        request.our_features,
        request.competitor_features,
        request.feature_weights,
        request.differentiator_features
    )

    return CompetitiveMatrixResponse(
        our_score=result.our_score,
        competitor_scores=result.competitor_scores,
        differentiators=result.differentiators,
        gaps=result.gaps
    )


# =============================================================================
# 이해관계자 API
# =============================================================================

@router.post("/industries/{industry_code}/stakeholder/classify", response_model=StakeholderClassifyResponse, tags=["Stakeholder"])
async def classify_stakeholder_strategy(industry_code: str, request: StakeholderCreate):
    """
    이해관계자 전략 분류 (Power-Interest Grid)
    """
    result = classify_stakeholder(
        request.power_level,
        request.interest_level,
        request.has_budget,
        request.has_decision_power
    )

    return StakeholderClassifyResponse(
        strategy=result.strategy.value,
        priority=result.priority,
        actions=result.actions
    )


@router.get("/industries/{industry_code}/stakeholder/templates", tags=["Stakeholder"])
async def get_stakeholder_templates(industry_code: str):
    """산업별 이해관계자 템플릿 조회"""
    try:
        code = IndustryCode(industry_code)
        profile = get_industry(code)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Industry '{industry_code}' not found")

    templates = []
    for t in profile.stakeholder_templates:
        classification = classify_stakeholder(
            t.typical_power,
            t.typical_interest,
            t.has_budget,
            t.has_decision_power
        )
        templates.append({
            "role": t.role,
            "organization_type": t.organization_type,
            "typical_power": t.typical_power,
            "typical_interest": t.typical_interest,
            "has_budget": t.has_budget,
            "has_decision_power": t.has_decision_power,
            "recommended_strategy": classification.strategy.value,
            "priority": classification.priority
        })

    return {
        "industry": industry_code,
        "templates": templates
    }


# =============================================================================
# Timing Thesis API
# =============================================================================

@router.post("/industries/{industry_code}/timing/score", response_model=TimingScoreResponse, tags=["Timing"])
async def calculate_timing(
    industry_code: str,
    factors: List[TimingFactorCreate]
):
    """
    Timing Score 계산
    """
    factor_dicts = []
    for i, f in enumerate(factors):
        factor_dicts.append({
            "id": f"factor_{i}",
            "name": f.name,
            "category": f.category,
            "maturity_level": f.maturity_level,
            "impact_score": f.impact_score,
            "confidence": f.confidence,
            "trend_direction": f.trend_direction,
            "window_start": f.window_start,
            "window_peak": f.window_peak,
            "window_end": f.window_end,
            "current_state": f.current_state
        })

    result = calculate_timing_score(factor_dicts)

    return TimingScoreResponse(
        total_score=result.total_score,
        grade=result.grade.value,
        message=result.message,
        factor_scores=result.factor_scores
    )


@router.post("/industries/{industry_code}/timing/thesis", response_model=TimingThesisResponse, tags=["Timing"])
async def generate_thesis(
    industry_code: str,
    request: TimingThesisGenerateRequest,
    factors: List[TimingFactorCreate]
):
    """
    Timing Thesis 문장 생성
    """
    factor_dicts = []
    for i, f in enumerate(factors):
        factor_dicts.append({
            "id": f"factor_{i}",
            "name": f.name,
            "category": f.category,
            "maturity_level": f.maturity_level,
            "impact_score": f.impact_score,
            "confidence": f.confidence,
            "trend_direction": f.trend_direction,
            "current_state": f.current_state
        })

    result = generate_timing_thesis(
        request.product_name,
        request.industry_name,
        factor_dicts
    )

    return TimingThesisResponse(
        thesis_statement=result["thesis_statement"],
        supporting_points=result["supporting_points"],
        one_liner=result["one_liner"]
    )


# =============================================================================
# Dashboard API
# =============================================================================

@router.get("/industries/{industry_code}/dashboard/health", response_model=DashboardHealthResponse, tags=["Dashboard"])
async def get_dashboard_health(
    industry_code: str,
    has_tam: bool = False,
    has_sam: bool = False,
    has_som: bool = False,
    has_growth_rationale: bool = False,
    policy_count: int = 0,
    competitor_count: int = 0,
    stakeholder_coverage: float = 0,
    timing_score: float = 0
):
    """
    대시보드 Health Score 조회

    각 항목 보유 여부와 수량을 쿼리 파라미터로 전달
    """
    market_data = {
        "tam": has_tam,
        "sam": has_sam,
        "som": has_som,
        "growth_rationale": has_growth_rationale
    }

    result = calculate_dashboard_health(
        market_data=market_data,
        policy_count=policy_count,
        competitor_count=competitor_count,
        stakeholder_coverage=stakeholder_coverage,
        timing_score=timing_score
    )

    return DashboardHealthResponse(
        total_score=result.total_score,
        grade=result.grade,
        status=result.status,
        breakdown=result.breakdown,
        recommendations=result.recommendations
    )


@router.get("/industries/{industry_code}/dashboard/summary", response_model=DashboardSummaryResponse, tags=["Dashboard"])
async def get_dashboard_summary(industry_code: str):
    """
    대시보드 요약 조회 (Placeholder)

    실제 구현 시 DB에서 데이터 조회
    """
    try:
        code = IndustryCode(industry_code)
        profile = get_industry(code)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Industry '{industry_code}' not found")

    # Placeholder - 실제로는 DB에서 조회
    health = calculate_dashboard_health()

    return DashboardSummaryResponse(
        industry_code=industry_code,
        industry_name=profile.name_ko,
        market=None,
        forces=profile.default_forces,
        policy_count=0,
        competitor_count=0,
        stakeholder_count=0,
        timing_score=None,
        health=DashboardHealthResponse(
            total_score=health.total_score,
            grade=health.grade,
            status=health.status,
            breakdown=health.breakdown,
            recommendations=health.recommendations
        )
    )
