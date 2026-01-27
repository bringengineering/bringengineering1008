# CEO 전략 분석 도구 - 아키텍처 상세

> Cursor AI 개발용 시스템 아키텍처 및 프로젝트 구조

---

## 1. 시스템 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Client Layer                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Next.js 14 App Router                             │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │Dashboard │ │ Market   │ │ Policy   │ │ Compete  │ │ Timing   │  │   │
│  │  │  Home    │ │  Size    │ │ Tracker  │ │ Analysis │ │ Thesis   │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  │  ┌──────────┐ ┌──────────┐                                         │   │
│  │  │ Industry │ │  Tech    │     Components: shadcn/ui + Recharts    │   │
│  │  │Structure │ │  Radar   │     State: Zustand + TanStack Query     │   │
│  │  └──────────┘ └──────────┘                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ HTTPS
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API Layer                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         FastAPI Backend                              │   │
│  │                                                                      │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
│  │  │/industry│  │/market  │  │/policy  │  │/compete │  │/timing  │   │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐               │   │
│  │  │ /tech   │  │/stakeh- │  │/dashboard│ │ /export │               │   │
│  │  │         │  │  older  │  │         │  │         │               │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘               │   │
│  │                                                                      │   │
│  │  Middleware: Auth, CORS, RateLimit, Logging                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                ▼                     ▼                     ▼
┌───────────────────────┐ ┌───────────────────┐ ┌───────────────────────┐
│    Service Layer      │ │   AI Layer        │ │  Background Jobs      │
│                       │ │                   │ │                       │
│ ┌───────────────────┐ │ │ ┌───────────────┐ │ │ ┌───────────────────┐ │
│ │ industry_service  │ │ │ │ OpenAI API    │ │ │ │ Policy Crawler    │ │
│ │ market_service    │ │ │ │ Claude API    │ │ │ │ News Collector    │ │
│ │ policy_service    │ │ │ │               │ │ │ │ AI Summarizer     │ │
│ │ tech_service      │ │ │ │ - Summarize   │ │ │ │ Score Calculator  │ │
│ │ competitor_service│ │ │ │ - Generate    │ │ │ │ Alert Sender      │ │
│ │ stakeholder_svc   │ │ │ │ - Analyze     │ │ │ │                   │ │
│ │ timing_service    │ │ │ └───────────────┘ │ │ └───────────────────┘ │
│ │ dashboard_service │ │ │                   │ │                       │
│ └───────────────────┘ │ │ ┌───────────────┐ │ │   Celery + Redis     │
│                       │ │ │ HuggingFace   │ │ │   Beat Scheduler     │
│  Algorithm Engine     │ │ │ (Optional)    │ │ │                       │
└───────────────────────┘ │ │ - KeyBERT     │ │ └───────────────────────┘
                          │ │ - BERTopic    │ │
                          │ └───────────────┘ │
                          └───────────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                ▼                     ▼                     ▼
