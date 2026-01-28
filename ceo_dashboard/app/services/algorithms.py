"""
CEO 전략 분석 알고리즘
모든 산업에 적용 가능한 범용 알고리즘
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
import math


# =============================================================================
# 1. 시장 규모 계산 (TAM/SAM/SOM)
# =============================================================================

@dataclass
class MarketSizeResult:
    value: float
    unit: str
    calculation: str
    method: str


def calculate_tam_topdown(
    total_market_budget: float,
    relevant_segment_ratio: float,
    target_application_ratio: float,
    unit: str = "억원"
) -> MarketSizeResult:
    """
    Top-Down TAM 계산

    예시 (건설/인프라):
    - 전체 인프라 예산: 50조원
    - 안전 관련 비율: 5%
    - 우리 기술 적용 가능 비율: 30%
    - TAM = 500,000억 × 0.05 × 0.30 = 7,500억원
    """
    tam = total_market_budget * relevant_segment_ratio * target_application_ratio

    calculation = f"{total_market_budget:,.0f} × {relevant_segment_ratio:.1%} × {target_application_ratio:.1%} = {tam:,.0f}"

    return MarketSizeResult(
        value=round(tam, 2),
        unit=unit,
        calculation=calculation,
        method="top_down"
    )


def calculate_tam_bottomup(
    total_potential_customers: int,
    avg_contract_value: float,
    purchase_frequency_per_year: float,
    unit: str = "억원"
) -> MarketSizeResult:
    """
    Bottom-Up TAM 계산

    예시 (보험):
    - 잠재 고객 (보험사): 30개
    - 평균 계약 규모: 10억원/년
    - TAM = 30 × 10 = 300억원
    """
    tam = total_potential_customers * avg_contract_value * purchase_frequency_per_year

    calculation = f"{total_potential_customers:,} customers × {avg_contract_value:,.0f} × {purchase_frequency_per_year:.1f}/year = {tam:,.0f}"

    return MarketSizeResult(
        value=round(tam, 2),
        unit=unit,
        calculation=calculation,
        method="bottom_up"
    )


def calculate_sam(
    tam: float,
    geographic_focus_ratio: float,
    technology_fit_ratio: float,
    unit: str = "억원"
) -> MarketSizeResult:
    """
    SAM (Serviceable Addressable Market) 계산

    SAM = TAM × 지역 집중 비율 × 기술 적합 비율
    """
    sam = tam * geographic_focus_ratio * technology_fit_ratio

    calculation = f"{tam:,.0f} × {geographic_focus_ratio:.1%} × {technology_fit_ratio:.1%} = {sam:,.0f}"

    return MarketSizeResult(
        value=round(sam, 2),
        unit=unit,
        calculation=calculation,
        method="derived_from_tam"
    )


def calculate_som(
    sam: float,
    target_market_share: float,
    years_to_achieve: int,
    yearly_penetration_rate: float,
    unit: str = "억원"
) -> MarketSizeResult:
    """
    SOM (Serviceable Obtainable Market) 계산

    SOM = SAM × 목표 점유율 × 침투 계수
    침투 계수 = 1 - (1 - 연간침투율)^기간
    """
    penetration_factor = 1 - ((1 - yearly_penetration_rate) ** years_to_achieve)
    som = sam * target_market_share * penetration_factor

    calculation = f"{sam:,.0f} × {target_market_share:.1%} × {penetration_factor:.2f} = {som:,.0f}"

    return MarketSizeResult(
        value=round(som, 2),
        unit=unit,
        calculation=calculation,
        method="penetration_model"
    )


def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
    """연평균 성장률 계산"""
    if start_value <= 0 or years <= 0:
        return 0.0
    return ((end_value / start_value) ** (1 / years)) - 1


def project_market_growth(
    base_value: float,
    cagr: float,
    years: int
) -> List[Dict[str, float]]:
    """연도별 시장 성장 예측"""
    projections = []
    for year in range(years + 1):
        value = base_value * ((1 + cagr) ** year)
        projections.append({
            "year_offset": year,
            "value": round(value, 2),
            "growth_from_base": round((value / base_value - 1) * 100, 1)
        })
    return projections


# =============================================================================
# 2. Porter's 5 Forces 분석
# =============================================================================

@dataclass
class ForcesResult:
    forces: Dict[str, int]
    total_pressure: int
    attractiveness_score: int
    grade: str
    interpretation: str


def calculate_five_forces(
    supplier_power: int,
    buyer_power: int,
    competitive_rivalry: int,
    threat_of_substitution: int,
    threat_of_new_entry: int
) -> ForcesResult:
    """
    Porter's 5 Forces 분석

    각 Force: 1(낮음) ~ 5(높음)
    총 압력: 5~25 (낮을수록 좋음)
    매력도: 25 - 총압력 = 0~20 (높을수록 좋음)
    """
    forces = {
        "supplier_power": supplier_power,
        "buyer_power": buyer_power,
        "competitive_rivalry": competitive_rivalry,
        "threat_of_substitution": threat_of_substitution,
        "threat_of_new_entry": threat_of_new_entry
    }

    total_pressure = sum(forces.values())
    attractiveness = 25 - total_pressure

    # 등급 산정
    if attractiveness >= 16:
        grade, interpretation = "A", "매우 매력적인 산업 - 적극 진입 권장"
    elif attractiveness >= 12:
        grade, interpretation = "B", "매력적인 산업 - 진입 고려"
    elif attractiveness >= 8:
        grade, interpretation = "C", "보통 산업 - 신중한 접근 필요"
    elif attractiveness >= 4:
        grade, interpretation = "D", "비매력적 산업 - 차별화 전략 필수"
    else:
        grade, interpretation = "E", "매우 비매력적 - 진입 재고 필요"

    return ForcesResult(
        forces=forces,
        total_pressure=total_pressure,
        attractiveness_score=attractiveness,
        grade=grade,
        interpretation=interpretation
    )


# =============================================================================
# 3. 정책 연관성 점수
# =============================================================================

@dataclass
class RelevanceResult:
    total_score: float
    grade: int  # 1-5
    label: str
    action: str
    matched_keywords: List[str]
    category_scores: Dict[str, float]


def calculate_policy_relevance(
    text: str,
    keywords: List[Dict],  # [{"keyword": str, "category": str, "weight": float}]
    source_authority: str,
    policy_type: str
) -> RelevanceResult:
    """
    정책 문서 연관성 점수 계산
    """
    text_lower = text.lower()
    matched = []
    category_scores: Dict[str, float] = {}

    # 키워드 매칭
    for kw in keywords:
        keyword = kw["keyword"].lower()
        category = kw.get("category", "general")
        weight = kw.get("weight", 1.0)

        count = text_lower.count(keyword)
        if count > 0:
            matched.append(kw["keyword"])
            score = weight * (1 + 0.3 * min(count - 1, 5))  # 반복 출현 감쇠

            if category not in category_scores:
                category_scores[category] = 0
            category_scores[category] += score

    keyword_score = sum(category_scores.values())

    # 출처 가중치
    authority_weights = {
        "ministry": 1.5,      # 부처
        "agency": 1.3,        # 공공기관
        "research": 1.2,      # 연구기관
        "association": 1.0,   # 협회
        "news": 0.8           # 언론
    }
    authority_weight = authority_weights.get(source_authority, 1.0)

    # 정책 유형 가중치
    type_weights = {
        "law": 2.0,           # 법령
        "plan": 1.5,          # 계획
        "budget": 1.8,        # 예산
        "press_release": 1.0  # 보도자료
    }
    type_weight = type_weights.get(policy_type, 1.0)

    # 최종 점수
    final_score = keyword_score * authority_weight * type_weight

    # 등급 산정
    if final_score >= 15:
        grade, label, action = 5, "매우 높음", "즉시 검토 필요"
    elif final_score >= 10:
        grade, label, action = 4, "높음", "주간 리뷰에 포함"
    elif final_score >= 5:
        grade, label, action = 3, "보통", "월간 리뷰에 포함"
    elif final_score >= 2:
        grade, label, action = 2, "낮음", "참고용 보관"
    else:
        grade, label, action = 1, "매우 낮음", "스킵 가능"

    return RelevanceResult(
        total_score=round(final_score, 2),
        grade=grade,
        label=label,
        action=action,
        matched_keywords=matched,
        category_scores=category_scores
    )


# =============================================================================
# 4. 기술 Radar 분류
# =============================================================================

class TechRing(str, Enum):
    ADOPT = "adopt"
    TRIAL = "trial"
    ASSESS = "assess"
    HOLD = "hold"


@dataclass
class TechClassificationResult:
    ring: TechRing
    score: float
    reason: str
    factors: Dict[str, float]


def classify_tech_ring(
    maturity_score: float,
    adoption_rate: float,
    our_experience: float,
    strategic_fit: float,
    risk_level: float
) -> TechClassificationResult:
    """
    기술 Ring 분류

    ADOPT: 성숙 + 도입률 높음 + 경험 있음 + 전략 적합 + 리스크 낮음
    TRIAL: 성숙도 중간 + 전략 적합 + 경험 쌓는 중
    ASSESS: 신기술 + 가능성 있음 + 평가 필요
    HOLD: 리스크 높음 OR 전략 부적합
    """
    # 종합 점수 (0-1)
    positive_score = (
        maturity_score * 0.25 +
        adoption_rate * 0.20 +
        our_experience * 0.20 +
        strategic_fit * 0.25 +
        (1 - risk_level) * 0.10
    )

    factors = {
        "maturity": maturity_score,
        "adoption": adoption_rate,
        "experience": our_experience,
        "strategic_fit": strategic_fit,
        "risk": risk_level
    }

    # Ring 결정
    if positive_score >= 0.75 and risk_level < 0.3:
        ring = TechRing.ADOPT
        reason = "성숙하고 검증된 기술, 적극 도입 권장"
    elif positive_score >= 0.55 and strategic_fit >= 0.6:
        ring = TechRing.TRIAL
        reason = "가능성 있음, 파일럿 프로젝트로 검증 필요"
    elif strategic_fit >= 0.4 and maturity_score < 0.5:
        ring = TechRing.ASSESS
        reason = "신기술, 지속적 모니터링 및 평가 필요"
    else:
        ring = TechRing.HOLD
        reason = "현재 도입 부적합, 상황 변화 시 재검토"

    return TechClassificationResult(
        ring=ring,
        score=round(positive_score, 3),
        reason=reason,
        factors=factors
    )


# =============================================================================
# 5. 경쟁사 분석
# =============================================================================

@dataclass
class CompetitiveScoreResult:
    our_score: float
    competitor_scores: Dict[str, float]
    differentiators: List[str]
    gaps: List[Dict]


def calculate_competitive_score(
    our_features: Dict[str, int],  # {feature_name: score (0-2)}
    competitor_features: Dict[str, Dict[str, int]],  # {competitor: {feature: score}}
    feature_weights: Dict[str, float],  # {feature: weight}
    differentiator_features: List[str]
) -> CompetitiveScoreResult:
    """
    경쟁력 점수 계산
    """
    # 최대 가능 점수
    max_score = sum(w * 2 for w in feature_weights.values())

    # 우리 점수
    our_weighted = sum(
        our_features.get(f, 0) * feature_weights.get(f, 1.0)
        for f in feature_weights.keys()
    )
    our_normalized = (our_weighted / max_score) * 100 if max_score > 0 else 0

    # 경쟁사 점수
    competitor_scores = {}
    for comp, features in competitor_features.items():
        comp_weighted = sum(
            features.get(f, 0) * feature_weights.get(f, 1.0)
            for f in feature_weights.keys()
        )
        competitor_scores[comp] = round((comp_weighted / max_score) * 100, 1) if max_score > 0 else 0

    # 차별화 요소
    differentiators = []
    for feature in differentiator_features:
        our_score = our_features.get(feature, 0)
        is_differentiator = all(
            our_score > comp_features.get(feature, 0)
            for comp_features in competitor_features.values()
        )
        if is_differentiator and our_score > 0:
            differentiators.append(feature)

    # 격차 (우리가 뒤처진 곳)
    gaps = []
    for feature, weight in feature_weights.items():
        our_score = our_features.get(feature, 0)
        for comp, features in competitor_features.items():
            comp_score = features.get(feature, 0)
            if comp_score > our_score:
                gaps.append({
                    "feature": feature,
                    "competitor": comp,
                    "gap": comp_score - our_score,
                    "weight": weight
                })

    gaps.sort(key=lambda x: x["gap"] * x["weight"], reverse=True)

    return CompetitiveScoreResult(
        our_score=round(our_normalized, 1),
        competitor_scores=competitor_scores,
        differentiators=differentiators,
        gaps=gaps[:5]  # Top 5 gaps
    )


# =============================================================================
# 6. 이해관계자 분석
# =============================================================================

class StakeholderStrategy(str, Enum):
    MANAGE_CLOSELY = "manage_closely"
    KEEP_SATISFIED = "keep_satisfied"
    KEEP_INFORMED = "keep_informed"
    MONITOR = "monitor"


@dataclass
class StakeholderClassificationResult:
    strategy: StakeholderStrategy
    priority: int
    actions: List[str]


def classify_stakeholder(
    power_level: int,
    interest_level: int,
    has_budget: bool = False,
    has_decision_power: bool = False
) -> StakeholderClassificationResult:
    """
    Power-Interest Grid 기반 이해관계자 분류
    """
    # Power/Interest 높음 기준: 3 이상
    high_power = power_level >= 3
    high_interest = interest_level >= 3

    # 예산/의사결정권 보유 시 power 보정
    if has_budget or has_decision_power:
        high_power = True

    if high_power and high_interest:
        return StakeholderClassificationResult(
            strategy=StakeholderStrategy.MANAGE_CLOSELY,
            priority=1,
            actions=[
                "정기 미팅 설정 (월 1회 이상)",
                "의사결정에 적극 참여 유도",
                "맞춤형 커뮤니케이션 제공",
                "핵심 정보 우선 공유"
            ]
        )
    elif high_power and not high_interest:
        return StakeholderClassificationResult(
            strategy=StakeholderStrategy.KEEP_SATISFIED,
            priority=2,
            actions=[
                "주요 마일스톤 보고",
                "이슈 발생 시 즉시 공유",
                "관심 유발 전략 수립",
                "간결한 executive summary 제공"
            ]
        )
    elif not high_power and high_interest:
        return StakeholderClassificationResult(
            strategy=StakeholderStrategy.KEEP_INFORMED,
            priority=3,
            actions=[
                "정기 뉴스레터 발송",
                "피드백 채널 제공",
                "서포터/앰배서더로 활용",
                "레퍼런스 확보"
            ]
        )
    else:
        return StakeholderClassificationResult(
            strategy=StakeholderStrategy.MONITOR,
            priority=4,
            actions=[
                "최소 커뮤니케이션 유지",
                "상황 변화 모니터링",
                "필요시 재분류"
            ]
        )


# =============================================================================
# 7. Timing Score 계산
# =============================================================================

class TimingGrade(str, Enum):
    PERFECT = "perfect"
    GOOD = "good"
    MODERATE = "moderate"
    WAIT = "wait"


@dataclass
class TimingScoreResult:
    total_score: float
    grade: TimingGrade
    message: str
    factor_scores: List[Dict]


def calculate_timing_score(
    factors: List[Dict],
    reference_date: Optional[date] = None
) -> TimingScoreResult:
    """
    Timing Score 계산

    factors: [
        {
            "id": str,
            "name": str,
            "category": str,
            "maturity_level": float (0-1),
            "impact_score": float (0-1),
            "confidence": float (0-1),
            "trend_direction": str,
            "window_start": date,
            "window_peak": date,
            "window_end": date
        }
    ]
    """
    if reference_date is None:
        reference_date = date.today()

    factor_scores = []

    for f in factors:
        # 기회 창 내 위치 점수
        window_start = f.get("window_start")
        window_peak = f.get("window_peak")
        window_end = f.get("window_end")

        if window_start and window_end:
            if reference_date < window_start:
                position_score = 0.3  # 아직 이름
                position = "before"
            elif reference_date > window_end:
                position_score = 0.2  # 이미 지남
                position = "after"
            else:
                # 정점까지의 거리 기반
                total_window = (window_end - window_start).days
                if window_peak and reference_date <= window_peak:
                    days_to_peak = (window_peak - reference_date).days
                    position_score = 0.7 + (0.3 * (1 - days_to_peak / max(total_window, 1)))
                else:
                    position_score = 0.6
                position = "in_window"
        else:
            position_score = 0.5
            position = "unknown"

        # Factor 점수
        maturity = f.get("maturity_level", 0.5)
        impact = f.get("impact_score", 0.5)
        confidence = f.get("confidence", 0.5)

        score = (
            position_score * 0.3 +
            maturity * 0.25 +
            impact * 0.25 +
            confidence * 0.2
        )

        # 트렌드 보정
        trend = f.get("trend_direction", "stable")
        if trend == "accelerating":
            score *= 1.1
        elif trend == "decelerating":
            score *= 0.9

        factor_scores.append({
            "factor_id": f.get("id"),
            "name": f.get("name"),
            "category": f.get("category"),
            "score": round(min(score, 1.0), 3),
            "position": position
        })

    # 종합 점수
    total_score = sum(fs["score"] for fs in factor_scores) / len(factor_scores) if factor_scores else 0

    # 등급
    if total_score >= 0.8:
        grade = TimingGrade.PERFECT
        message = "지금이 최적의 타이밍 - 즉시 실행 권장"
    elif total_score >= 0.6:
        grade = TimingGrade.GOOD
        message = "좋은 타이밍 - 실행 권장"
    elif total_score >= 0.4:
        grade = TimingGrade.MODERATE
        message = "보통 타이밍 - 조건부 진행 가능"
    else:
        grade = TimingGrade.WAIT
        message = "타이밍 재고 필요 - 준비 기간 확보"

    return TimingScoreResult(
        total_score=round(total_score, 2),
        grade=grade,
        message=message,
        factor_scores=factor_scores
    )


def generate_timing_thesis(
    product_name: str,
    industry_name: str,
    factors: List[Dict]
) -> Dict:
    """
    Timing Thesis 문장 생성

    Returns:
    {
        "thesis_statement": str,
        "supporting_points": List[Dict],
        "one_liner": str
    }
    """
    # 카테고리별 상위 Factor
    categorized = {}
    for f in factors:
        cat = f.get("category", "general")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(f)

    # 상위 Factor 추출
    top_factors = []
    for cat, items in categorized.items():
        sorted_items = sorted(items, key=lambda x: x.get("impact_score", 0), reverse=True)
        if sorted_items:
            top_factors.append(sorted_items[0])

    # Thesis 조각 생성
    thesis_parts = []
    for f in sorted(top_factors, key=lambda x: x.get("impact_score", 0), reverse=True)[:3]:
        cat = f.get("category", "")
        name = f.get("name", "")

        if cat == "technology":
            thesis_parts.append(f"{name}의 성숙")
        elif cat == "policy":
            thesis_parts.append(f"{name}으로 인한 제도적 기반 마련")
        elif cat == "market":
            thesis_parts.append(f"{name}")
        elif cat == "social":
            thesis_parts.append(f"{name}에 대한 사회적 인식 변화")
        else:
            thesis_parts.append(name)

    # 문장 조합
    if len(thesis_parts) >= 3:
        reasons = f"{thesis_parts[0]}, {thesis_parts[1]}, 그리고 {thesis_parts[2]}"
    elif len(thesis_parts) == 2:
        reasons = f"{thesis_parts[0]}과(와) {thesis_parts[1]}"
    elif len(thesis_parts) == 1:
        reasons = thesis_parts[0]
    else:
        reasons = "여러 요인의 동시 성숙"

    thesis = f"{industry_name} 시장은 예전에도 존재했지만, {product_name}이(가) 지금에서야 가능해진 이유는 {reasons} 때문입니다."

    # Supporting points
    supporting = []
    for f in top_factors[:3]:
        supporting.append({
            "factor": f.get("name"),
            "category": f.get("category"),
            "current_state": f.get("current_state", ""),
            "trend": f.get("trend_direction", "stable")
        })

    # One-liner
    keywords = " + ".join([f.get("name", "") for f in top_factors[:3]])
    one_liner = f"{keywords} = 지금이 최적의 타이밍"

    return {
        "thesis_statement": thesis,
        "supporting_points": supporting,
        "one_liner": one_liner
    }


# =============================================================================
# 8. Dashboard Health Score
# =============================================================================

@dataclass
class HealthScoreResult:
    total_score: float
    grade: str
    status: str
    breakdown: Dict[str, float]
    recommendations: List[str]


def calculate_dashboard_health(
    market_data: Optional[Dict] = None,
    policy_count: int = 0,
    competitor_count: int = 0,
    stakeholder_coverage: float = 0,
    timing_score: float = 0
) -> HealthScoreResult:
    """
    대시보드 Health Score 계산
    """
    # 시장 명확도
    market_clarity = 0
    if market_data:
        if market_data.get("tam"):
            market_clarity += 30
        if market_data.get("sam"):
            market_clarity += 30
        if market_data.get("som"):
            market_clarity += 20
        if market_data.get("growth_rationale"):
            market_clarity += 20

    # 정책 트래킹
    policy_tracking = min(100, policy_count * 10)

    # 경쟁 인식
    competitive_awareness = min(100, competitor_count * 15)

    # 이해관계자 매핑
    stakeholder_mapping = stakeholder_coverage * 100

    # 타이밍 준비도
    timing_readiness = timing_score * 100

    breakdown = {
        "market_clarity": market_clarity,
        "policy_tracking": policy_tracking,
        "competitive_awareness": competitive_awareness,
        "stakeholder_mapping": stakeholder_mapping,
        "timing_readiness": timing_readiness
    }

    # 가중 평균
    weights = {
        "market_clarity": 0.25,
        "policy_tracking": 0.15,
        "competitive_awareness": 0.20,
        "stakeholder_mapping": 0.15,
        "timing_readiness": 0.25
    }

    total = sum(breakdown[k] * weights[k] for k in breakdown)

    # 등급
    if total >= 80:
        grade, status = "A", "투자자 미팅 준비 완료"
    elif total >= 60:
        grade, status = "B", "대부분 준비됨, 일부 보완 필요"
    elif total >= 40:
        grade, status = "C", "기본 준비됨, 추가 분석 필요"
    else:
        grade, status = "D", "준비 부족, 집중 보완 필요"

    # 권고사항
    recommendations = []
    if market_clarity < 70:
        recommendations.append("시장 규모(TAM/SAM/SOM) 근거 자료 보강 필요")
    if policy_tracking < 50:
        recommendations.append("관련 정책 모니터링 확대 필요")
    if competitive_awareness < 50:
        recommendations.append("경쟁사 분석 및 차별화 포인트 명확화 필요")
    if stakeholder_mapping < 50:
        recommendations.append("핵심 이해관계자 파악 및 관계 구축 필요")
    if timing_readiness < 50:
        recommendations.append("'왜 지금인가' 논리 강화 필요")

    if not recommendations:
        recommendations.append("현재 상태 양호, 유지 관리 권장")

    return HealthScoreResult(
        total_score=round(total, 1),
        grade=grade,
        status=status,
        breakdown=breakdown,
        recommendations=recommendations
    )
