# CEO 전략 분석 도구 - 알고리즘 상세 명세

> Cursor AI 개발용 알고리즘 레퍼런스

---

## 1. 시장 규모 계산 (TAM/SAM/SOM)

### 1.1 개념 정의

```
TAM (Total Addressable Market): 전체 시장 규모
SAM (Serviceable Addressable Market): 접근 가능한 시장
SOM (Serviceable Obtainable Market): 실제 획득 가능한 시장
```

### 1.2 계산 알고리즘

#### Top-Down 방식

```python
def calculate_tam_topdown(
    total_infrastructure_budget: float,  # 전체 인프라 예산 (억원)
    safety_allocation_ratio: float,      # 안전 분야 배분 비율 (0.0-1.0)
    tunnel_road_ratio: float             # 터널/도로 비율 (0.0-1.0)
) -> float:
    """
    TAM = 전체 인프라 예산 × 안전 분야 비율 × 터널/도로 비율

    예시:
    - 전체 인프라 예산: 50조원
    - 안전 분야 비율: 5%
    - 터널/도로 비율: 30%
    - TAM = 500,000억 × 0.05 × 0.30 = 7,500억원
    """
    tam = total_infrastructure_budget * safety_allocation_ratio * tunnel_road_ratio
    return tam


def calculate_sam(
    tam: float,
    technology_applicable_ratio: float,  # 우리 기술 적용 가능 비율
    region_focus_ratio: float            # 타겟 지역 비율 (국내/특정 지역)
) -> float:
    """
    SAM = TAM × 기술 적용 가능 비율 × 지역 집중 비율

    예시:
    - TAM: 7,500억원
    - 기술 적용 가능: 40% (직광 위험 해당 터널)
    - 지역 집중: 100% (국내 전체)
    - SAM = 7,500 × 0.40 × 1.0 = 3,000억원
    """
    sam = tam * technology_applicable_ratio * region_focus_ratio
    return sam


def calculate_som(
    sam: float,
    market_share_target: float,          # 목표 시장 점유율
    time_horizon_years: int,             # 목표 달성 기간
    yearly_penetration_rate: float       # 연간 시장 침투율
) -> float:
    """
    SOM = SAM × 목표 점유율 × (1 - (1-침투율)^기간)

    예시:
    - SAM: 3,000억원
    - 목표 점유율: 10%
    - 기간: 5년
    - 연간 침투율: 30%
    - SOM = 3,000 × 0.10 × (1 - 0.7^5) = 약 250억원
    """
    penetration_factor = 1 - ((1 - yearly_penetration_rate) ** time_horizon_years)
    som = sam * market_share_target * penetration_factor
    return som
```

#### Bottom-Up 방식

```python
def calculate_tam_bottomup(
    total_tunnels: int,                  # 전체 터널 수
    avg_contract_value: float,           # 평균 계약 단가 (억원)
    replacement_cycle_years: int         # 교체 주기 (년)
) -> float:
    """
    TAM = (전체 터널 수 × 평균 단가) / 교체 주기

    예시:
    - 전체 터널: 2,000개
    - 평균 단가: 5억원
    - 교체 주기: 10년
    - TAM = (2,000 × 5) / 10 = 1,000억원/년
    """
    tam = (total_tunnels * avg_contract_value) / replacement_cycle_years
    return tam


def calculate_som_bottomup(
    target_customers: int,               # 목표 고객 수
    avg_deal_size: float,                # 평균 거래 규모
    win_rate: float,                     # 수주 확률
    deals_per_year: int                  # 연간 거래 기회
) -> float:
    """
    SOM = 목표 고객 × 평균 거래 × 수주율 × 연간 기회

    예시:
    - 목표 고객: 50개 (도로공사, 지자체 등)
    - 평균 거래: 3억원
    - 수주율: 20%
    - 연간 기회: 2회
    - SOM = 50 × 3 × 0.2 × 2 = 60억원/년
    """
    som = target_customers * avg_deal_size * win_rate * deals_per_year
    return som
```

### 1.3 성장률 예측

```python
def calculate_cagr(
    start_value: float,
    end_value: float,
    years: int
) -> float:
    """
    CAGR (연평균 성장률) = (최종값/초기값)^(1/기간) - 1
    """
    if start_value <= 0 or years <= 0:
        return 0.0
    cagr = (end_value / start_value) ** (1 / years) - 1
    return cagr


def project_market_size(
    current_size: float,
    cagr: float,
    years: int
) -> list[float]:
    """
    연도별 시장 규모 예측
    """
    projections = []
    for year in range(years + 1):
        projected = current_size * ((1 + cagr) ** year)
        projections.append(round(projected, 2))
    return projections
```

---

## 2. Porter's 5 Forces 분석

### 2.1 점수 체계