┌───────────────────────┐ ┌───────────────────┐ ┌───────────────────────┐
│    PostgreSQL         │ │    Redis          │ │   External APIs       │
│    (Primary DB)       │ │    (Cache/Queue)  │ │                       │
│                       │ │                   │ │ - 국토부 RSS          │
│ - Industry data       │ │ - API cache       │ │ - 조달청 API          │
│ - Market data         │ │ - Session         │ │ - 법령정보 API        │
│ - Policy data         │ │ - Job queue       │ │ - 뉴스 크롤링         │
│ - Tech radar          │ │ - Rate limiting   │ │ - KIPRIS (특허)       │
│ - Competitors         │ │                   │ │                       │
│ - Stakeholders        │ └───────────────────┘ └───────────────────────┘
│ - Timing thesis       │
│                       │ ┌───────────────────┐
│                       │ │   Neo4j           │
│                       │ │   (Optional)      │
│                       │ │                   │
│                       │ │ - Stakeholder     │
│                       │ │   relationships   │
│                       │ │ - PageRank        │
└───────────────────────┘ └───────────────────┘
```

---

## 2. 프로젝트 디렉토리 구조

### 2.1 전체 구조

```
ceo-strategic-dashboard/
├── frontend/                    # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/                 # App Router 페이지
│   │   ├── components/          # React 컴포넌트
│   │   ├── lib/                 # 유틸리티
│   │   ├── hooks/               # Custom hooks
│   │   ├── stores/              # Zustand stores
│   │   └── types/               # TypeScript 타입
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── next.config.js
│
├── backend/                     # FastAPI 백엔드
│   ├── app/
│   │   ├── api/                 # API 라우터
│   │   ├── core/                # 핵심 설정
│   │   ├── models/              # SQLAlchemy 모델
│   │   ├── schemas/             # Pydantic 스키마
│   │   ├── services/            # 비즈니스 로직
│   │   ├── algorithms/          # 알고리즘 엔진
│   │   ├── tasks/               # Celery 태스크
│   │   └── main.py              # 앱 진입점
│   ├── alembic/                 # DB 마이그레이션
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker/                      # Docker 설정
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── nginx/
│
├── docs/                        # 문서
│   ├── ALGORITHMS.md
│   ├── DATABASE_SCHEMA.md
│   ├── ARCHITECTURE.md
│   └── API_SPEC.md
│
├── scripts/                     # 유틸리티 스크립트
│   ├── seed_data.py
│   └── crawl_policies.py
│
└── README.md
```

### 2.2 Frontend 상세 구조

```
frontend/src/
├── app/                                 # Next.js App Router
│   ├── layout.tsx                       # 루트 레이아웃
│   ├── page.tsx                         # 대시보드 홈
│   ├── globals.css                      # 글로벌 스타일
│   │
│   ├── (dashboard)/                     # 대시보드 그룹
│   │   ├── layout.tsx                   # 대시보드 레이아웃 (사이드바)
│   │   │
│   │   ├── industry/
│   │   │   ├── page.tsx                 # 산업 구조 페이지
│   │   │   └── components/
│   │   │       ├── FiveForces.tsx       # Porter's 5 Forces
│   │   │       ├── SankeyDiagram.tsx    # 돈의 흐름
│   │   │       └── StructureEditor.tsx  # 구조 편집기
│   │   │
│   │   ├── market/
│   │   │   ├── page.tsx                 # 시장 규모 페이지
│   │   │   └── components/
│   │   │       ├── TamSamSom.tsx        # TAM/SAM/SOM 카드
│   │   │       ├── GrowthChart.tsx      # 성장 예측 차트
│   │   │       ├── EvidenceList.tsx     # 근거 자료 목록
│   │   │       └── OnePagerPreview.tsx  # 1-pager 미리보기
│   │   │
│   │   ├── policy/
│   │   │   ├── page.tsx                 # 정책 트래킹 페이지
│   │   │   └── components/
│   │   │       ├── KeywordManager.tsx   # 키워드 관리
│   │   │       ├── PolicyList.tsx       # 정책 목록
│   │   │       ├── PolicyCard.tsx       # 정책 카드
│   │   │       ├── PolicyDetail.tsx     # 정책 상세
│   │   │       └── Timeline.tsx         # 타임라인 뷰
│   │   │
│   │   ├── tech/
│   │   │   ├── page.tsx                 # 기술 Radar 페이지
│   │   │   └── components/
│   │   │       ├── TechRadar.tsx        # Radar 시각화
│   │   │       ├── TechList.tsx         # 기술 목록
│   │   │       └── TechEditor.tsx       # 기술 편집
│   │   │
│   │   ├── compete/
│   │   │   ├── page.tsx                 # 경쟁 분석 페이지
│   │   │   └── components/
│   │   │       ├── CompetitorList.tsx   # 경쟁사 목록
│   │   │       ├── FeatureMatrix.tsx    # 기능 비교 매트릭스
│   │   │       ├── PositioningMap.tsx   # 포지셔닝 맵
│   │   │       └── SwotCard.tsx         # SWOT 카드
│   │   │
│   │   ├── stakeholder/
│   │   │   ├── page.tsx                 # 이해관계자 페이지
│   │   │   └── components/
│   │   │       ├── StakeholderGraph.tsx # 관계 그래프
│   │   │       ├── PowerInterestGrid.tsx # Power-Interest
│   │   │       └── StakeholderList.tsx  # 목록
│   │   │
│   │   └── timing/
│   │       ├── page.tsx                 # Timing Thesis 페이지
│   │       └── components/
│   │           ├── FactorList.tsx       # Factor 목록
│   │           ├── FactorTimeline.tsx   # 타임라인
│   │           ├── ThesisEditor.tsx     # Thesis 편집기
│   │           └── OnePager.tsx         # 1-pager 출력
│   │
│   ├── settings/
│   │   └── page.tsx                     # 설정 페이지
│   │
│   └── api/                             # API Routes (if needed)
│
├── components/                          # 공유 컴포넌트
│   ├── ui/                              # shadcn/ui 컴포넌트
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── dropdown-menu.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   ├── table.tsx
│   │   ├── tabs.tsx
│   │   └── ...
│   │
│   ├── charts/                          # 차트 컴포넌트
│   │   ├── RadarChart.tsx               # 범용 Radar
│   │   ├── SankeyChart.tsx              # Sankey 다이어그램
│   │   ├── ForceGraph.tsx               # Force-directed Graph
│   │   ├── LineChart.tsx                # 라인 차트
│   │   ├── BarChart.tsx                 # 바 차트
│   │   └── GridChart.tsx                # 2x2 Grid (Power-Interest)
│   │
│   ├── layout/                          # 레이아웃 컴포넌트
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   ├── PageHeader.tsx
│   │   └── Footer.tsx
│   │
│   └── shared/                          # 공용 컴포넌트
│       ├── ExportButton.tsx             # 내보내기 버튼
│       ├── DataSourceBadge.tsx          # 출처 뱃지
│       ├── ScoreGauge.tsx               # 점수 게이지
│       ├── LoadingSpinner.tsx
│       ├── ErrorBoundary.tsx
│       └── EmptyState.tsx
│
├── lib/                                 # 유틸리티
│   ├── api.ts                           # API 클라이언트
│   ├── utils.ts                         # 공용 유틸
│   ├── format.ts                        # 포맷팅 함수
│   └── constants.ts                     # 상수
│
├── hooks/                               # Custom Hooks
│   ├── useMarket.ts                     # 시장 데이터
│   ├── usePolicy.ts                     # 정책 데이터
│   ├── useTech.ts                       # 기술 데이터
│   ├── useCompetitor.ts                 # 경쟁사 데이터
│   ├── useStakeholder.ts                # 이해관계자 데이터
│   ├── useTiming.ts                     # Timing 데이터
│   └── useDashboard.ts                  # 대시보드 데이터
│
├── stores/                              # Zustand Stores
│   ├── authStore.ts                     # 인증 상태
│   ├── uiStore.ts                       # UI 상태
│   └── filterStore.ts                   # 필터 상태
│
└── types/                               # TypeScript 타입
    ├── industry.ts
    ├── market.ts
    ├── policy.ts
    ├── tech.ts
    ├── competitor.ts
    ├── stakeholder.ts
    ├── timing.ts
    └── common.ts
