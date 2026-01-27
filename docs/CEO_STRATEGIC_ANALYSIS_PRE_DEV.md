# CEO 전략 분석 도구 - 개발 전 준비 단계 총정리

> **목적**: Cursor AI에서 실제 개발에 들어가기 전, 완료해야 할 모든 준비 작업 정리
> **대상 제품**: Lux-Guard (터널·도로 안전 산업)

---

## 📋 목차

1. [Phase 0: 프로젝트 정의](#phase-0-프로젝트-정의)
2. [Phase 1: 데이터 소스 조사](#phase-1-데이터-소스-조사)
3. [Phase 2: 요구사항 명세](#phase-2-요구사항-명세)
4. [Phase 3: 아키텍처 설계](#phase-3-아키텍처-설계)
5. [Phase 4: 데이터 모델 설계](#phase-4-데이터-모델-설계)
6. [Phase 5: API 명세 작성](#phase-5-api-명세-작성)
7. [Phase 6: UI/UX 설계](#phase-6-uiux-설계)
8. [Phase 7: 기술 스택 확정](#phase-7-기술-스택-확정)
9. [Phase 8: 개발 로드맵](#phase-8-개발-로드맵)

---

## Phase 0: 프로젝트 정의

### 0.1 해결하려는 문제

```
대표가 "판을 설명하는 보고서"를 머릿속에 항상 갖고 있어야 함
→ 이를 자동화/시각화하는 대시보드 필요
```

### 0.2 만들어야 할 7가지 분석 도구

| # | 분석 도구 | 핵심 질문 | 산출물 |
|---|----------|----------|--------|
| 1 | 산업 구조 보고서 | "이 산업은 왜 이렇게 굴러가냐?" | 이해관계자 맵, 돈의 흐름도 |
| 2 | 시장 규모 & 성장 논리 | "TAM/SAM/SOM이 얼마냐?" | 시장 규모 계산서, 성장 근거 |
| 3 | 정책·제도 트래킹 | "어떤 정책이 우리에게 유리하냐?" | 정책 알림, 요약 리포트 |
| 4 | 기술 트렌드 지도 | "이 기술은 3년 후에도 살아남냐?" | Technology Radar |
| 5 | 경쟁 & 유사 기술 리포트 | "진짜 경쟁자가 누구냐?" | 경쟁사 비교표, 포지셔닝 맵 |
| 6 | Value Chain & Stakeholder 맵 | "누가 뭘 쥐고 있냐?" | 이해관계자 관계도 |
| 7 | '왜 지금인가' 보고서 | "왜 지금이 기회냐?" | Timing Thesis 1-pager |

### 0.3 사용자 정의

| 사용자 | 사용 목적 | 필요 기능 |
|--------|----------|----------|
| CEO/대표 | 투자자/공공 미팅 준비 | 핵심 수치 즉시 조회, 1-pager 출력 |
| CEO/대표 | 전략 의사결정 | 트렌드 변화 알림, What-if 시뮬레이션 |
| CEO/대표 | 팀 방향 제시 | 산업 맥락 공유 자료 생성 |

---

## Phase 1: 데이터 소스 조사

> **[TODO]** 각 항목별로 실제 URL, API 키 발급 방법, 데이터 형식 조사 필요

### 1.1 산업 구조 데이터

| 데이터 | 출처 후보 | 조사 항목 | 상태 |
|--------|----------|----------|------|
| 도로/터널 발주 현황 | 조달청 나라장터 | API 유무, 크롤링 가능 여부 | [ ] 미조사 |
| 공공 예산 현황 | 열린재정 (기재부) | API 스펙, 데이터 갱신 주기 | [ ] 미조사 |
| 건설/안전 업체 현황 | 대한건설협회, 안전공단 | 데이터 접근 방법 | [ ] 미조사 |
| 사고 통계 | 도로교통공단, 국토부 | API 또는 다운로드 | [ ] 미조사 |

### 1.2 시장 규모 데이터

| 데이터 | 출처 후보 | 조사 항목 | 상태 |
|--------|----------|----------|------|
| 국내 도로 인프라 투자 | 국토부 중장기 계획 | PDF 파싱 또는 수동 입력 | [ ] 미조사 |
| 터널 수/길이 현황 | 국가교통DB | API 유무 | [ ] 미조사 |
| 안전 시장 규모 | 민간 리서치 (마크앤마켓 등) | 유료/무료, 인용 가능 여부 | [ ] 미조사 |
| 해외 시장 규모 | Statista, IBIS World | 구독 필요 여부 | [ ] 미조사 |

### 1.3 정책·제도 데이터

| 데이터 | 출처 후보 | 조사 항목 | 상태 |
|--------|----------|----------|------|
| 국토부 정책 | 국토부 보도자료 RSS | RSS 피드 URL | [ ] 미조사 |
| 행안부 안전 정책 | 행안부 보도자료 | RSS/크롤링 방법 | [ ] 미조사 |
| 법령 개정 | 국가법령정보센터 | API 스펙 | [ ] 미조사 |
| R&D 예산 | 과기부, NTIS | API 또는 공개 데이터 | [ ] 미조사 |

### 1.4 기술 트렌드 데이터

| 데이터 | 출처 후보 | 조사 항목 | 상태 |
|--------|----------|----------|------|
| 특허 동향 | KIPRIS (특허청) | API 스펙, 검색 키워드 | [ ] 미조사 |
| 논문 동향 | Google Scholar, RISS | 크롤링/API 방법 | [ ] 미조사 |
| 기술 뉴스 | TechCrunch, 전자신문 | RSS 피드 | [ ] 미조사 |
| Gartner/Forrester | 공식 리포트 | 유료 여부, 요약 접근 | [ ] 미조사 |

### 1.5 경쟁사 데이터

| 데이터 | 출처 후보 | 조사 항목 | 상태 |
|--------|----------|----------|------|
| 국내 경쟁사 리스트 | 수동 조사 + 뉴스 | 목록 작성 | [ ] 미조사 |
| 해외 유사 서비스 | Crunchbase, LinkedIn | 검색 키워드 | [ ] 미조사 |
| 경쟁사 뉴스 | 구글 알리미, 네이버 알림 | 설정 방법 | [ ] 미조사 |
| 제품 스펙 비교 | 경쟁사 웹사이트 | 수동 수집 항목 정의 | [ ] 미조사 |

### 1.6 이해관계자 데이터

| 데이터 | 출처 후보 | 조사 항목 | 상태 |
|--------|----------|----------|------|
| 발주처 조직도 | 국토부, 한국도로공사 | 공개 조직도 URL | [ ] 미조사 |
| 의사결정자 정보 | LinkedIn, 뉴스 | 수동 수집 범위 | [ ] 미조사 |
| 협력사/파트너 후보 | 업계 리스트 | 수동 조사 | [ ] 미조사 |

---

## Phase 2: 요구사항 명세

### 2.1 산업 구조 보고서

#### 기능 요구사항 (FR)

| ID | 요구사항 | 우선순위 | 상태 |
|----|---------|---------|------|
| FR-IND-01 | 발주 구조 다이어그램 표시 | Must | [ ] |
| FR-IND-02 | 책임 구조 (누가 책임지나) 시각화 | Must | [ ] |
| FR-IND-03 | 돈의 흐름 Sankey 다이어그램 | Should | [ ] |
| FR-IND-04 | Porter's 5 Forces 레이더 차트 | Should | [ ] |
| FR-IND-05 | 데이터 수동 입력/수정 기능 | Must | [ ] |
| FR-IND-06 | PDF/이미지 내보내기 | Should | [ ] |

#### 비기능 요구사항 (NFR)

| ID | 요구사항 | 기준 |
|----|---------|------|
| NFR-IND-01 | 페이지 로딩 시간 | < 2초 |
| NFR-IND-02 | 데이터 갱신 주기 | 수동 (사용자 입력 기반) |

---

### 2.2 시장 규모 & 성장 논리

#### 기능 요구사항 (FR)

| ID | 요구사항 | 우선순위 | 상태 |
|----|---------|---------|------|
| FR-MKT-01 | TAM/SAM/SOM 입력 및 계산 | Must | [ ] |
| FR-MKT-02 | 계산 근거 (출처) 기록 | Must | [ ] |
| FR-MKT-03 | 성장률 예측 그래프 | Should | [ ] |
| FR-MKT-04 | "왜 커질 수밖에 없는가" 논리 정리 | Must | [ ] |
| FR-MKT-05 | 사고 통계 연동 (자동/수동) | Should | [ ] |
| FR-MKT-06 | 투자자용 1-pager 출력 | Must | [ ] |

---

### 2.3 정책·제도 트래킹

#### 기능 요구사항 (FR)

| ID | 요구사항 | 우선순위 | 상태 |
|----|---------|---------|------|
| FR-POL-01 | 정책 키워드 등록 | Must | [ ] |
| FR-POL-02 | 새 정책 자동 알림 (이메일/슬랙) | Must | [ ] |
| FR-POL-03 | 정책 문서 자동 요약 (AI) | Should | [ ] |
| FR-POL-04 | 정책 타임라인 시각화 | Should | [ ] |
| FR-POL-05 | 우리 제품과 연관성 표시 | Should | [ ] |
| FR-POL-06 | 정책 북마크/태그 기능 | Must | [ ] |

---

### 2.4 기술 트렌드 지도

#### 기능 요구사항 (FR)

| ID | 요구사항 | 우선순위 | 상태 |
|----|---------|---------|------|
| FR-TECH-01 | Technology Radar 시각화 (4분면) | Must | [ ] |
| FR-TECH-02 | 기술별 Adopt/Trial/Assess/Hold 분류 | Must | [ ] |
| FR-TECH-03 | 기술 성숙도 평가 입력 | Must | [ ] |
| FR-TECH-04 | 관련 기술 뉴스 연동 | Should | [ ] |
| FR-TECH-05 | 대체 가능성 평가 | Should | [ ] |
| FR-TECH-06 | 히스토리 (분류 변경 이력) | Should | [ ] |

---

### 2.5 경쟁 & 유사 기술 리포트

#### 기능 요구사항 (FR)

| ID | 요구사항 | 우선순위 | 상태 |
|----|---------|---------|------|
| FR-COMP-01 | 경쟁사 등록/관리 | Must | [ ] |
| FR-COMP-02 | 기능 비교 매트릭스 | Must | [ ] |
| FR-COMP-03 | 2D 포지셔닝 맵 | Should | [ ] |
| FR-COMP-04 | 경쟁사 뉴스 자동 수집 | Should | [ ] |
| FR-COMP-05 | SWOT 분석 템플릿 | Must | [ ] |
| FR-COMP-06 | "진짜 경쟁자 vs 다른 접근" 분류 | Should | [ ] |

---

### 2.6 Value Chain & Stakeholder 맵

#### 기능 요구사항 (FR)

| ID | 요구사항 | 우선순위 | 상태 |
|----|---------|---------|------|
| FR-VC-01 | 이해관계자 등록 (조직/개인) | Must | [ ] |
| FR-VC-02 | 관계 정의 (발주권, 예산, 책임, 데이터) | Must | [ ] |
| FR-VC-03 | 관계도 시각화 (Graph) | Must | [ ] |
| FR-VC-04 | Power/Interest Grid | Should | [ ] |
| FR-VC-05 | Value Chain 다이어그램 | Should | [ ] |
| FR-VC-06 | 핵심 의사결정자 하이라이트 | Must | [ ] |

---

### 2.7 '왜 지금인가' 보고서

#### 기능 요구사항 (FR)

| ID | 요구사항 | 우선순위 | 상태 |
|----|---------|---------|------|
| FR-TIME-01 | Timing Factor 등록 (AI 성숙, 정책 압박 등) | Must | [ ] |
| FR-TIME-02 | 각 Factor별 근거 자료 연결 | Must | [ ] |
| FR-TIME-03 | Timing Thesis 문장 생성 (AI) | Should | [ ] |
| FR-TIME-04 | 타임라인 시각화 | Should | [ ] |
| FR-TIME-05 | 피치덱용 1-pager 출력 | Must | [ ] |

---

## Phase 3: 아키텍처 설계

### 3.1 전체 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CEO Dashboard                                │
│                    (Next.js + React + TailwindCSS)                  │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┬────────┐ │
│  │ Industry │ Market   │ Policy   │ Tech     │ Compete  │ Timing │ │
│  │ Structure│ Size     │ Tracker  │ Radar    │ Watch    │ Thesis │ │
│  └──────────┴──────────┴──────────┴──────────┴──────────┴────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         API Gateway (FastAPI)                        │
│         /api/industry  /api/market  /api/policy  /api/tech          │
│         /api/compete   /api/valuechain  /api/timing                 │
└─────────────────────────────────────────────────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐        ┌─────────────────┐        ┌─────────────────┐
│  Data Layer   │        │   AI Layer      │        │  External APIs  │
│               │        │                 │        │                 │
│ PostgreSQL    │        │ OpenAI/Claude   │        │ 국토부 RSS      │
│ (메인 DB)     │        │ (요약, 생성)    │        │ 조달청 API      │
│               │        │                 │        │ 뉴스 크롤러     │
│ Neo4j         │        │ Hugging Face    │        │ 특허청 API      │
│ (관계 그래프) │        │ (키워드 추출)   │        │                 │
│               │        │                 │        │                 │
│ Redis         │        │                 │        │                 │
│ (캐시)        │        │                 │        │                 │
└───────────────┘        └─────────────────┘        └─────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────┐
                    │    Background Jobs      │
                    │    (Celery + Redis)     │
                    │                         │
                    │ - 정책 크롤링 (1시간)   │
                    │ - 뉴스 수집 (30분)      │
                    │ - AI 요약 (on-demand)   │
                    └─────────────────────────┘
```

### 3.2 컴포넌트 설계

#### Frontend 컴포넌트 구조

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx (대시보드 홈)
│   ├── industry/
│   │   └── page.tsx
│   ├── market/
│   │   └── page.tsx
│   ├── policy/
│   │   └── page.tsx
│   ├── tech/
│   │   └── page.tsx
│   ├── compete/
│   │   └── page.tsx
│   ├── valuechain/
│   │   └── page.tsx
│   └── timing/
│       └── page.tsx
├── components/
│   ├── charts/
│   │   ├── RadarChart.tsx
│   │   ├── SankeyDiagram.tsx
│   │   ├── ForceGraph.tsx
│   │   ├── PositioningMap.tsx
│   │   └── Timeline.tsx
│   ├── cards/
│   │   ├── MetricCard.tsx
│   │   ├── PolicyCard.tsx
│   │   └── CompetitorCard.tsx
│   └── shared/
│       ├── ExportButton.tsx
│       └── DataSourceBadge.tsx
└── lib/
    ├── api.ts
    └── utils.ts
```

#### Backend 컴포넌트 구조

```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── industry.py
│   │   ├── market.py
│   │   ├── policy.py
│   │   ├── tech.py
│   │   ├── competitor.py
│   │   ├── stakeholder.py
│   │   └── timing.py
│   ├── schemas/
│   │   └── (Pydantic 스키마)
│   ├── services/
│   │   ├── industry_service.py
│   │   ├── market_service.py
│   │   ├── policy_service.py
│   │   ├── tech_service.py
│   │   ├── competitor_service.py
│   │   ├── stakeholder_service.py
│   │   ├── timing_service.py
│   │   └── ai_service.py
│   ├── routers/
│   │   └── (API 라우터)
│   └── tasks/
│       ├── policy_crawler.py
│       ├── news_collector.py
│       └── ai_summarizer.py
└── requirements.txt
```

---

## Phase 4: 데이터 모델 설계

### 4.1 PostgreSQL 테이블

#### industry_structure (산업 구조)

```sql
CREATE TABLE industry_structure (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,           -- 구조 이름 (예: "터널 안전 산업")
    description TEXT,

    -- Porter's 5 Forces 점수 (1-5)
    supplier_power INTEGER,
    buyer_power INTEGER,
    competitive_rivalry INTEGER,
    threat_of_substitution INTEGER,
    threat_of_new_entry INTEGER,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE money_flow (
    id SERIAL PRIMARY KEY,
    industry_id INTEGER REFERENCES industry_structure(id),
    source_entity VARCHAR(255),           -- 돈 출처
    target_entity VARCHAR(255),           -- 돈 도착
    amount_description VARCHAR(255),      -- 금액 설명
    flow_type VARCHAR(50),                -- budget, contract, subsidy 등
    notes TEXT
);
```

#### market_size (시장 규모)

```sql
CREATE TABLE market_size (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,

    -- TAM/SAM/SOM
    tam_value BIGINT,
    tam_unit VARCHAR(20),                 -- "억원", "백만달러" 등
    tam_source TEXT,
    tam_year INTEGER,

    sam_value BIGINT,
    sam_unit VARCHAR(20),
    sam_source TEXT,
    sam_year INTEGER,

    som_value BIGINT,
    som_unit VARCHAR(20),
    som_source TEXT,
    som_year INTEGER,

    -- 성장 논리
    growth_rate_percent DECIMAL(5,2),
    growth_rationale TEXT,               -- "왜 커지는가"

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE market_evidence (
    id SERIAL PRIMARY KEY,
    market_id INTEGER REFERENCES market_size(id),
    evidence_type VARCHAR(50),           -- accident_stat, policy_budget, infra_plan, overseas_demand
    title VARCHAR(255),
    value TEXT,
    source_url TEXT,
    source_date DATE
);
```

#### policy_tracking (정책 트래킹)

```sql
CREATE TABLE policy_keyword (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE policy_item (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    source VARCHAR(255),                  -- 국토부, 행안부 등
    source_url TEXT,
    published_at TIMESTAMP,

    summary TEXT,                         -- AI 생성 요약
    relevance_score INTEGER,              -- 1-5 연관성
    relevance_reason TEXT,

    is_bookmarked BOOLEAN DEFAULT FALSE,
    tags TEXT[],

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE policy_keyword_match (
    policy_id INTEGER REFERENCES policy_item(id),
    keyword_id INTEGER REFERENCES policy_keyword(id),
    PRIMARY KEY (policy_id, keyword_id)
);
```

#### tech_radar (기술 트렌드)

```sql
CREATE TABLE tech_item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),                -- sensor, algorithm, platform 등

    quadrant VARCHAR(50),                 -- techniques, tools, platforms, languages
    ring VARCHAR(50),                     -- adopt, trial, assess, hold

    is_replaceable BOOLEAN,
    maturity_stage VARCHAR(50),           -- emerging, growth, mature, decline

    description TEXT,
    our_position TEXT,                    -- 우리 기술과의 관계

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tech_history (
    id SERIAL PRIMARY KEY,
    tech_id INTEGER REFERENCES tech_item(id),
    previous_ring VARCHAR(50),
    new_ring VARCHAR(50),
    changed_at TIMESTAMP DEFAULT NOW(),
    reason TEXT
);
```

#### competitor (경쟁사)

```sql
CREATE TABLE competitor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    website TEXT,

    competitor_type VARCHAR(50),          -- direct, indirect, potential
    approach_difference TEXT,             -- 우리와 다른 접근 방식

    -- SWOT
    strengths TEXT[],
    weaknesses TEXT[],
    opportunities TEXT[],
    threats TEXT[],

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE competitor_feature (
    id SERIAL PRIMARY KEY,
    competitor_id INTEGER REFERENCES competitor(id),
    feature_name VARCHAR(255),
    has_feature BOOLEAN,
    notes TEXT
);

CREATE TABLE our_feature (
    id SERIAL PRIMARY KEY,
    feature_name VARCHAR(255),
    has_feature BOOLEAN,
    differentiator BOOLEAN DEFAULT FALSE,
    notes TEXT
);
```

#### stakeholder (이해관계자)

```sql
CREATE TABLE stakeholder (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    organization VARCHAR(255),
    role VARCHAR(255),
    stakeholder_type VARCHAR(50),         -- government, company, individual

    -- Power/Interest Grid
    power_level INTEGER,                  -- 1-5
    interest_level INTEGER,               -- 1-5

    -- 보유 권한
    has_budget BOOLEAN DEFAULT FALSE,
    has_decision_power BOOLEAN DEFAULT FALSE,
    has_data_access BOOLEAN DEFAULT FALSE,
    has_responsibility BOOLEAN DEFAULT FALSE,

    notes TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.2 Neo4j 그래프 모델 (이해관계자 관계)

```cypher
// 노드 타입
(:Stakeholder {
    id: string,
    name: string,
    organization: string,
    type: string,
    power: int,
    interest: int
})

(:Organization {
    id: string,
    name: string,
    type: string  // government, company, association
})

// 관계 타입
(:Stakeholder)-[:WORKS_AT]->(:Organization)
(:Stakeholder)-[:REPORTS_TO]->(:Stakeholder)
(:Organization)-[:CONTRACTS_WITH]->(:Organization)
(:Organization)-[:SUPERVISES]->(:Organization)
(:Organization)-[:FUNDS]->(:Organization)
```

### 4.3 timing_thesis (왜 지금인가)

```sql
CREATE TABLE timing_factor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,           -- "AI 성능 성숙", "정책 압박" 등
    category VARCHAR(100),                -- technology, policy, market, social

    description TEXT,
    current_status TEXT,                  -- 현재 상황
    trend_direction VARCHAR(50),          -- improving, stable, declining

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE timing_evidence (
    id SERIAL PRIMARY KEY,
    factor_id INTEGER REFERENCES timing_factor(id),
    title VARCHAR(255),
    description TEXT,
    source_url TEXT,
    source_date DATE
);

CREATE TABLE timing_thesis (
    id SERIAL PRIMARY KEY,
    thesis_statement TEXT NOT NULL,       -- 핵심 문장
    target_audience VARCHAR(100),         -- investor, government, partner
    version INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE timing_thesis_factor (
    thesis_id INTEGER REFERENCES timing_thesis(id),
    factor_id INTEGER REFERENCES timing_factor(id),
    PRIMARY KEY (thesis_id, factor_id)
);
```

---

## Phase 5: API 명세 작성

### 5.1 API 엔드포인트 목록

#### 산업 구조 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/industry` | 산업 구조 조회 |
| PUT | `/api/industry` | 산업 구조 수정 |
| GET | `/api/industry/forces` | Porter's 5 Forces 데이터 |
| PUT | `/api/industry/forces` | 5 Forces 점수 수정 |
| GET | `/api/industry/money-flow` | 돈의 흐름 조회 |
| POST | `/api/industry/money-flow` | 돈의 흐름 추가 |
| DELETE | `/api/industry/money-flow/{id}` | 돈의 흐름 삭제 |

#### 시장 규모 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/market` | 시장 규모 조회 |
| PUT | `/api/market` | TAM/SAM/SOM 수정 |
| GET | `/api/market/evidence` | 근거 자료 목록 |
| POST | `/api/market/evidence` | 근거 자료 추가 |
| DELETE | `/api/market/evidence/{id}` | 근거 자료 삭제 |
| GET | `/api/market/export/onepager` | 1-pager PDF 생성 |

#### 정책 트래킹 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/policy/keywords` | 키워드 목록 |
| POST | `/api/policy/keywords` | 키워드 추가 |
| DELETE | `/api/policy/keywords/{id}` | 키워드 삭제 |
| GET | `/api/policy/items` | 수집된 정책 목록 |
| GET | `/api/policy/items/{id}` | 정책 상세 |
| POST | `/api/policy/items/{id}/bookmark` | 북마크 토글 |
| POST | `/api/policy/items/{id}/summarize` | AI 요약 생성 |
| GET | `/api/policy/timeline` | 정책 타임라인 |

#### 기술 트렌드 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/tech` | 기술 목록 |
| POST | `/api/tech` | 기술 추가 |
| PUT | `/api/tech/{id}` | 기술 수정 |
| DELETE | `/api/tech/{id}` | 기술 삭제 |
| PUT | `/api/tech/{id}/ring` | Ring 변경 (adopt/trial/assess/hold) |
| GET | `/api/tech/radar` | Radar 시각화용 데이터 |
| GET | `/api/tech/{id}/history` | 변경 이력 |

#### 경쟁사 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/competitors` | 경쟁사 목록 |
| POST | `/api/competitors` | 경쟁사 추가 |
| PUT | `/api/competitors/{id}` | 경쟁사 수정 |
| DELETE | `/api/competitors/{id}` | 경쟁사 삭제 |
| GET | `/api/competitors/matrix` | 기능 비교 매트릭스 |
| GET | `/api/competitors/positioning` | 포지셔닝 맵 데이터 |
| PUT | `/api/competitors/{id}/swot` | SWOT 수정 |
| GET | `/api/our-features` | 우리 기능 목록 |
| PUT | `/api/our-features` | 우리 기능 수정 |

#### 이해관계자 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/stakeholders` | 이해관계자 목록 |
| POST | `/api/stakeholders` | 이해관계자 추가 |
| PUT | `/api/stakeholders/{id}` | 이해관계자 수정 |
| DELETE | `/api/stakeholders/{id}` | 이해관계자 삭제 |
| GET | `/api/stakeholders/graph` | 관계 그래프 데이터 |
| POST | `/api/stakeholders/relations` | 관계 추가 |
| DELETE | `/api/stakeholders/relations/{id}` | 관계 삭제 |
| GET | `/api/stakeholders/power-grid` | Power/Interest Grid 데이터 |

#### Timing Thesis API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/timing/factors` | Timing Factor 목록 |
| POST | `/api/timing/factors` | Factor 추가 |
| PUT | `/api/timing/factors/{id}` | Factor 수정 |
| DELETE | `/api/timing/factors/{id}` | Factor 삭제 |
| GET | `/api/timing/factors/{id}/evidence` | Factor 근거 목록 |
| POST | `/api/timing/factors/{id}/evidence` | 근거 추가 |
| GET | `/api/timing/thesis` | Thesis 목록 |
| POST | `/api/timing/thesis` | Thesis 생성 |
| POST | `/api/timing/thesis/generate` | AI Thesis 생성 |
| GET | `/api/timing/export/onepager` | 1-pager PDF 생성 |

---

## Phase 6: UI/UX 설계

### 6.1 와이어프레임 필요 목록

| 화면 | 주요 요소 | 상태 |
|------|----------|------|
| 대시보드 홈 | 7개 분석 카드 요약, 최근 알림 | [ ] 미작성 |
| 산업 구조 | 5 Forces 레이더, Sankey 다이어그램 | [ ] 미작성 |
| 시장 규모 | TAM/SAM/SOM 카드, 근거 테이블, 1-pager 미리보기 | [ ] 미작성 |
| 정책 트래킹 | 키워드 필터, 정책 카드 목록, 타임라인 뷰 | [ ] 미작성 |
| 기술 트렌드 | Technology Radar (4분면), 기술 리스트 | [ ] 미작성 |
| 경쟁사 분석 | 비교 매트릭스, 포지셔닝 맵, SWOT 카드 | [ ] 미작성 |
| 이해관계자 맵 | Force Graph, Power/Interest Grid | [ ] 미작성 |
| Timing Thesis | Factor 카드, 타임라인, Thesis 에디터 | [ ] 미작성 |

### 6.2 디자인 시스템

> **[TODO]** 확정 필요

| 항목 | 후보 | 결정 |
|------|------|------|
| CSS 프레임워크 | TailwindCSS | [ ] |
| 컴포넌트 라이브러리 | shadcn/ui, Radix UI | [ ] |
| 차트 라이브러리 | Chart.js, Recharts, D3.js | [ ] |
| 그래프 시각화 | D3.js Force, vis.js, Cytoscape | [ ] |
| 아이콘 | Lucide, Heroicons | [ ] |
| 컬러 팔레트 | 브랜드 컬러 정의 필요 | [ ] |

---

## Phase 7: 기술 스택 확정

### 7.1 기술 스택 결정 체크리스트

#### Frontend

| 항목 | 후보 | 선택 | 선택 이유 |
|------|------|------|----------|
| 프레임워크 | Next.js 14 / React | [ ] | |
| 언어 | TypeScript | [ ] | |
| 스타일링 | TailwindCSS | [ ] | |
| 상태 관리 | Zustand / Jotai / Redux | [ ] | |
| API 클라이언트 | TanStack Query (React Query) | [ ] | |
| 폼 관리 | React Hook Form + Zod | [ ] | |
| 차트 | Recharts / Chart.js / D3.js | [ ] | |
| 그래프 | D3.js / vis.js | [ ] | |
| PDF 생성 | react-pdf / html2canvas | [ ] | |

#### Backend

| 항목 | 후보 | 선택 | 선택 이유 |
|------|------|------|----------|
| 프레임워크 | FastAPI (기존 유지) | [x] | 기존 프로젝트 |
| ORM | SQLAlchemy 2.0 / Prisma | [ ] | |
| 마이그레이션 | Alembic | [ ] | |
| 백그라운드 작업 | Celery / Dramatiq / ARQ | [ ] | |
| 캐시 | Redis | [ ] | |
| AI 연동 | OpenAI / Anthropic Claude | [ ] | |

#### Database

| 항목 | 후보 | 선택 | 선택 이유 |
|------|------|------|----------|
| 메인 DB | PostgreSQL | [ ] | |
| 그래프 DB | Neo4j / 없음 (PostgreSQL만) | [ ] | |
| 캐시 | Redis | [ ] | |

#### Infrastructure

| 항목 | 후보 | 선택 | 선택 이유 |
|------|------|------|----------|
| 컨테이너 | Docker + Docker Compose | [ ] | |
| 배포 | Vercel (FE) + Railway/Render (BE) | [ ] | |
| CI/CD | GitHub Actions | [ ] | |

---

## Phase 8: 개발 로드맵

### 8.1 마일스톤 정의

| 마일스톤 | 포함 기능 | 완료 기준 |
|---------|----------|----------|
| **M0: 환경 구축** | DB 셋업, 프로젝트 구조, 기본 UI | Docker Compose로 전체 실행 가능 |
| **M1: 시장 규모** | TAM/SAM/SOM 입력, 근거 관리, 1-pager | 투자자용 문서 출력 가능 |
| **M2: 정책 트래킹** | 키워드 등록, 자동 수집, 알림 | 새 정책 슬랙 알림 수신 |
| **M3: 경쟁사 분석** | 경쟁사 등록, 비교 매트릭스, SWOT | 경쟁 비교표 출력 가능 |
| **M4: 이해관계자 맵** | 등록, 관계 정의, 시각화 | 그래프 시각화 동작 |
| **M5: Timing Thesis** | Factor 관리, AI 생성, 1-pager | Thesis 문서 출력 가능 |
| **M6: 산업 구조** | 5 Forces, Sankey | 산업 구조 시각화 동작 |
| **M7: 기술 Radar** | Radar 시각화, 분류 관리 | Technology Radar 동작 |
| **M8: 통합 & 최적화** | 대시보드 통합, 성능 최적화 | 전체 기능 통합 완료 |

### 8.2 개발 우선순위 (추천)

```
[높음] ─────────────────────────────────────────────────► [낮음]

시장 규모 → 정책 트래킹 → Timing Thesis → 경쟁사 → 이해관계자 → 산업 구조 → 기술 Radar
   │            │              │
   └── 투자 미팅 필수 ──────────┘
```

### 8.3 개발 시작 전 체크리스트

```
[ ] Phase 1: 데이터 소스 조사 완료
[ ] Phase 2: 요구사항 우선순위 확정
[ ] Phase 3: 아키텍처 리뷰 완료
[ ] Phase 4: 데이터 모델 리뷰 완료
[ ] Phase 5: API 명세 리뷰 완료
[ ] Phase 6: 와이어프레임 작성 완료
[ ] Phase 7: 기술 스택 확정
[ ] Phase 8: 마일스톤 일정 확정
```

---

## 부록 A: 알고리즘 & 라이브러리 레퍼런스

### 데이터 수집

| 용도 | 라이브러리 | 설치 |
|------|-----------|------|
| 웹 스크래핑 | BeautifulSoup, Scrapy | `pip install beautifulsoup4 scrapy` |
| RSS 파싱 | feedparser | `pip install feedparser` |
| HTTP 클라이언트 | httpx (async) | `pip install httpx` |

### NLP / AI

| 용도 | 라이브러리/API | 설치/연동 |
|------|---------------|----------|
| 키워드 추출 | KeyBERT, YAKE | `pip install keybert yake` |
| 토픽 모델링 | BERTopic | `pip install bertopic` |
| 문서 요약 | OpenAI API, Claude API | API Key 필요 |
| 한국어 NLP | KoNLPy, kiwipiepy | `pip install konlpy kiwipiepy` |

### 시각화

| 용도 | 라이브러리 | 설치 |
|------|-----------|------|
| 차트 (React) | Recharts | `npm install recharts` |
| Radar Chart | Chart.js | `npm install chart.js react-chartjs-2` |
| Sankey Diagram | D3.js | `npm install d3` |
| Force Graph | D3.js, vis.js | `npm install d3` or `npm install vis-network` |
| 타임라인 | vis-timeline | `npm install vis-timeline` |

### 데이터 분석

| 용도 | 라이브러리 | 설치 |
|------|-----------|------|
| 시계열 예측 | Prophet | `pip install prophet` |
| 통계 분석 | pandas, scipy | `pip install pandas scipy` |
| 그래프 분석 | NetworkX | `pip install networkx` |

---

## 부록 B: 외부 API 레퍼런스 (조사 필요)

| API | 용도 | URL | 상태 |
|-----|------|-----|------|
| 나라장터 | 발주 현황 | https://www.g2b.go.kr | [ ] 조사 필요 |
| 열린재정 | 예산 현황 | https://www.openfiscaldata.go.kr | [ ] 조사 필요 |
| 국가법령정보센터 | 법령 조회 | https://www.law.go.kr | [ ] 조사 필요 |
| KIPRIS | 특허 검색 | https://www.kipris.or.kr | [ ] 조사 필요 |
| NTIS | R&D 정보 | https://www.ntis.go.kr | [ ] 조사 필요 |
| 도로교통공단 | 사고 통계 | https://taas.koroad.or.kr | [ ] 조사 필요 |

---

## 변경 이력

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| 0.1 | 2026-01-27 | Claude | 초안 작성 |