```python
from enum import Enum
from dataclasses import dataclass

class ForceLevel(Enum):
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5


@dataclass
class FiveForces:
    supplier_power: int          # 공급자 교섭력 (1-5)
    buyer_power: int             # 구매자 교섭력 (1-5)
    competitive_rivalry: int     # 기존 경쟁 강도 (1-5)
    threat_of_substitution: int  # 대체재 위협 (1-5)
    threat_of_new_entry: int     # 신규 진입 위협 (1-5)
```

### 2.2 각 Force 평가 기준

```python
def evaluate_supplier_power(
    num_suppliers: int,              # 공급자 수
    switching_cost: float,           # 전환 비용 (0-1)
    supplier_concentration: float,   # 공급자 집중도 (0-1)
    input_importance: float          # 투입물 중요도 (0-1)
) -> int:
    """
    공급자 교섭력 점수 계산

    점수 = (전환비용 + 집중도 + 중요도) / 3 × 5
    공급자 수가 적을수록 +1 보정
    """
    base_score = (switching_cost + supplier_concentration + input_importance) / 3 * 5

    # 공급자 수 보정
    if num_suppliers < 3:
        base_score += 1
    elif num_suppliers > 10:
        base_score -= 1

    return max(1, min(5, round(base_score)))


def evaluate_buyer_power(
    num_buyers: int,                 # 구매자 수
    buyer_concentration: float,      # 구매자 집중도 (0-1)
    price_sensitivity: float,        # 가격 민감도 (0-1)
    switching_cost: float,           # 전환 비용 (0-1, 높으면 buyer power 낮음)
    product_differentiation: float   # 제품 차별화 (0-1, 높으면 buyer power 낮음)
) -> int:
    """
    구매자 교섭력 점수 계산

    점수 = (집중도 + 가격민감도 + (1-전환비용) + (1-차별화)) / 4 × 5
    """
    score = (
        buyer_concentration +
        price_sensitivity +
        (1 - switching_cost) +
        (1 - product_differentiation)
    ) / 4 * 5

    return max(1, min(5, round(score)))


def evaluate_competitive_rivalry(
    num_competitors: int,            # 경쟁자 수
    industry_growth: float,          # 산업 성장률 (-1 to 1)
    fixed_costs_ratio: float,        # 고정비 비율 (0-1)
    product_differentiation: float,  # 제품 차별화 (0-1)
    exit_barriers: float             # 퇴출 장벽 (0-1)
) -> int:
    """
    경쟁 강도 점수 계산

    경쟁자 많고, 성장 느리고, 고정비 높고, 차별화 낮고, 퇴출 어려우면 = 높은 점수
    """
    # 성장률 역변환 (성장 느리면 경쟁 심함)
    growth_factor = 1 - (industry_growth + 1) / 2  # -1~1 -> 1~0

    score = (
        min(num_competitors / 10, 1) +  # 경쟁자 수 (10개 이상이면 만점)
        growth_factor +
        fixed_costs_ratio +
        (1 - product_differentiation) +
        exit_barriers
    ) / 5 * 5

    return max(1, min(5, round(score)))


def evaluate_substitution_threat(
    num_substitutes: int,            # 대체재 수
    substitute_performance: float,   # 대체재 성능 (0-1)
    switching_cost: float,           # 전환 비용 (0-1)
    price_performance_ratio: float   # 대체재 가성비 (0-1)
) -> int:
    """
    대체재 위협 점수 계산
    """
    if num_substitutes == 0:
        return 1

    score = (
        min(num_substitutes / 5, 1) +
        substitute_performance +
        (1 - switching_cost) +
        price_performance_ratio
    ) / 4 * 5

    return max(1, min(5, round(score)))


def evaluate_new_entry_threat(
    capital_requirements: float,     # 필요 자본 (0-1, 높으면 진입 어려움)
    economies_of_scale: float,       # 규모의 경제 (0-1, 높으면 진입 어려움)
    brand_loyalty: float,            # 브랜드 충성도 (0-1, 높으면 진입 어려움)
    regulatory_barriers: float,      # 규제 장벽 (0-1, 높으면 진입 어려움)
    access_to_distribution: float    # 유통 접근성 (0-1, 낮으면 진입 어려움)
) -> int:
    """
    신규 진입 위협 점수 계산

    진입 장벽이 높으면 = 낮은 점수 (위협 낮음)
    """
    barriers = (
        capital_requirements +
        economies_of_scale +
        brand_loyalty +
        regulatory_barriers +
        (1 - access_to_distribution)
    ) / 5

    # 장벽 높으면 위협 낮음
    score = (1 - barriers) * 5

    return max(1, min(5, round(score)))
```

### 2.3 산업 매력도 종합 점수