```

### 2.3 Backend 상세 구조

```
backend/app/
├── main.py                              # FastAPI 앱 진입점
│
├── core/                                # 핵심 설정
│   ├── __init__.py
│   ├── config.py                        # 환경 설정
│   ├── database.py                      # DB 연결
│   ├── security.py                      # 인증/보안
│   └── dependencies.py                  # 의존성 주입
│
├── api/                                 # API 라우터
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── router.py                    # 메인 라우터
│   │   │
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── industry.py              # 산업 구조 API
│   │   │   ├── market.py                # 시장 규모 API
│   │   │   ├── policy.py                # 정책 트래킹 API
│   │   │   ├── tech.py                  # 기술 Radar API
│   │   │   ├── competitor.py            # 경쟁사 API
│   │   │   ├── stakeholder.py           # 이해관계자 API
│   │   │   ├── timing.py                # Timing Thesis API
│   │   │   ├── dashboard.py             # 대시보드 API
│   │   │   └── export.py                # 내보내기 API
│   │   │
│   │   └── deps.py                      # 라우터 의존성
│   │
│   └── health.py                        # 헬스체크
│
├── models/                              # SQLAlchemy 모델
│   ├── __init__.py
│   ├── base.py                          # Base 모델
│   ├── user.py
│   ├── industry.py
│   ├── market.py
│   ├── policy.py
│   ├── tech.py
│   ├── competitor.py
│   ├── stakeholder.py
│   └── timing.py
│
├── schemas/                             # Pydantic 스키마
│   ├── __init__.py
│   ├── common.py                        # 공통 스키마
│   ├── industry.py
│   ├── market.py
│   ├── policy.py
│   ├── tech.py
│   ├── competitor.py
│   ├── stakeholder.py
│   ├── timing.py
│   └── dashboard.py
│
├── services/                            # 비즈니스 로직
│   ├── __init__.py
│   ├── industry_service.py
│   ├── market_service.py
│   ├── policy_service.py
│   ├── tech_service.py
│   ├── competitor_service.py
│   ├── stakeholder_service.py
│   ├── timing_service.py
│   ├── dashboard_service.py
│   ├── export_service.py
│   └── ai_service.py                    # AI/LLM 연동
│
├── algorithms/                          # 알고리즘 엔진
│   ├── __init__.py
│   ├── market_calculator.py             # TAM/SAM/SOM 계산
│   ├── forces_analyzer.py               # 5 Forces 분석
│   ├── relevance_scorer.py              # 정책 연관성 점수
│   ├── tech_classifier.py               # Tech Ring 분류
│   ├── competitive_analyzer.py          # 경쟁 분석
│   ├── stakeholder_analyzer.py          # 이해관계자 분석
│   ├── timing_calculator.py             # Timing Score 계산
│   └── health_calculator.py             # Dashboard Health
│
├── tasks/                               # Celery 비동기 태스크
│   ├── __init__.py
│   ├── celery_app.py                    # Celery 설정
│   ├── policy_crawler.py                # 정책 크롤링
│   ├── news_collector.py                # 뉴스 수집
│   ├── ai_tasks.py                      # AI 요약/분석
│   ├── notification_tasks.py            # 알림 발송
│   └── score_tasks.py                   # 점수 계산
│
├── integrations/                        # 외부 연동
│   ├── __init__.py
│   ├── openai_client.py                 # OpenAI API
│   ├── claude_client.py                 # Claude API
│   ├── rss_parser.py                    # RSS 파서
│   └── web_scraper.py                   # 웹 스크래퍼
│
└── utils/                               # 유틸리티
    ├── __init__.py
    ├── text_processor.py                # 텍스트 처리
    ├── date_utils.py                    # 날짜 유틸
    └── cache.py                         # 캐시 유틸
