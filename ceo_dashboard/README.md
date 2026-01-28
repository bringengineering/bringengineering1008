# CEO 전략 분석 대시보드

> 대표가 "판을 설명하는 보고서"를 머릿속에 항상 갖고 있을 수 있도록 지원하는 도구

## 지원 산업 (5개)

| 코드 | 산업명 | 핵심 개념 |
|------|--------|----------|
| `civil_infra` | 건설 및 인프라 자산 관리 | BIM, 시설물 안전, 노후 시설물 유지보수 |
| `insurance_risk` | 보험 및 리스크 금융 | 지수보험, 재보험, 언더라이팅, 손해율 |
| `logistics_scm` | 물류 및 공급망 관리 | VPC, 공급망 최적화, 기회비용 |
| `ai_data` | AI 및 데이터 엔지니어링 | MLOps, XAI, 디지털 트윈, Edge AI |
| `public_law` | 공공 행정 및 법률 | 중대재해법, 시설물안전법, G2B |

## 분석 기능 (7종)

1. **산업 구조 분석** - Porter's 5 Forces로 산업 매력도 평가
2. **시장 규모 계산** - TAM/SAM/SOM 계산 및 성장 예측
3. **정책 트래킹** - 키워드 기반 정책 연관성 점수
4. **기술 트렌드** - Technology Radar (Adopt/Trial/Assess/Hold)
5. **경쟁사 분석** - 기능 비교 매트릭스, 포지셔닝
6. **이해관계자 맵** - Power-Interest Grid
7. **Timing Thesis** - "왜 지금인가" 논리 생성

## 빠른 시작

### 1. 설치

```bash
cd ceo_dashboard
pip install -r requirements.txt
```

### 2. 실행

```bash
# 개발 서버
uvicorn app.main:app --reload --port 8000

# 또는
python -m app.main
```

### 3. API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 사용 예시

### 산업 목록 조회

```bash
curl http://localhost:8000/api/v1/industries
```

### 시장 규모 계산 (Top-Down)

```bash
curl -X POST http://localhost:8000/api/v1/industries/civil_infra/market/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "method": "top_down",
    "total_market_budget": 500000,
    "relevant_segment_ratio": 0.05,
    "target_application_ratio": 0.30,
    "geographic_focus_ratio": 1.0,
    "technology_fit_ratio": 0.4,
    "target_market_share": 0.1,
    "years_to_achieve": 5,
    "yearly_penetration_rate": 0.3
  }'
```

### Porter's 5 Forces 분석

```bash
curl -X POST http://localhost:8000/api/v1/industries/insurance_risk/forces/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "supplier_power": 2,
    "buyer_power": 3,
    "competitive_rivalry": 4,
    "threat_of_substitution": 3,
    "threat_of_new_entry": 3
  }'
```

### 정책 연관성 점수

```bash
curl -X POST http://localhost:8000/api/v1/industries/public_law/policy/relevance \
  -H "Content-Type: application/json" \
  -d '{
    "text": "국토교통부는 터널 안전 강화를 위한 중대재해처벌법 개정안을 발표했다. 시설물안전법에 따른 정밀안전진단 의무화 확대.",
    "source_authority": "ministry",
    "policy_type": "law"
  }'
```

### 기술 Ring 분류

```bash
curl -X POST http://localhost:8000/api/v1/industries/ai_data/tech/classify \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Edge AI",
    "maturity_score": 0.6,
    "adoption_rate": 0.4,
    "our_experience": 0.7,
    "strategic_fit": 0.9,
    "risk_level": 0.3
  }'
```

### Timing Thesis 생성

```bash
curl -X POST "http://localhost:8000/api/v1/industries/civil_infra/timing/thesis?product_name=Lux-Guard&industry_name=인프라 안전" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "name": "AI 기술 성숙",
      "category": "technology",
      "maturity_level": 0.85,
      "impact_score": 0.9,
      "confidence": 0.85,
      "trend_direction": "accelerating",
      "current_state": "딥러닝 기반 컴퓨터 비전이 실용화 단계"
    },
    {
      "name": "중대재해처벌법 시행",
      "category": "policy",
      "maturity_level": 1.0,
      "impact_score": 0.95,
      "confidence": 1.0,
      "trend_direction": "stable",
      "current_state": "2022년 시행, 처벌 사례 증가"
    }
  ]'
```

## 프로젝트 구조

```
ceo_dashboard/
├── app/
│   ├── main.py              # FastAPI 앱
│   ├── core/
│   │   ├── config.py        # 설정
│   │   └── industries.py    # 5개 산업 정의
│   ├── models/
│   │   ├── industry.py      # DB 모델
│   │   ├── stakeholder.py
│   │   └── timing.py
│   ├── schemas/
│   │   └── industry.py      # API 스키마
│   ├── services/
│   │   └── algorithms.py    # 핵심 알고리즘
│   └── api/
│       └── routes.py        # API 라우터
├── requirements.txt
└── README.md
```

## 핵심 알고리즘

### 1. TAM/SAM/SOM 계산

```python
# Top-Down
TAM = 전체시장 × 관련비율 × 적용비율
SAM = TAM × 지역비율 × 기술적합비율
SOM = SAM × 목표점유율 × 침투계수
```

### 2. Porter's 5 Forces

```python
# 매력도 = 25 - (5개 Force 합계)
# 등급: A(16+), B(12+), C(8+), D(4+), E(<4)
```

### 3. Timing Score

```python
# Score = 위치점수×0.3 + 성숙도×0.25 + 영향도×0.25 + 확신도×0.2
# 등급: PERFECT(0.8+), GOOD(0.6+), MODERATE(0.4+), WAIT(<0.4)
```

## 확장 계획

- [ ] PostgreSQL 연동
- [ ] 정책 자동 크롤링 (Celery)
- [ ] AI 요약 (OpenAI/Claude 연동)
- [ ] 프론트엔드 대시보드 (Next.js)
- [ ] PDF 보고서 출력

## 라이선스

Private - BRING Engineering