```python
def calculate_industry_attractiveness(forces: FiveForces) -> dict:
    """
    산업 매력도 계산

    매력도 = 25 - (5개 Force 합계)
    범위: 0 (최악) ~ 20 (최고)
    """
    total_forces = (
        forces.supplier_power +
        forces.buyer_power +
        forces.competitive_rivalry +
        forces.threat_of_substitution +
        forces.threat_of_new_entry
    )

    attractiveness = 25 - total_forces

    # 등급 산정
    if attractiveness >= 16:
        grade = "A"
        interpretation = "매우 매력적인 산업"
    elif attractiveness >= 12:
        grade = "B"
        interpretation = "매력적인 산업"
    elif attractiveness >= 8:
        grade = "C"
        interpretation = "보통 산업"
    elif attractiveness >= 4:
        grade = "D"
        interpretation = "매력도 낮은 산업"
    else:
        grade = "E"
        interpretation = "진입 비추천 산업"

    return {
        "total_forces": total_forces,
        "attractiveness_score": attractiveness,
        "grade": grade,
        "interpretation": interpretation,
        "max_score": 20
    }
```

---

## 3. 정책 연관성 점수 (Policy Relevance Score)

### 3.1 키워드 매칭 알고리즘

```python
from typing import List, Dict
import re

# 핵심 키워드 카테고리
KEYWORD_CATEGORIES = {
    "direct": {  # 직접 연관 (가중치 높음)
        "keywords": ["터널", "도로안전", "직광", "눈부심", "glare", "교통안전시설"],
        "weight": 3.0
    },
    "infrastructure": {  # 인프라 관련
        "keywords": ["스마트도로", "스마트인프라", "도로시설", "교통시설", "ITS"],
        "weight": 2.0
    },
    "safety": {  # 안전 일반
        "keywords": ["안전", "사고예방", "재해", "위험", "모니터링"],
        "weight": 1.5
    },
    "technology": {  # 기술 관련
        "keywords": ["AI", "인공지능", "센서", "IoT", "디지털트윈"],
        "weight": 1.0
    },
    "budget": {  # 예산 관련
        "keywords": ["예산", "투자", "R&D", "연구개발", "지원사업"],
        "weight": 1.0
    }
}


def calculate_keyword_score(
    text: str,
    custom_keywords: List[str] = None
) -> Dict:
    """
    정책 문서의 키워드 매칭 점수 계산

    Returns:
        {
            "total_score": float,
            "matched_keywords": List[str],
            "category_scores": Dict[str, float]
        }
    """
    text_lower = text.lower()
    matched = []
    category_scores = {}

    for category, config in KEYWORD_CATEGORIES.items():
        category_score = 0
        for keyword in config["keywords"]:
            # 키워드 출현 횟수
            count = len(re.findall(keyword.lower(), text_lower))
            if count > 0:
                matched.append(keyword)
                # 로그 스케일로 반복 출현 효과 감소
                category_score += config["weight"] * (1 + 0.5 * min(count - 1, 3))

        category_scores[category] = round(category_score, 2)

    # 커스텀 키워드 처리
    if custom_keywords:
        custom_score = 0
        for keyword in custom_keywords:
            if keyword.lower() in text_lower:
                matched.append(f"[custom]{keyword}")
                custom_score += 2.0
        category_scores["custom"] = custom_score

    total_score = sum(category_scores.values())

    return {
        "total_score": round(total_score, 2),
        "matched_keywords": list(set(matched)),
        "category_scores": category_scores
    }
```

### 3.2 연관성 등급 산정

```python
def calculate_relevance_grade(
    keyword_score: float,
    source_authority: str,    # "국토부", "행안부", "지자체", "기타"
    policy_type: str          # "법령", "계획", "예산", "보도자료"
) -> Dict:
    """
    연관성 등급 산정
    """
    # 출처 가중치
    authority_weights = {
        "국토부": 1.5,
        "행안부": 1.3,
        "과기부": 1.2,
        "지자체": 1.0,
        "기타": 0.8
    }

    # 정책 유형 가중치
    type_weights = {
        "법령": 2.0,      # 법적 구속력
        "계획": 1.5,      # 중장기 계획
        "예산": 1.8,      # 예산 배정
        "보도자료": 1.0   # 일반 공지
    }

    authority_weight = authority_weights.get(source_authority, 0.8)
    type_weight = type_weights.get(policy_type, 1.0)

    final_score = keyword_score * authority_weight * type_weight

    # 등급 산정 (1-5)
    if final_score >= 15:
        grade = 5
        label = "매우 높음"
        action = "즉시 검토 필요"
    elif final_score >= 10:
        grade = 4
        label = "높음"
        action = "주간 리뷰에 포함"
    elif final_score >= 5:
        grade = 3
        label = "보통"
        action = "월간 리뷰에 포함"
    elif final_score >= 2:
        grade = 2
        label = "낮음"
        action = "참고용 보관"
    else:
        grade = 1
        label = "매우 낮음"
        action = "스킵 가능"

    return {
        "final_score": round(final_score, 2),
        "grade": grade,
        "label": label,
        "action": action,
        "factors": {
            "keyword_score": keyword_score,
            "authority_weight": authority_weight,
            "type_weight": type_weight
        }
    }
```