```

---

## 3. 컴포넌트 상세 설계

### 3.1 Frontend 핵심 컴포넌트

#### TechRadar.tsx 구조

```typescript
// frontend/src/app/(dashboard)/tech/components/TechRadar.tsx

interface TechItem {
  id: string;
  name: string;
  quadrant: 'techniques' | 'tools' | 'platforms' | 'languages';
  ring: 'adopt' | 'trial' | 'assess' | 'hold';
  isNew: boolean;
}

interface TechRadarProps {
  items: TechItem[];
  onItemClick?: (item: TechItem) => void;
  onItemMove?: (item: TechItem, newRing: string) => void;
}

// 렌더링 구조
/*
┌─────────────────────────────────────────┐
│               TECHNIQUES                 │
│     ┌───────────────────────┐           │
│     │   ADOPT (innermost)   │           │
│     │  ┌─────────────────┐  │           │
│     │  │     TRIAL       │  │           │
│     │  │  ┌───────────┐  │  │           │
│     │  │  │  ASSESS   │  │  │           │
│     │  │  │ ┌───────┐ │  │  │           │
│ T   │  │  │ │ HOLD  │ │  │  │  P        │
│ O   │  │  │ └───────┘ │  │  │  L        │
│ O   │  │  └───────────┘  │  │  A        │
│ L   │  └─────────────────┘  │  T        │
│ S   └───────────────────────┘  F        │
│                                O        │
│            LANGUAGES           R        │
│                                M        │
│                                S        │
└─────────────────────────────────────────┘
*/
```

#### ForceGraph.tsx 구조

```typescript
// frontend/src/components/charts/ForceGraph.tsx

interface Node {
  id: string;
  name: string;
  type: string;
  power?: number;
  interest?: number;
  size?: number;
}

interface Edge {
  source: string;
  target: string;
  type: string;
  strength?: number;
}

interface ForceGraphProps {
  nodes: Node[];
  edges: Edge[];
  width?: number;
  height?: number;
  onNodeClick?: (node: Node) => void;
  onNodeDrag?: (node: Node, x: number, y: number) => void;
}

