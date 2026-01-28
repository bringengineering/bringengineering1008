"""
5개 핵심 산업 정의
CEO 전략 분석 도구의 산업별 설정

1. 건설 및 인프라 자산 관리 (Civil Engineering & Asset Management)
2. 보험 및 리스크 금융 (Insurance & Risk Finance)
3. 물류 및 공급망 관리 (Logistics & SCM)
4. AI 및 데이터 엔지니어링 (AI & Data Science)
5. 공공 행정 및 법률 (Public Affairs & Law)
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional


class IndustryCode(str, Enum):
    """산업 코드"""
    CIVIL_INFRA = "civil_infra"          # 건설 및 인프라
    INSURANCE_RISK = "insurance_risk"    # 보험 및 리스크 금융
    LOGISTICS_SCM = "logistics_scm"      # 물류 및 공급망
    AI_DATA = "ai_data"                  # AI 및 데이터 엔지니어링
    PUBLIC_LAW = "public_law"            # 공공 행정 및 법률


@dataclass
class PolicySource:
    """정책 수집 소스"""
    name: str
    org_name: str
    source_type: str  # 'rss', 'webpage', 'api'
    url: str
    crawl_frequency_minutes: int = 60


@dataclass
class IndustryKeyword:
    """산업별 키워드"""
    keyword: str
    category: str  # 'direct', 'related', 'technology', 'policy'
    weight: float = 1.0


@dataclass
class StakeholderTemplate:
    """이해관계자 템플릿"""
    role: str
    organization_type: str
    typical_power: int  # 1-5
    typical_interest: int  # 1-5
    has_budget: bool = False
    has_decision_power: bool = False


@dataclass
class IndustryProfile:
    """산업 프로필 정의"""
    code: IndustryCode
    name_ko: str
    name_en: str
    description: str

    # 핵심 개념
    core_concepts: List[str]

    # 우리 사업과의 연결점
    business_connection: str

    # 정책 소스
    policy_sources: List[PolicySource]

    # 키워드
    keywords: List[IndustryKeyword]

    # 주요 이해관계자 유형
    stakeholder_templates: List[StakeholderTemplate]

    # Porter's 5 Forces 기본값
    default_forces: Dict[str, int] = field(default_factory=dict)

    # 기술 트렌드 카테고리
    tech_categories: List[str] = field(default_factory=list)


# =============================================================================
# 5개 산업 프로필 정의
# =============================================================================

INDUSTRY_PROFILES: Dict[IndustryCode, IndustryProfile] = {

    # =========================================================================
    # 1. 건설 및 인프라 자산 관리
    # =========================================================================
    IndustryCode.CIVIL_INFRA: IndustryProfile(
        code=IndustryCode.CIVIL_INFRA,
        name_ko="건설 및 인프라 자산 관리",
        name_en="Civil Engineering & Asset Management",
        description="물리적 실체를 다루는 영역. BIM, 시설물 안전 관리, 노후 시설물 유지보수의 행정 사이클을 이해하여 데이터 수집 지점을 파악",

        core_concepts=[
            "BIM (Building Information Modeling)",
            "시설물 안전 관리 체계",
            "노후 시설물 유지보수 법령",
            "자산 생애주기 관리 (Asset Lifecycle)",
            "예방적 유지보수 (Predictive Maintenance)"
        ],

        business_connection="터널과 다리가 어떻게 지어지고 관리되는지 '행정 사이클'을 알아야 데이터를 어디서 캘지 정할 수 있음",

        policy_sources=[
            PolicySource("국토부 보도자료", "국토교통부", "rss", "https://www.molit.go.kr/RSS/portal_news.xml"),
            PolicySource("시설안전공단", "한국시설안전공단", "webpage", "https://www.kistec.or.kr"),
            PolicySource("건설기술정보시스템", "국토교통부", "api", "https://www.codil.or.kr"),
        ],

        keywords=[
            IndustryKeyword("BIM", "technology", 2.5),
            IndustryKeyword("시설물안전", "direct", 3.0),
            IndustryKeyword("노후시설", "direct", 3.0),
            IndustryKeyword("유지보수", "direct", 2.5),
            IndustryKeyword("터널", "direct", 3.0),
            IndustryKeyword("교량", "direct", 3.0),
            IndustryKeyword("정밀안전진단", "direct", 2.5),
            IndustryKeyword("디지털트윈", "technology", 2.0),
            IndustryKeyword("스마트건설", "technology", 2.0),
            IndustryKeyword("건설자동화", "technology", 1.5),
        ],

        stakeholder_templates=[
            StakeholderTemplate("시설안전 담당관", "government", 4, 5, True, True),
            StakeholderTemplate("도로정책과장", "government", 4, 4, True, True),
            StakeholderTemplate("시설관리 본부장", "agency", 5, 4, True, True),
            StakeholderTemplate("건설사 기술이사", "company", 3, 5, False, False),
            StakeholderTemplate("설계사무소 대표", "company", 2, 4, False, False),
        ],

        default_forces={
            "supplier_power": 3,
            "buyer_power": 4,  # 공공 발주처 우위
            "competitive_rivalry": 4,
            "threat_of_substitution": 2,
            "threat_of_new_entry": 2  # 높은 진입장벽
        },

        tech_categories=["BIM/CAD", "IoT 센서", "드론/로봇", "AI 진단", "디지털트윈"]
    ),

    # =========================================================================
    # 2. 보험 및 리스크 금융
    # =========================================================================
    IndustryCode.INSURANCE_RISK: IndustryProfile(
        code=IndustryCode.INSURANCE_RISK,
        name_ko="보험 및 리스크 금융",
        name_en="Insurance & Risk Finance",
        description="수집한 데이터를 '돈'의 언어로 바꾸는 '연금술'의 영역. 보험사가 손해율을 낮추기 위해 목말라 하는 데이터를 파악",

        core_concepts=[
            "지수형 보험 (Parametric Insurance)",
            "재보험 시장 구조",
            "언더라이팅 (보험 인수) 로직",
            "손해율 (Loss Ratio)",
            "리스크 프리미엄 산정"
        ],

        business_connection="보험사가 '손해율'을 낮추기 위해 어떤 데이터에 목말라 있는지 알아야 우리 점수를 돈을 받고 팔 수 있음",

        policy_sources=[
            PolicySource("금융위원회 보도자료", "금융위원회", "rss", "https://www.fsc.go.kr/rss/"),
            PolicySource("금융감독원", "금융감독원", "webpage", "https://www.fss.or.kr"),
            PolicySource("보험개발원", "보험개발원", "webpage", "https://www.kidi.or.kr"),
        ],

        keywords=[
            IndustryKeyword("지수보험", "direct", 3.0),
            IndustryKeyword("파라메트릭", "direct", 3.0),
            IndustryKeyword("재보험", "direct", 2.5),
            IndustryKeyword("언더라이팅", "direct", 2.5),
            IndustryKeyword("손해율", "direct", 2.5),
            IndustryKeyword("리스크평가", "direct", 3.0),
            IndustryKeyword("인슈어테크", "technology", 2.0),
            IndustryKeyword("보험사기", "related", 1.5),
            IndustryKeyword("기후리스크", "related", 2.0),
            IndustryKeyword("자연재해보험", "related", 2.0),
        ],

        stakeholder_templates=[
            StakeholderTemplate("보험사 CRO", "company", 5, 5, True, True),
            StakeholderTemplate("재보험사 언더라이터", "company", 4, 5, True, True),
            StakeholderTemplate("금융위 보험정책과", "government", 4, 3, False, True),
            StakeholderTemplate("보험개발원 연구원", "research", 2, 5, False, False),
            StakeholderTemplate("액츄어리 (계리사)", "company", 3, 5, False, False),
        ],

        default_forces={
            "supplier_power": 2,
            "buyer_power": 3,
            "competitive_rivalry": 4,
            "threat_of_substitution": 3,
            "threat_of_new_entry": 3
        },

        tech_categories=["리스크 모델링", "데이터 분석", "블록체인", "AI 심사", "IoT 연동"]
    ),

    # =========================================================================
    # 3. 물류 및 공급망 관리
    # =========================================================================
    IndustryCode.LOGISTICS_SCM: IndustryProfile(
        code=IndustryCode.LOGISTICS_SCM,
        name_ko="물류 및 공급망 관리",
        name_en="Logistics & Supply Chain Management",
        description="인프라 마비가 경제에 미치는 '진짜 가치'를 증명하는 영역. 터널 하나가 막혔을 때의 경제적 피해를 숫자로 산출",

        core_concepts=[
            "통과 화물 가치 (VPC: Value of Passing Cargo)",
            "국가 물류 네트워크 최적화",
            "기회비용 계산",
            "공급망 회복탄력성 (Supply Chain Resilience)",
            "라스트마일 배송"
        ],

        business_connection="터널 하나가 막혔을 때 쿠팡이나 CJ대한통운 같은 기업의 물류 허브가 어떻게 마비되는지 숫자로 뽑아내야 우리 솔루션의 필요성이 극대화",

        policy_sources=[
            PolicySource("국토부 물류정책", "국토교통부", "webpage", "https://www.molit.go.kr/logistics"),
            PolicySource("물류신문", "물류신문", "rss", "https://www.klnews.co.kr/rss/"),
            PolicySource("한국교통연구원", "한국교통연구원", "webpage", "https://www.koti.re.kr"),
        ],

        keywords=[
            IndustryKeyword("물류", "direct", 3.0),
            IndustryKeyword("공급망", "direct", 3.0),
            IndustryKeyword("SCM", "direct", 2.5),
            IndustryKeyword("화물", "direct", 2.5),
            IndustryKeyword("배송", "related", 2.0),
            IndustryKeyword("물류센터", "direct", 2.5),
            IndustryKeyword("스마트물류", "technology", 2.0),
            IndustryKeyword("풀필먼트", "related", 1.5),
            IndustryKeyword("콜드체인", "related", 1.5),
            IndustryKeyword("라스트마일", "related", 2.0),
        ],

        stakeholder_templates=[
            StakeholderTemplate("물류기업 CEO", "company", 4, 5, True, True),
            StakeholderTemplate("대형 유통사 SCM 담당", "company", 4, 5, True, True),
            StakeholderTemplate("국토부 물류정책관", "government", 4, 4, True, True),
            StakeholderTemplate("물류협회 사무총장", "association", 3, 4, False, False),
            StakeholderTemplate("항만/공항 운영사", "agency", 4, 3, True, False),
        ],

        default_forces={
            "supplier_power": 3,
            "buyer_power": 4,
            "competitive_rivalry": 5,  # 매우 치열
            "threat_of_substitution": 2,
            "threat_of_new_entry": 3
        },

        tech_categories=["WMS/TMS", "자율주행", "드론배송", "AI 최적화", "블록체인 추적"]
    ),

    # =========================================================================
    # 4. AI 및 데이터 엔지니어링
    # =========================================================================
    IndustryCode.AI_DATA: IndustryProfile(
        code=IndustryCode.AI_DATA,
        name_ko="AI 및 데이터 엔지니어링",
        name_en="AI & Data Engineering",
        description="'인프라판 커서(Cursor)'를 실제로 구동하는 엔진실. 물리 법칙과 데이터 학습 모델을 결합하여 금융권이 신뢰할 수 있는 결과값 생성",

        core_concepts=[
            "MLOps (데이터 관리)",
            "설명 가능한 AI (XAI: Explainable AI)",
            "디지털 트윈 엔진",
            "물리 기반 AI (Physics-Informed ML)",
            "엣지 AI"
        ],

        business_connection="단순히 AI를 돌리는 게 아니라, '물리 법칙'과 '데이터 학습 모델'을 결합하여 금융권이 신뢰할 수 있는 결과값을 내놓아야 함",

        policy_sources=[
            PolicySource("과기부 AI 정책", "과학기술정보통신부", "rss", "https://www.msit.go.kr/rss/"),
            PolicySource("NIA AI 허브", "한국지능정보사회진흥원", "webpage", "https://www.nia.or.kr"),
            PolicySource("NIPA AI 산업", "정보통신산업진흥원", "webpage", "https://www.nipa.kr"),
        ],

        keywords=[
            IndustryKeyword("인공지능", "direct", 3.0),
            IndustryKeyword("AI", "direct", 3.0),
            IndustryKeyword("머신러닝", "direct", 2.5),
            IndustryKeyword("딥러닝", "direct", 2.5),
            IndustryKeyword("MLOps", "technology", 2.0),
            IndustryKeyword("XAI", "technology", 2.5),
            IndustryKeyword("디지털트윈", "technology", 3.0),
            IndustryKeyword("데이터", "direct", 2.0),
            IndustryKeyword("빅데이터", "direct", 2.0),
            IndustryKeyword("클라우드", "technology", 1.5),
        ],

        stakeholder_templates=[
            StakeholderTemplate("AI 스타트업 CTO", "company", 3, 5, False, False),
            StakeholderTemplate("대기업 AI 센터장", "company", 4, 4, True, True),
            StakeholderTemplate("과기부 AI정책관", "government", 4, 4, True, True),
            StakeholderTemplate("AI 연구소장", "research", 3, 5, False, False),
            StakeholderTemplate("클라우드 벤더 파트너", "company", 3, 4, True, False),
        ],

        default_forces={
            "supplier_power": 4,  # 인재/기술 희소성
            "buyer_power": 3,
            "competitive_rivalry": 5,  # 글로벌 경쟁
            "threat_of_substitution": 2,
            "threat_of_new_entry": 4  # 진입 쉬움
        },

        tech_categories=["ML/DL 프레임워크", "MLOps", "데이터 파이프라인", "Edge AI", "시뮬레이션"]
    ),

    # =========================================================================
    # 5. 공공 행정 및 법률
    # =========================================================================
    IndustryCode.PUBLIC_LAW: IndustryProfile(
        code=IndustryCode.PUBLIC_LAW,
        name_ko="공공 행정 및 법률",
        name_en="Public Affairs & Law",
        description="정부를 설득하고 우리 점수를 '국가 표준'으로 법제화하는 영역. 사고 시 공무원들이 법적 책임에서 벗어날 수 있는 '면책의 데이터' 제공",

        core_concepts=[
            "중대재해처벌법",
            "시설물안전법",
            "공공조달 프로세스 (G2B)",
            "표준화 및 인증",
            "규제 샌드박스"
        ],

        business_connection="사고 시 공무원들이 '법적 책임'에서 벗어날 수 있는 '면책의 데이터'를 제공하는 것이 시장 확산의 가장 빠른 길",

        policy_sources=[
            PolicySource("법제처 법령정보", "법제처", "api", "https://www.law.go.kr"),
            PolicySource("행안부 보도자료", "행정안전부", "rss", "https://www.mois.go.kr/rss/"),
            PolicySource("고용노동부", "고용노동부", "rss", "https://www.moel.go.kr/rss/"),
            PolicySource("조달청 나라장터", "조달청", "api", "https://www.g2b.go.kr"),
        ],

        keywords=[
            IndustryKeyword("중대재해", "direct", 3.0),
            IndustryKeyword("시설물안전법", "direct", 3.0),
            IndustryKeyword("안전관리", "direct", 2.5),
            IndustryKeyword("조달", "direct", 2.5),
            IndustryKeyword("G2B", "direct", 2.0),
            IndustryKeyword("표준", "related", 2.0),
            IndustryKeyword("인증", "related", 2.0),
            IndustryKeyword("규제샌드박스", "policy", 2.0),
            IndustryKeyword("법령개정", "policy", 2.5),
            IndustryKeyword("공공기관", "related", 1.5),
        ],

        stakeholder_templates=[
            StakeholderTemplate("국회 상임위 전문위원", "government", 5, 4, False, True),
            StakeholderTemplate("부처 법무담당관", "government", 4, 4, False, True),
            StakeholderTemplate("조달청 담당 사무관", "government", 4, 5, True, True),
            StakeholderTemplate("표준협회 심사관", "agency", 3, 4, False, True),
            StakeholderTemplate("로펌 규제전문 변호사", "company", 2, 5, False, False),
        ],

        default_forces={
            "supplier_power": 2,
            "buyer_power": 5,  # 정부가 슈퍼 갑
            "competitive_rivalry": 3,
            "threat_of_substitution": 2,
            "threat_of_new_entry": 2  # 관계/실적 중요
        },

        tech_categories=["레그테크", "컴플라이언스 AI", "문서 자동화", "전자조달", "블록체인 증적"]
    ),
}


def get_industry(code: IndustryCode) -> IndustryProfile:
    """산업 프로필 조회"""
    return INDUSTRY_PROFILES[code]


def get_all_industries() -> Dict[IndustryCode, IndustryProfile]:
    """전체 산업 목록"""
    return INDUSTRY_PROFILES


def get_industry_keywords(code: IndustryCode) -> List[IndustryKeyword]:
    """산업별 키워드 목록"""
    return INDUSTRY_PROFILES[code].keywords


def get_cross_industry_keywords() -> Dict[str, List[IndustryCode]]:
    """
    산업 간 교차 키워드 분석
    어떤 키워드가 여러 산업에서 공통으로 중요한지 파악
    """
    keyword_map: Dict[str, List[IndustryCode]] = {}

    for code, profile in INDUSTRY_PROFILES.items():
        for kw in profile.keywords:
            if kw.keyword not in keyword_map:
                keyword_map[kw.keyword] = []
            keyword_map[kw.keyword].append(code)

    # 2개 이상 산업에서 공통인 키워드만 필터
    return {k: v for k, v in keyword_map.items() if len(v) >= 2}