### 3.3 AI 요약 프롬프트

```python
POLICY_SUMMARY_PROMPT = """
다음 정책 문서를 분석하고 아래 형식으로 요약해주세요:

[정책 문서]
{document_text}

[출력 형식]
1. 핵심 내용 (2-3문장)
2. 우리 사업(터널/도로 안전 기술)과의 연관성
3. 기회 요인
4. 주의할 점
5. 권장 액션

JSON 형식으로 출력:
{{
    "summary": "핵심 내용",
    "relevance": "연관성 설명",
    "opportunities": ["기회1", "기회2"],
    "risks": ["주의점1"],
    "actions": ["액션1", "액션2"]
}}
"""
```

---

## 4. Technology Radar 분류 알고리즘

### 4.1 4분면(Quadrant) 정의

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class TechQuadrant(Enum):
    TECHNIQUES = "techniques"      # 기법/방법론
    TOOLS = "tools"                # 도구
    PLATFORMS = "platforms"        # 플랫폼
    LANGUAGES = "languages"        # 언어/프레임워크


class TechRing(Enum):
    ADOPT = "adopt"       # 적극 도입
    TRIAL = "trial"       # 시범 적용
    ASSESS = "assess"     # 평가 중
    HOLD = "hold"         # 보류/주의


@dataclass
class TechItem:
    name: str
    quadrant: TechQuadrant
    ring: TechRing
    description: str
    is_new: bool = False  # 이번에 새로 추가/변경됨
```

### 4.2 Ring 분류 기준 알고리즘

```python
def classify_tech_ring(
    maturity_score: float,        # 기술 성숙도 (0-1)
    adoption_rate: float,         # 시장 도입률 (0-1)
    our_experience: float,        # 우리 팀 경험 (0-1)
    strategic_fit: float,         # 전략적 적합성 (0-1)
    risk_level: float             # 리스크 수준 (0-1, 높으면 위험)
) -> Dict:
    """
    기술을 어느 Ring에 배치할지 결정

    ADOPT: 성숙 + 도입률 높음 + 경험 있음 + 전략 적합 + 리스크 낮음
    TRIAL: 성숙도 중간 + 전략 적합 + 경험 쌓는 중
    ASSESS: 신기술 + 가능성 있음 + 평가 필요
    HOLD: 리스크 높음 OR 전략 부적합 OR 대체재 존재
    """

    # 종합 점수 계산
    positive_score = (
        maturity_score * 0.25 +
        adoption_rate * 0.20 +
        our_experience * 0.20 +
        strategic_fit * 0.25 +
        (1 - risk_level) * 0.10
    )

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

    return {
        "ring": ring.value,
        "score": round(positive_score, 2),
        "reason": reason,
        "factors": {
            "maturity": maturity_score,
            "adoption": adoption_rate,
            "experience": our_experience,
            "strategic_fit": strategic_fit,
            "risk": risk_level
        }
    }
```

### 4.3 대체 가능성 평가

```python
def evaluate_replaceability(
    is_commodity: bool,           # 범용 기술인가
    proprietary_data: bool,       # 독자 데이터 필요한가
    integration_depth: float,     # 시스템 통합 깊이 (0-1)
    learning_curve: float,        # 학습 곡선 (0-1, 높으면 어려움)
    vendor_lock_in: float         # 벤더 종속성 (0-1)
) -> Dict:
    """
    기술의 대체 가능성 평가

    대체 어려움 = 독자 데이터 + 깊은 통합 + 높은 학습곡선 + 벤더 종속
    """

    replaceability_score = (
        (1 if is_commodity else 0) * 0.3 +
        (0 if proprietary_data else 1) * 0.25 +
        (1 - integration_depth) * 0.2 +
        (1 - learning_curve) * 0.15 +
        (1 - vendor_lock_in) * 0.1
    )

    if replaceability_score >= 0.7:
        level = "HIGH"
        warning = "쉽게 대체 가능, 차별화 전략 필요"
    elif replaceability_score >= 0.4:
        level = "MEDIUM"
        warning = "부분적 대체 가능, 전환 비용 존재"
    else:
        level = "LOW"
        warning = "대체 어려움, 경쟁 우위 요소"

    return {
        "replaceability": level,
        "score": round(replaceability_score, 2),
        "warning": warning
    }
```

---

## 5. 경쟁사 분석 알고리즘

### 5.1 기능 비교 매트릭스

```python
from typing import List, Dict