// D3.js Force Simulation 사용
```

### 3.2 Backend 서비스 설계

#### market_service.py 구조

```python
# backend/app/services/market_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.market import MarketAnalysis, MarketEvidence
from app.schemas.market import MarketCreate, MarketUpdate
from app.algorithms.market_calculator import (
    calculate_tam_topdown,
    calculate_tam_bottomup,
    calculate_sam,
    calculate_som,
    project_market_size
)

class MarketService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_market(self, market_id: str) -> MarketAnalysis:
        """시장 분석 조회"""
        pass

    async def create_market(self, data: MarketCreate) -> MarketAnalysis:
        """시장 분석 생성"""
        pass

    async def update_market(self, market_id: str, data: MarketUpdate) -> MarketAnalysis:
        """시장 분석 수정"""
        pass

    async def calculate_market_size(
        self,
        market_id: str,
        method: str,  # 'top_down' or 'bottom_up'
        params: dict
    ) -> dict:
        """TAM/SAM/SOM 계산"""
        if method == 'top_down':
            tam = calculate_tam_topdown(**params['tam'])
            sam = calculate_sam(tam, **params['sam'])
            som = calculate_som(sam, **params['som'])
        else:
            tam = calculate_tam_bottomup(**params['tam'])
            # ...
        return {'tam': tam, 'sam': sam, 'som': som}

    async def add_evidence(self, market_id: str, evidence: dict) -> MarketEvidence:
        """근거 자료 추가"""
        pass

    async def generate_projections(
        self,
        market_id: str,
        cagr: float,
        years: int
    ) -> list:
        """연도별 예측 생성"""
        market = await self.get_market(market_id)
        projections = project_market_size(market.tam_value, cagr, years)
        # DB 저장
        return projections

    async def export_onepager(self, market_id: str, format: str = 'pdf') -> bytes:
        """1-pager 내보내기"""
        pass
```

---

## 4. 데이터 플로우

### 4.1 정책 트래킹 플로우

```
┌───────────────────────────────────────────────────────────────────────┐
│                        Policy Tracking Flow                           │
└───────────────────────────────────────────────────────────────────────┘

1. 크롤링 (Celery Beat - 매 1시간)
   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │ RSS Sources │ ---> │ RSS Parser  │ ---> │ Raw Policy  │
   │ (국토부 등)  │      │             │      │   Data      │
   └─────────────┘      └─────────────┘      └─────────────┘
                                                    │
                                                    ▼
2. 키워드 매칭
   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │  Keywords   │ ---> │  Relevance  │ ---> │   Score +   │
   │   (DB)      │      │   Scorer    │      │   Grade     │
   └─────────────┘      └─────────────┘      └─────────────┘
                                                    │
                                                    ▼
3. AI 분석 (연관성 높은 것만)
   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │  Policy     │ ---> │  OpenAI/    │ ---> │  Summary +  │
   │  Content    │      │  Claude     │      │  Analysis   │
   └─────────────┘      └─────────────┘      └─────────────┘
                                                    │
                                                    ▼
4. 알림 발송
   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │  Grade 4-5  │ ---> │ Notification│ ---> │  Email/     │
   │  Policies   │      │   Service   │      │  Slack      │
   └─────────────┘      └─────────────┘      └─────────────┘
                                                    │
                                                    ▼
5. 대시보드 표시
   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │  Frontend   │ <--- │  REST API   │ <--- │  PostgreSQL │
   │  Policy UI  │      │  /policy    │      │  + Redis    │
   └─────────────┘      └─────────────┘      └─────────────┘
```

### 4.2 대시보드 Health Score 플로우

```
┌───────────────────────────────────────────────────────────────────────┐
│                      Dashboard Health Score Flow                       │
└───────────────────────────────────────────────────────────────────────┘

         ┌──────────────┐
         │   Dashboard  │
         │   Request    │
         └──────────────┘
                │
                ▼
    ┌───────────────────────┐
    │   Dashboard Service   │
    └───────────────────────┘
                │
    ┌───────────┼───────────┬───────────┬───────────┬───────────┐
    ▼           ▼           ▼           ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Market │ │ Policy │ │Compete │ │Stakeh- │ │ Timing │ │Industry│