@dataclass
class FeatureComparison:
    feature_name: str
    our_score: int           # 0: 없음, 1: 부분, 2: 완전
    competitor_scores: Dict[str, int]  # {경쟁사명: 점수}
    weight: float            # 중요도 가중치 (0-1)
    is_differentiator: bool  # 차별화 요소인가


def calculate_competitive_score(
    features: List[FeatureComparison]
) -> Dict:
    """
    경쟁력 점수 계산
    """
    our_total = 0
    competitor_totals = {}
    weight_sum = 0

    differentiators = []
    gaps = []

    for f in features:
        weight_sum += f.weight
        our_weighted = f.our_score * f.weight
        our_total += our_weighted

        for comp_name, comp_score in f.competitor_scores.items():
            if comp_name not in competitor_totals:
                competitor_totals[comp_name] = 0
            competitor_totals[comp_name] += comp_score * f.weight

            # 차별화 요소 식별
            if f.our_score > comp_score and f.is_differentiator:
                differentiators.append(f.feature_name)

            # 격차 식별 (우리가 뒤처짐)
            if f.our_score < comp_score:
                gaps.append({
                    "feature": f.feature_name,
                    "competitor": comp_name,
                    "gap": comp_score - f.our_score
                })

    # 정규화 (0-100)
    max_possible = weight_sum * 2  # 최대 점수
    our_normalized = (our_total / max_possible) * 100 if max_possible > 0 else 0

    competitor_normalized = {
        name: (score / max_possible) * 100
        for name, score in competitor_totals.items()
    }

    return {
        "our_score": round(our_normalized, 1),
        "competitor_scores": {k: round(v, 1) for k, v in competitor_normalized.items()},
        "differentiators": differentiators,
        "gaps": sorted(gaps, key=lambda x: x["gap"], reverse=True)[:5],
        "feature_count": len(features)
    }
```

### 5.2 포지셔닝 맵 좌표 계산

```python
def calculate_positioning(
    competitors: List[Dict],
    x_axis: str,              # "price", "technology", "coverage" 등
    y_axis: str               # "quality", "innovation", "service" 등
) -> List[Dict]:
    """
    2D 포지셔닝 맵 좌표 계산

    각 competitor dict 구조:
    {
        "name": str,
        "metrics": {
            "price": float,        # 0-1 (높을수록 고가)
            "technology": float,   # 0-1 (높을수록 고기술)
            "quality": float,      # 0-1
            "coverage": float,     # 0-1 (시장 커버리지)
            "innovation": float,   # 0-1
            "service": float       # 0-1
        }
    }
    """
    positioned = []

    for comp in competitors:
        x = comp["metrics"].get(x_axis, 0.5)
        y = comp["metrics"].get(y_axis, 0.5)

        # 0-100 스케일로 변환
        positioned.append({
            "name": comp["name"],
            "x": round(x * 100, 1),
            "y": round(y * 100, 1),
            "is_us": comp.get("is_us", False)
        })

    return positioned
```

### 5.3 유사도 계산 (Cosine Similarity)

```python
import math
from typing import List

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    두 벡터 간 코사인 유사도 계산
    """
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def find_similar_competitors(
    our_features: List[float],
    competitors: Dict[str, List[float]],
    threshold: float = 0.7
) -> List[Dict]:
    """
    우리와 유사한 경쟁사 찾기

    our_features: 우리 제품 특성 벡터
    competitors: {경쟁사명: 특성 벡터}
    threshold: 유사도 임계값
    """
    similarities = []

    for name, features in competitors.items():
        sim = cosine_similarity(our_features, features)
        similarities.append({
            "name": name,
            "similarity": round(sim, 3),
            "is_direct_competitor": sim >= threshold
        })

    return sorted(similarities, key=lambda x: x["similarity"], reverse=True)
```

---

## 6. 이해관계자 분석 알고리즘

### 6.1 Power-Interest Grid

```python
from enum import Enum
from dataclasses import dataclass
from typing import List

class StakeholderStrategy(Enum):
    MANAGE_CLOSELY = "manage_closely"       # 긴밀 관리 (높은 권력 + 높은 관심)
    KEEP_SATISFIED = "keep_satisfied"       # 만족 유지 (높은 권력 + 낮은 관심)
    KEEP_INFORMED = "keep_informed"         # 정보 제공 (낮은 권력 + 높은 관심)
    MONITOR = "monitor"                     # 모니터링 (낮은 권력 + 낮은 관심)


@dataclass
class Stakeholder:
    id: str
    name: str
    organization: str
    power: int          # 1-5
    interest: int       # 1-5
    influence: int      # 1-5 (다른 이해관계자에 대한 영향력)

    # 보유 권한
    has_budget: bool
    has_decision_power: bool
    has_data_access: bool


def classify_stakeholder(stakeholder: Stakeholder) -> Dict:
    """
    이해관계자 전략 분류
    """
    # Power-Interest 매트릭스 기준 (3을 중간점으로)
    high_power = stakeholder.power >= 3
    high_interest = stakeholder.interest >= 3

    if high_power and high_interest:
        strategy = StakeholderStrategy.MANAGE_CLOSELY
        priority = 1
        actions = [
            "정기 미팅 설정",
            "의사결정에 적극 참여 유도",
            "맞춤형 커뮤니케이션"
        ]
    elif high_power and not high_interest:
        strategy = StakeholderStrategy.KEEP_SATISFIED
        priority = 2
        actions = [
            "주요 마일스톤 보고",
            "이슈 발생 시 즉시 공유",
            "관심 유발 전략 수립"
        ]
    elif not high_power and high_interest:
        strategy = StakeholderStrategy.KEEP_INFORMED
        priority = 3
        actions = [
            "정기 뉴스레터 발송",
            "피드백 채널 제공",
            "서포터로 활용"
        ]
    else:
        strategy = StakeholderStrategy.MONITOR
        priority = 4
        actions = [
            "최소 커뮤니케이션",
            "상황 변화 모니터링"
        ]

    return {
        "strategy": strategy.value,
        "priority": priority,
        "actions": actions,
        "quadrant": f"Power={stakeholder.power}, Interest={stakeholder.interest}"
    }
```

### 6.2 영향력 네트워크 분석 (Simplified PageRank)

```python
def calculate_influence_score(
    stakeholders: List[Stakeholder],
    relationships: List[Dict]  # [{"from": id, "to": id, "weight": float}]
) -> Dict[str, float]:
    """
    간소화된 영향력 점수 계산

    실제 구현시 NetworkX의 PageRank 사용 권장
    """
    # 초기 점수 (보유 권한 기반)
    scores = {}
    for s in stakeholders:
        base_score = (
            (3 if s.has_budget else 0) +
            (3 if s.has_decision_power else 0) +
            (2 if s.has_data_access else 0) +
            s.power
        )
        scores[s.id] = base_score

    # 관계 기반 보정 (3회 반복)
    for _ in range(3):
        new_scores = scores.copy()
        for rel in relationships:
            # "to"에게 "from"의 영향력 전파
            transfer = scores[rel["from"]] * rel["weight"] * 0.1
            new_scores[rel["to"]] += transfer
        scores = new_scores

    # 정규화 (0-100)
    max_score = max(scores.values()) if scores else 1
    normalized = {k: round((v / max_score) * 100, 1) for k, v in scores.items()}

    return normalized
```

### 6.3 핵심 의사결정자 식별

```python
def identify_key_decision_makers(
    stakeholders: List[Stakeholder],
    influence_scores: Dict[str, float]
) -> List[Dict]:
    """
    핵심 의사결정자 식별 및 우선순위 산정
    """
    results = []

    for s in stakeholders:
        # 종합 점수 계산
        total_score = (
            s.power * 2 +
            s.influence * 1.5 +
            (influence_scores.get(s.id, 0) / 100) * 3 +
            (5 if s.has_budget else 0) +
            (5 if s.has_decision_power else 0)
        )

        results.append({
            "id": s.id,
            "name": s.name,
            "organization": s.organization,
            "total_score": round(total_score, 1),
            "is_key_decision_maker": s.has_budget or s.has_decision_power,
            "influence_rank": influence_scores.get(s.id, 0)
        })

    # 점수 순 정렬
    return sorted(results, key=lambda x: x["total_score"], reverse=True)
```

---

## 7. Timing Thesis 생성 알고리즘

### 7.1 Timing Factor 모델

```python
from enum import Enum
from dataclasses import dataclass
from typing import List
from datetime import date

class FactorCategory(Enum):
    TECHNOLOGY = "technology"     # 기술 성숙
    POLICY = "policy"             # 정책/규제
    MARKET = "market"             # 시장 변화
    SOCIAL = "social"             # 사회적 요인
    ECONOMIC = "economic"         # 경제적 요인


class TrendDirection(Enum):
    ACCELERATING = "accelerating"   # 가속화
    STABLE = "stable"               # 안정
    DECELERATING = "decelerating"   # 감속


@dataclass
class TimingFactor:
    id: str
    name: str
    category: FactorCategory
    description: str

    # 현재 상태
    current_state: str           # 현재 상황 설명
    trend_direction: TrendDirection
    maturity_level: float        # 0-1 (1이면 완전 성숙)

    # 타이밍 관련
    window_start: date           # 기회 창 시작
    window_peak: date            # 기회 정점
    window_end: date             # 기회 창 종료

    # 중요도
    impact_score: float          # 0-1
    confidence: float            # 0-1 (확신도)
```

### 7.2 Timing Score 계산

```python
from datetime import date, timedelta

def calculate_timing_score(
    factors: List[TimingFactor],
    reference_date: date = None
) -> Dict:
    """
    종합 타이밍 점수 계산
    """
    if reference_date is None:
        reference_date = date.today()

    factor_scores = []

    for f in factors:
        # 기회 창 내 위치 계산
        total_window = (f.window_end - f.window_start).days
        days_from_start = (reference_date - f.window_start).days
        days_to_peak = (f.window_peak - reference_date).days

        # 위치 점수 (정점에 가까울수록 높음)
        if reference_date < f.window_start:
            position_score = 0.3  # 아직 이름
        elif reference_date > f.window_end:
            position_score = 0.2  # 이미 지남
        else:
            # 정점까지의 거리 기반
            if days_to_peak > 0:
                position_score = 0.7 + (0.3 * (1 - days_to_peak / total_window))
            else:
                # 정점 지남
                days_after_peak = abs(days_to_peak)
                position_score = 1.0 - (0.5 * days_after_peak / total_window)

        # Factor 점수 = 위치 × 성숙도 × 영향도 × 확신도
        score = (
            position_score * 0.3 +
            f.maturity_level * 0.25 +
            f.impact_score * 0.25 +
            f.confidence * 0.2
        )

        # 트렌드 보정
        if f.trend_direction == TrendDirection.ACCELERATING:
            score *= 1.1
        elif f.trend_direction == TrendDirection.DECELERATING:
            score *= 0.9

        factor_scores.append({
            "factor_id": f.id,
            "name": f.name,
            "category": f.category.value,
            "score": round(score, 3),
            "position": "before" if reference_date < f.window_start
                       else "after" if reference_date > f.window_end
                       else "in_window"
        })

    # 종합 점수
    total_score = sum(fs["score"] for fs in factor_scores) / len(factor_scores) if factor_scores else 0

    # 등급 산정
    if total_score >= 0.8:
        grade = "PERFECT"
        message = "지금이 최적의 타이밍"
    elif total_score >= 0.6:
        grade = "GOOD"
        message = "좋은 타이밍, 실행 권장"
    elif total_score >= 0.4:
        grade = "MODERATE"
        message = "조건부 진행 가능"
    else:
        grade = "WAIT"
        message = "타이밍 재고 필요"

    return {
        "total_score": round(total_score, 2),
        "grade": grade,
        "message": message,
        "factor_scores": factor_scores,
        "reference_date": reference_date.isoformat()
    }
```

### 7.3 Timing Thesis 문장 생성

```python
def generate_timing_thesis(
    factors: List[TimingFactor],
    product_name: str,
    industry_name: str
) -> Dict:
    """
    Timing Thesis 문장 자동 생성

    템플릿:
    "이 산업은 예전에도 있었지만, 지금에서야 가능한 이유는 ○○ 때문이다."
    """

    # Factor별 문장 조각 생성
    tech_factors = [f for f in factors if f.category == FactorCategory.TECHNOLOGY]
    policy_factors = [f for f in factors if f.category == FactorCategory.POLICY]
    market_factors = [f for f in factors if f.category == FactorCategory.MARKET]

    thesis_parts = []

    # 기술 요인
    if tech_factors:
        top_tech = max(tech_factors, key=lambda x: x.impact_score)
        thesis_parts.append(f"{top_tech.name}의 성숙")

    # 정책 요인
    if policy_factors:
        top_policy = max(policy_factors, key=lambda x: x.impact_score)
        thesis_parts.append(f"{top_policy.name}으로 인한 제도적 기반 마련")

    # 시장 요인
    if market_factors:
        top_market = max(market_factors, key=lambda x: x.impact_score)
        thesis_parts.append(f"{top_market.name}")

    # 문장 조합
    if len(thesis_parts) >= 3:
        reasons = f"{thesis_parts[0]}, {thesis_parts[1]}, 그리고 {thesis_parts[2]}"
    elif len(thesis_parts) == 2:
        reasons = f"{thesis_parts[0]}과(와) {thesis_parts[1]}"
    elif len(thesis_parts) == 1:
        reasons = thesis_parts[0]
    else:
        reasons = "여러 요인의 동시 성숙"

    # 최종 Thesis
    thesis = f"{industry_name} 시장은 예전에도 존재했지만, {product_name}이(가) 지금에서야 가능해진 이유는 {reasons} 때문입니다."

    # 부연 설명
    supporting_points = []
    for f in sorted(factors, key=lambda x: x.impact_score, reverse=True)[:3]:
        supporting_points.append({
            "factor": f.name,
            "evidence": f.current_state,
            "trend": f.trend_direction.value
        })

    return {
        "thesis_statement": thesis,
        "supporting_points": supporting_points,
        "confidence": sum(f.confidence for f in factors) / len(factors) if factors else 0
    }
```

### 7.4 AI 기반 Thesis 생성 프롬프트

```python
TIMING_THESIS_PROMPT = """
다음 정보를 바탕으로 Timing Thesis를 작성해주세요.