│Service │ │Service │ │Service │ │ older  │ │Service │ │Service │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
    │           │           │           │           │           │
    ▼           ▼           ▼           ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Clarity │ │Tracking│ │Aware-  │ │Mapping │ │Readines│ │Structur│
│ Score  │ │ Score  │ │ ness   │ │ Score  │ │  Score │ │  Score │
│ (0-100)│ │ (0-100)│ │ (0-100)│ │ (0-100)│ │ (0-100)│ │ (0-100)│
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
    │           │           │           │           │           │
    └───────────┴───────────┴─────┬─────┴───────────┴───────────┘
                                  │
                                  ▼
                    ┌───────────────────────┐
                    │   Health Calculator   │
                    │                       │
                    │ total = Σ(score × w)  │
                    │ grade = f(total)      │
                    └───────────────────────┘
                                  │
                                  ▼
                    ┌───────────────────────┐
                    │   Health Score        │
                    │   ┌───────────────┐   │
                    │   │ Score: 72.5   │   │
                    │   │ Grade: B      │   │
                    │   │ Status: ...   │   │
                    │   │ Recommend: [] │   │
                    │   └───────────────┘   │
                    └───────────────────────┘
```

---

## 5. 기술 스택 상세

### 5.1 Frontend

```yaml
Framework: Next.js 14 (App Router)
Language: TypeScript 5.x
Styling: TailwindCSS 3.x
Components: shadcn/ui (Radix UI 기반)
State:
  - Server State: TanStack Query (React Query) v5
  - Client State: Zustand v4
Charts:
  - Recharts (기본 차트)
  - D3.js (Force Graph, Sankey, Radar)
Forms: React Hook Form + Zod
Icons: Lucide React
Date: date-fns
PDF: react-pdf / @react-pdf/renderer
```

### 5.2 Backend

```yaml
Framework: FastAPI 0.110+
Language: Python 3.11+
ORM: SQLAlchemy 2.0 (async)
Validation: Pydantic v2
Database:
  - PostgreSQL 15+
  - Redis 7+
  - Neo4j 5+ (optional)
Background Jobs: Celery 5.x + Redis
AI/ML:
  - OpenAI API (GPT-4)
  - Anthropic API (Claude)
  - KeyBERT (keyword extraction)
  - BERTopic (topic modeling) - optional
Web Scraping:
  - httpx (async HTTP)
  - BeautifulSoup4
  - feedparser (RSS)
PDF Generation: WeasyPrint
```

### 5.3 Infrastructure

```yaml
Container: Docker + Docker Compose
Reverse Proxy: Nginx (production)
Deployment:
  - Frontend: Vercel
  - Backend: Railway / Render / AWS ECS
  - Database: Supabase / AWS RDS
CI/CD: GitHub Actions
Monitoring: (optional)
  - Sentry (error tracking)
  - Prometheus + Grafana
```

---

## 6. Docker 구성

### 6.1 docker-compose.yml

```yaml
version: '3.8'

services:
  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-ceo_dashboard}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
      POSTGRES_DB: ${POSTGRES_DB:-ceo_dashboard}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-ceo_dashboard}"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER:-ceo_dashboard}:${POSTGRES_PASSWORD:-password}@postgres:5432/${POSTGRES_DB:-ceo_dashboard}
      - REDIS_URL=redis://redis:6379/0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Celery Worker
  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER:-ceo_dashboard}:${POSTGRES_PASSWORD:-password}@postgres:5432/${POSTGRES_DB:-ceo_dashboard}
      - REDIS_URL=redis://redis:6379/0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - backend
      - redis
    volumes:
      - ./backend:/app
    command: celery -A app.tasks.celery_app worker --loglevel=info

  # Celery Beat (Scheduler)
  celery_beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER:-ceo_dashboard}:${POSTGRES_PASSWORD:-password}@postgres:5432/${POSTGRES_DB:-ceo_dashboard}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - backend
      - redis
    volumes:
      - ./backend:/app
    command: celery -A app.tasks.celery_app beat --loglevel=info

  # Frontend (Development)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

volumes:
  postgres_data:
  redis_data:
```

### 6.2 Backend Dockerfile

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 7. 환경 변수

### 7.1 Backend (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ceo_dashboard
REDIS_URL=redis://localhost:6379/0

# Neo4j (optional)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# AI APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
MOLIT_RSS_URL=https://www.molit.go.kr/RSS/portal_news.xml

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Environment
ENVIRONMENT=development
DEBUG=true
```