[제품/서비스]
{product_name}: {product_description}

[타겟 산업]
{industry_name}

[Timing Factors]
{factors_json}

[출력 요구사항]
1. 핵심 Thesis 문장 (1문장)
   - "이 산업은 예전에도 있었지만, 지금에서야 가능한 이유는 ○○ 때문이다" 형식

2. 근거 3가지 (각 2-3문장)
   - 각 Factor별 구체적 데이터/사례 포함

3. 투자자용 한 줄 요약

4. 리스크 (타이밍이 틀릴 수 있는 이유) 1가지

JSON 형식으로 출력:
{{
    "thesis": "핵심 문장",
    "evidences": [
        {{"factor": "요인명", "explanation": "설명", "data_point": "구체적 수치/사례"}}
    ],
    "one_liner": "투자자용 한 줄",
    "risk": "리스크 설명"
}}
"""
```

---

## 8. 종합 대시보드 점수

### 8.1 CEO 대시보드 Health Score

```python
def calculate_dashboard_health(
    market_data: Dict,
    competitive_data: Dict,
    timing_data: Dict,
    policy_count: int,
    stakeholder_coverage: float
) -> Dict:
    """
    대시보드 전체 건강도 점수
    """
    scores = {
        "market_clarity": min(100, (
            (30 if market_data.get("tam") else 0) +
            (30 if market_data.get("sam") else 0) +
            (20 if market_data.get("som") else 0) +
            (20 if market_data.get("growth_rationale") else 0)
        )),
        "competitive_awareness": competitive_data.get("our_score", 0),
        "timing_readiness": timing_data.get("total_score", 0) * 100,
        "policy_tracking": min(100, policy_count * 10),  # 10개 정책 = 100점
        "stakeholder_mapping": stakeholder_coverage * 100
    }

    # 가중 평균
    weights = {
        "market_clarity": 0.25,
        "competitive_awareness": 0.20,
        "timing_readiness": 0.25,
        "policy_tracking": 0.15,
        "stakeholder_mapping": 0.15
    }

    total = sum(scores[k] * weights[k] for k in scores)

    # 등급
    if total >= 80:
        grade = "A"
        status = "투자자 미팅 준비 완료"
    elif total >= 60:
        grade = "B"
        status = "대부분 준비됨, 일부 보완 필요"
    elif total >= 40:
        grade = "C"
        status = "기본 준비됨, 추가 분석 필요"
    else:
        grade = "D"
        status = "준비 부족, 집중 보완 필요"

    return {
        "total_score": round(total, 1),
        "grade": grade,
        "status": status,
        "breakdown": scores,
        "recommendations": get_recommendations(scores)
    }


def get_recommendations(scores: Dict) -> List[str]:
    """
    점수 기반 개선 권고사항
    """
    recommendations = []

    if scores["market_clarity"] < 70:
        recommendations.append("시장 규모(TAM/SAM/SOM) 근거 자료 보강 필요")

    if scores["competitive_awareness"] < 70:
        recommendations.append("경쟁사 분석 및 차별화 포인트 명확화 필요")

    if scores["timing_readiness"] < 70:
        recommendations.append("'왜 지금인가' 논리 강화 필요")

    if scores["policy_tracking"] < 50:
        recommendations.append("관련 정책 모니터링 확대 필요")

    if scores["stakeholder_mapping"] < 50:
        recommendations.append("핵심 이해관계자 파악 및 관계 구축 필요")

    return recommendations if recommendations else ["현재 상태 양호, 유지 관리 권장"]
```

---

## 부록: 알고리즘 구현 체크리스트

| 알고리즘 | 파일 위치 | 테스트 | 상태 |
|---------|----------|--------|------|
| TAM/SAM/SOM 계산 | `services/market_service.py` | [ ] | 미구현 |
| Porter's 5 Forces | `services/industry_service.py` | [ ] | 미구현 |
| 정책 연관성 점수 | `services/policy_service.py` | [ ] | 미구현 |
| Tech Radar 분류 | `services/tech_service.py` | [ ] | 미구현 |
| 경쟁사 유사도 | `services/competitor_service.py` | [ ] | 미구현 |
| Power-Interest Grid | `services/stakeholder_service.py` | [ ] | 미구현 |
| Timing Score | `services/timing_service.py` | [ ] | 미구현 |
| Dashboard Health | `services/dashboard_service.py` | [ ] | 미구현 |