### 7.2 Frontend (.env.local)

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Feature Flags
NEXT_PUBLIC_ENABLE_AI_FEATURES=true
NEXT_PUBLIC_ENABLE_EXPORT=true
```

---

## 8. 개발 시작 가이드

### 8.1 로컬 개발 환경 설정

```bash
# 1. 저장소 클론
git clone <repository>
cd ceo-strategic-dashboard

# 2. 환경 변수 설정
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
# 각 파일 편집하여 API 키 등 설정

# 3. Docker로 인프라 실행
docker-compose up -d postgres redis

# 4. Backend 설정
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# DB 마이그레이션
alembic upgrade head

# 시드 데이터
python scripts/seed_data.py

# 서버 실행
uvicorn app.main:app --reload

# 5. Frontend 설정 (새 터미널)
cd frontend
npm install
npm run dev

# 6. 접속
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 8.2 개발 순서 권장

```
Phase 1: 기반 구축
├── Backend 프로젝트 구조 생성
├── DB 모델 및 마이그레이션
├── 기본 CRUD API
└── Frontend 프로젝트 구조 생성

Phase 2: 핵심 기능 (시장 규모)
├── Market API 완성
├── TAM/SAM/SOM 계산 알고리즘
├── Market UI 컴포넌트
└── 1-pager 내보내기

Phase 3: 정책 트래킹
├── Policy API
├── 크롤링 태스크
├── 연관성 점수 알고리즘
├── Policy UI
└── 알림 시스템

Phase 4: 나머지 기능
├── Tech Radar
├── Competitor Analysis
├── Stakeholder Map
└── Timing Thesis

Phase 5: 통합
├── Dashboard Home
├── Health Score
├── 전체 통합 테스트
└── 최적화
```

---

## 부록: 파일 템플릿

### A. FastAPI 라우터 템플릿

```python
# backend/app/api/v1/endpoints/market.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.market import (
    MarketResponse,
    MarketCreate,
    MarketUpdate,
    MarketCalculateRequest,
)
from app.services.market_service import MarketService

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{market_id}", response_model=MarketResponse)
async def get_market(
    market_id: str,
    db: AsyncSession = Depends(get_db)
):
    """시장 분석 조회"""
    service = MarketService(db)
    market = await service.get_market(market_id)
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    return market


@router.post("/", response_model=MarketResponse, status_code=status.HTTP_201_CREATED)
async def create_market(
    data: MarketCreate,
    db: AsyncSession = Depends(get_db)
):
    """시장 분석 생성"""
    service = MarketService(db)
    return await service.create_market(data)


@router.put("/{market_id}", response_model=MarketResponse)
async def update_market(
    market_id: str,
    data: MarketUpdate,
    db: AsyncSession = Depends(get_db)
):
    """시장 분석 수정"""
    service = MarketService(db)
    return await service.update_market(market_id, data)


@router.post("/{market_id}/calculate")
async def calculate_market_size(
    market_id: str,
    data: MarketCalculateRequest,
    db: AsyncSession = Depends(get_db)
):
    """TAM/SAM/SOM 계산"""
    service = MarketService(db)
    return await service.calculate_market_size(market_id, data.method, data.params)
```

### B. React 컴포넌트 템플릿

```typescript
// frontend/src/app/(dashboard)/market/components/TamSamSom.tsx

'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useMarket } from '@/hooks/useMarket';
import { formatCurrency } from '@/lib/format';

interface TamSamSomProps {
  marketId: string;
}

export function TamSamSom({ marketId }: TamSamSomProps) {
  const { data: market, isLoading, error } = useMarket(marketId);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading market data</div>;
  if (!market) return null;

  const metrics = [
    {
      label: 'TAM',
      value: market.tamValue,
      unit: market.tamUnit,
      description: 'Total Addressable Market',
    },
    {
      label: 'SAM',
      value: market.samValue,
      unit: market.samUnit,
      description: 'Serviceable Addressable Market',
    },
    {
      label: 'SOM',
      value: market.somValue,
      unit: market.somUnit,
      description: 'Serviceable Obtainable Market',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {metrics.map((metric) => (
        <Card key={metric.label}>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {metric.label}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(metric.value)} {metric.unit}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {metric.description}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
```
