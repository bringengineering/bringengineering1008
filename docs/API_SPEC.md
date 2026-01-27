# CEO 전략 분석 도구 - API 상세 명세

> Cursor AI 개발용 API 레퍼런스 (Request/Response 예시 포함)

---

## 1. API 공통 사항

### 1.1 Base URL

```
Development: http://localhost:8000/api/v1
Production:  https://api.yourdomain.com/api/v1
```

### 1.2 공통 헤더

```http
Content-Type: application/json
Authorization: Bearer <access_token>  # 인증 필요한 엔드포인트
```

### 1.3 공통 응답 형식

#### 성공 응답

```json
{
  "data": { ... },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

#### 에러 응답

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "tam_value",
        "message": "must be a positive number"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

### 1.4 페이지네이션

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## 2. 시장 규모 API (Market)

### 2.1 시장 분석 목록 조회

```http
GET /api/v1/market
```

**Query Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| page | int | No | 페이지 번호 (default: 1) |
| page_size | int | No | 페이지 크기 (default: 20) |
| status | string | No | 상태 필터 (draft/reviewed/approved) |

**Response:**

```json
{
  "data": [
    {
      "id": "mkt_abc123",
      "name": "터널 안전 시장 2024",
      "base_year": 2024,
      "tam_value": 7500,
      "tam_unit": "억원",
      "sam_value": 3000,
      "sam_unit": "억원",
      "som_value": 250,
      "som_unit": "억원",
      "cagr_percent": 12.5,
      "status": "draft",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 3,
    "total_pages": 1
  }
}
```

### 2.2 시장 분석 상세 조회

```http
GET /api/v1/market/{market_id}
```

**Response:**

```json
{
  "data": {
    "id": "mkt_abc123",
    "name": "터널 안전 시장 2024",
    "description": "국내 터널 및 도로 안전 시장 분석",
    "base_year": 2024,

    "tam": {
      "value": 7500,
      "unit": "억원",
      "calculation_method": "top_down",
      "assumptions": {
        "total_infrastructure_budget": 500000,
        "safety_allocation_ratio": 0.05,
        "tunnel_road_ratio": 0.30
      },
      "sources": [
        "국토부 2024년 예산안",
        "도로교통공단 통계"
      ]
    },

    "sam": {
      "value": 3000,
      "unit": "억원",
      "calculation_method": "top_down",
      "assumptions": {
        "technology_applicable_ratio": 0.40,
        "region_focus_ratio": 1.0
      },
      "sources": ["자체 분석"]
    },

    "som": {
      "value": 250,
      "unit": "억원",
      "calculation_method": "top_down",
      "assumptions": {
        "market_share_target": 0.10,
        "time_horizon_years": 5,
        "yearly_penetration_rate": 0.30
      },
      "target_year": 2029,
      "sources": ["사업 계획서"]
    },

    "growth": {
      "cagr_percent": 12.5,
      "rationale": "정부 안전 투자 확대, AI 기술 도입 가속화, 노후 터널 증가"
    },

    "status": "draft",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

### 2.3 시장 분석 생성

```http
POST /api/v1/market
```

**Request Body:**

```json
{
  "name": "터널 안전 시장 2024",
  "description": "국내 터널 및 도로 안전 시장 분석",
  "base_year": 2024
}
```

**Response:** `201 Created`

```json
{
  "data": {
    "id": "mkt_abc123",
    "name": "터널 안전 시장 2024",
    "description": "국내 터널 및 도로 안전 시장 분석",
    "base_year": 2024,
    "status": "draft",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

### 2.4 TAM/SAM/SOM 계산

```http
POST /api/v1/market/{market_id}/calculate
```

**Request Body:**

```json
{
  "method": "top_down",
  "params": {
    "tam": {
      "total_infrastructure_budget": 500000,
      "safety_allocation_ratio": 0.05,
      "tunnel_road_ratio": 0.30
    },
    "sam": {
      "technology_applicable_ratio": 0.40,
      "region_focus_ratio": 1.0
    },
    "som": {
      "market_share_target": 0.10,
      "time_horizon_years": 5,
      "yearly_penetration_rate": 0.30
    }
  },
  "save": true
}
```

**Response:**

```json
{
  "data": {
    "tam": {
      "value": 7500,
      "unit": "억원",
      "calculation": "500,000 × 0.05 × 0.30 = 7,500"
    },
    "sam": {
      "value": 3000,
      "unit": "억원",
      "calculation": "7,500 × 0.40 × 1.0 = 3,000"
    },
    "som": {
      "value": 250.27,
      "unit": "억원",
      "calculation": "3,000 × 0.10 × (1 - 0.7^5) = 250.27"
    },
    "summary": {
      "tam_to_sam_ratio": 0.40,
      "sam_to_som_ratio": 0.083,
      "realistic_assessment": "보수적인 추정치"
    }
  }
}
```

### 2.5 근거 자료 추가

```http
POST /api/v1/market/{market_id}/evidence
```

**Request Body:**

```json
{
  "evidence_type": "accident_stat",
  "title": "2023년 터널 내 사고 통계",
  "description": "터널 내 직광으로 인한 사고 건수",
  "data_value": "연간 1,200건",
  "data_year": 2023,
  "data_source": "도로교통공단",
  "source_url": "https://taas.koroad.or.kr/...",
  "reliability": "high"
}
```

**Response:** `201 Created`

```json
{
  "data": {
    "id": "evd_xyz789",
    "market_id": "mkt_abc123",
    "evidence_type": "accident_stat",
    "title": "2023년 터널 내 사고 통계",
    "data_value": "연간 1,200건",
    "reliability": "high",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### 2.6 성장 예측 생성

```http
POST /api/v1/market/{market_id}/projections
```

**Request Body:**

```json
{
  "cagr": 0.125,
  "years": 10,
  "base_metric": "tam"
}
```

**Response:**

```json
{
  "data": {
    "projections": [
      { "year": 2024, "value": 7500.00 },
      { "year": 2025, "value": 8437.50 },
      { "year": 2026, "value": 9492.19 },
      { "year": 2027, "value": 10678.71 },
      { "year": 2028, "value": 12013.55 },
      { "year": 2029, "value": 13515.24 },
      { "year": 2030, "value": 15204.65 },
      { "year": 2031, "value": 17105.23 },
      { "year": 2032, "value": 19243.38 },
      { "year": 2033, "value": 21648.80 },
      { "year": 2034, "value": 24354.90 }
    ],
    "cagr_percent": 12.5,
    "total_growth_percent": 224.73,
    "unit": "억원"
  }
}
```

### 2.7 1-Pager 내보내기

```http
GET /api/v1/market/{market_id}/export/onepager?format=pdf
```

**Query Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| format | string | No | pdf, png (default: pdf) |
| template | string | No | investor, internal (default: investor) |

**Response:** Binary file (application/pdf)

---

## 3. 정책 트래킹 API (Policy)

### 3.1 키워드 목록 조회

```http
GET /api/v1/policy/keywords
```

**Response:**

```json
{
  "data": [
    {
      "id": "kw_001",
      "keyword": "터널",
      "category": "direct",
      "weight": 3.0,
      "is_active": true,
      "match_count": 45
    },
    {
      "id": "kw_002",
      "keyword": "도로안전",
      "category": "direct",
      "weight": 3.0,
      "is_active": true,
      "match_count": 32
    }
  ]
}
```

### 3.2 키워드 추가

```http
POST /api/v1/policy/keywords
```

**Request Body:**

```json
{
  "keyword": "스마트터널",
  "category": "infrastructure",
  "weight": 2.5
}
```

**Response:** `201 Created`

### 3.3 정책 목록 조회

```http
GET /api/v1/policy/items
```

**Query Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| page | int | No | 페이지 번호 |
| page_size | int | No | 페이지 크기 |
| source_org | string | No | 출처 기관 필터 |
| min_grade | int | No | 최소 연관성 등급 (1-5) |
| is_bookmarked | bool | No | 북마크 필터 |
| from_date | string | No | 시작일 (YYYY-MM-DD) |
| to_date | string | No | 종료일 (YYYY-MM-DD) |

**Response:**

```json
{
  "data": [
    {
      "id": "pol_abc123",
      "title": "2024년 도로안전 종합대책 발표",
      "source_org": "국토교통부",
      "policy_type": "plan",
      "source_url": "https://molit.go.kr/...",
      "published_at": "2024-01-10T09:00:00Z",

      "summary": "국토부가 터널 및 도로 안전 강화를 위한 종합대책을 발표. AI 기반 위험 감지 시스템 도입 확대 계획 포함.",

      "relevance": {
        "score": 15.5,
        "grade": 5,
        "label": "매우 높음",
        "matched_keywords": ["터널", "도로안전", "AI", "위험"]
      },

      "is_bookmarked": true,
      "is_read": true,
      "tags": ["중요", "기회"],

      "crawled_at": "2024-01-10T10:30:00Z"
    }
  ],
  "pagination": { ... }
}
```

### 3.4 정책 상세 조회

```http
GET /api/v1/policy/items/{policy_id}
```

**Response:**

```json
{
  "data": {
    "id": "pol_abc123",
    "title": "2024년 도로안전 종합대책 발표",
    "source_org": "국토교통부",
    "source_type": "ministry",
    "policy_type": "plan",
    "source_url": "https://molit.go.kr/...",
    "published_at": "2024-01-10T09:00:00Z",

    "content_raw": "국토교통부는 10일 터널 및 도로 안전 강화를 위한...(생략)...",

    "summary": "국토부가 터널 및 도로 안전 강화를 위한 종합대책을 발표...",

    "ai_analysis": {
      "key_points": [
        "2024년 터널 안전시설 투자 500억원 확대",
        "AI 기반 위험 감지 시스템 시범 도입 10개소",
        "노후 터널 정밀 안전진단 의무화"
      ],
      "opportunities": [
        "AI 위험 감지 시스템 시범사업 참여 기회",
        "터널 안전시설 교체 수요 증가"
      ],
      "risks": [
        "대기업 중심 발주 가능성"
      ],
      "actions": [
        "국토부 담당 부서 접촉",
        "시범사업 공모 일정 확인"
      ],
      "related_to_us": "직접 연관 - Lux-Guard 직광 위험 감지 기술 적용 가능"
    },

    "relevance": {
      "score": 15.5,
      "grade": 5,
      "label": "매우 높음",
      "factors": {
        "keyword_score": 8.5,
        "authority_weight": 1.5,
        "type_weight": 1.5
      },
      "matched_keywords": ["터널", "도로안전", "AI", "위험"]
    },

    "is_bookmarked": true,
    "is_read": true,
    "user_notes": "시범사업 공모 시 반드시 지원할 것",
    "tags": ["중요", "기회", "시범사업"],

    "crawled_at": "2024-01-10T10:30:00Z",
    "analyzed_at": "2024-01-10T10:35:00Z"
  }
}
```

### 3.5 AI 요약 요청

```http
POST /api/v1/policy/items/{policy_id}/summarize
```

**Request Body:**

```json
{
  "force_refresh": false,
  "analysis_depth": "detailed"
}
```

**Response:**

```json
{
  "data": {
    "summary": "국토부가 터널 및 도로 안전 강화를 위한 종합대책을 발표...",
    "ai_analysis": {
      "key_points": [...],
      "opportunities": [...],
      "risks": [...],
      "actions": [...]
    },
    "model_used": "gpt-4",
    "analyzed_at": "2024-01-15T11:00:00Z"
  }
}
```

### 3.6 정책 타임라인

```http
GET /api/v1/policy/timeline
```

**Query Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| from_date | string | No | 시작일 |
| to_date | string | No | 종료일 |
| min_grade | int | No | 최소 연관성 등급 |

**Response:**

```json
{
  "data": {
    "timeline": [
      {
        "date": "2024-01-10",
        "items": [
          {
            "id": "pol_abc123",
            "title": "2024년 도로안전 종합대책 발표",
            "source_org": "국토교통부",
            "grade": 5
          }
        ]
      },
      {
        "date": "2024-01-08",
        "items": [...]
      }
    ],
    "date_range": {
      "from": "2024-01-01",
      "to": "2024-01-15"
    }
  }
}
```

---

## 4. 기술 Radar API (Tech)

### 4.1 Radar 데이터 조회

```http
GET /api/v1/tech/radar
```

**Response:**

```json
{
  "data": {
    "quadrants": [
      { "id": "techniques", "name": "Techniques" },
      { "id": "tools", "name": "Tools" },
      { "id": "platforms", "name": "Platforms" },
      { "id": "languages", "name": "Languages & Frameworks" }
    ],
    "rings": [
      { "id": "adopt", "name": "Adopt", "color": "#5BA300" },
      { "id": "trial", "name": "Trial", "color": "#009EB0" },
      { "id": "assess", "name": "Assess", "color": "#C7BA00" },
      { "id": "hold", "name": "Hold", "color": "#E09B96" }
    ],
    "items": [
      {
        "id": "tech_001",
        "name": "Computer Vision for Safety",
        "quadrant": "techniques",
        "ring": "adopt",
        "is_new": false,
        "description": "컴퓨터 비전 기반 안전 위험 감지"
      },
      {
        "id": "tech_002",
        "name": "LiDAR Sensing",
        "quadrant": "tools",
        "ring": "trial",
        "is_new": true,
        "description": "LiDAR 기반 거리/깊이 측정"
      },
      {
        "id": "tech_003",
        "name": "Edge AI",
        "quadrant": "platforms",
        "ring": "assess",
        "is_new": true,
        "description": "엣지 디바이스에서의 AI 추론"
      }
    ]
  }
}
```

### 4.2 기술 상세 조회

```http
GET /api/v1/tech/{tech_id}
```

**Response:**

```json
{
  "data": {
    "id": "tech_001",
    "name": "Computer Vision for Safety",
    "description": "컴퓨터 비전 기반 안전 위험 감지 기술",

    "quadrant": "techniques",
    "ring": "adopt",
    "is_new": false,

    "evaluation": {
      "maturity_score": 0.85,
      "adoption_rate": 0.70,
      "our_experience": 0.90,
      "strategic_fit": 0.95,
      "risk_level": 0.15,
      "calculated_ring": "adopt"
    },

    "replaceability": {
      "is_replaceable": false,
      "score": 0.25,
      "analysis": "독자적 알고리즘과 학습 데이터로 대체 어려움"
    },

    "our_position": "핵심 기술 - Lux-Guard의 직광 감지 알고리즘에 적용",

    "history": [
      {
        "date": "2023-06-01",
        "previous_ring": "trial",
        "new_ring": "adopt",
        "reason": "프로덕션 안정성 검증 완료"
      }
    ],

    "resources": [
      {
        "type": "paper",
        "title": "Deep Learning for Traffic Safety",
        "url": "https://arxiv.org/...",
        "published_at": "2023-09-15"
      }
    ],

    "created_at": "2023-01-15T10:00:00Z",
    "updated_at": "2024-01-10T15:00:00Z"
  }
}
```

### 4.3 기술 추가

```http
POST /api/v1/tech
```

**Request Body:**

```json
{
  "name": "Thermal Imaging",
  "description": "열화상 기반 이상 감지",
  "quadrant": "tools",

  "evaluation": {
    "maturity_score": 0.60,
    "adoption_rate": 0.40,
    "our_experience": 0.20,
    "strategic_fit": 0.70,
    "risk_level": 0.30
  }
}
```

**Response:** `201 Created`

```json
{
  "data": {
    "id": "tech_004",
    "name": "Thermal Imaging",
    "quadrant": "tools",
    "ring": "assess",
    "calculated_ring": "assess",
    "is_new": true
  }
}
```

### 4.4 Ring 변경

```http
PUT /api/v1/tech/{tech_id}/ring
```

**Request Body:**

```json
{
  "new_ring": "trial",
  "reason": "파일럿 프로젝트 성공적 완료"
}
```

**Response:**

```json
{
  "data": {
    "id": "tech_004",
    "previous_ring": "assess",
    "new_ring": "trial",
    "reason": "파일럿 프로젝트 성공적 완료",
    "changed_at": "2024-01-15T11:00:00Z"
  }
}
```

---

## 5. 경쟁사 분석 API (Competitor)

### 5.1 경쟁사 목록 조회

```http
GET /api/v1/competitors
```

**Response:**

```json
{
  "data": [
    {
      "id": "comp_001",
      "name": "A사",
      "country": "한국",
      "competitor_type": "direct",
      "website": "https://a-company.co.kr",

      "positioning": {
        "price": 0.7,
        "technology": 0.6,
        "quality": 0.7,
        "coverage": 0.8,
        "innovation": 0.5,
        "service": 0.6
      },

      "summary": {
        "strengths_count": 3,
        "weaknesses_count": 2
      }
    }
  ]
}
```

### 5.2 경쟁사 상세 조회

```http
GET /api/v1/competitors/{competitor_id}
```

**Response:**

```json
{
  "data": {
    "id": "comp_001",
    "name": "A사",
    "name_en": "A Company",
    "country": "한국",
    "website": "https://a-company.co.kr",
    "logo_url": null,

    "competitor_type": "direct",
    "description": "터널 안전 모니터링 시스템 전문 기업",
    "approach_difference": "하드웨어 중심 접근, 센서 자체 개발",

    "positioning": {
      "price": 0.7,
      "technology": 0.6,
      "quality": 0.7,
      "coverage": 0.8,
      "innovation": 0.5,
      "service": 0.6
    },

    "swot": {
      "strengths": [
        "공공 프로젝트 수주 경험 풍부",
        "자체 센서 기술 보유",
        "전국 A/S 네트워크"
      ],
      "weaknesses": [
        "AI 기술력 부족",
        "높은 하드웨어 의존도"
      ],
      "opportunities": [
        "정부 안전 투자 확대"
      ],
      "threats": [
        "AI 스타트업 진입"
      ]
    },

    "data_confidence": "medium",
    "last_updated": "2024-01-10",

    "created_at": "2023-06-01T10:00:00Z",
    "updated_at": "2024-01-10T15:00:00Z"
  }
}
```

### 5.3 기능 비교 매트릭스

```http
GET /api/v1/competitors/matrix
```

**Response:**

```json
{
  "data": {
    "features": [
      {
        "id": "feat_001",
        "name": "실시간 위험 감지",
        "category": "core",
        "weight": 1.0,
        "is_differentiator": true
      },
      {
        "id": "feat_002",
        "name": "AI 분석",
        "category": "core",
        "weight": 0.9,
        "is_differentiator": true
      },
      {
        "id": "feat_003",
        "name": "대시보드",
        "category": "ui",
        "weight": 0.7,
        "is_differentiator": false
      }
    ],

    "our_scores": {
      "feat_001": { "score": 2, "notes": "자체 알고리즘" },
      "feat_002": { "score": 2, "notes": "딥러닝 기반" },
      "feat_003": { "score": 1, "notes": "개발 중" }
    },

    "competitor_scores": {
      "comp_001": {
        "feat_001": { "score": 1, "notes": "센서 기반" },
        "feat_002": { "score": 0, "notes": "없음" },
        "feat_003": { "score": 2, "notes": "완성도 높음" }
      },
      "comp_002": {
        "feat_001": { "score": 2, "notes": "" },
        "feat_002": { "score": 1, "notes": "규칙 기반" },
        "feat_003": { "score": 2, "notes": "" }
      }
    },

    "summary": {
      "our_total_score": 78.5,
      "competitor_scores": {
        "comp_001": 62.3,
        "comp_002": 71.0
      },
      "differentiators": ["실시간 위험 감지", "AI 분석"],
      "gaps": [
        {
          "feature": "대시보드",
          "competitor": "comp_001",
          "gap": 1
        }
      ]
    }
  }
}
```

### 5.4 포지셔닝 맵 데이터

```http
GET /api/v1/competitors/positioning
```

**Query Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| x_axis | string | No | X축 지표 (default: technology) |
| y_axis | string | No | Y축 지표 (default: price) |

**Response:**

```json
{
  "data": {
    "axes": {
      "x": { "name": "technology", "label": "기술 수준" },
      "y": { "name": "price", "label": "가격대" }
    },

    "positions": [
      {
        "id": "us",
        "name": "Lux-Guard (우리)",
        "x": 85.0,
        "y": 50.0,
        "is_us": true
      },
      {
        "id": "comp_001",
        "name": "A사",
        "x": 60.0,
        "y": 70.0,
        "is_us": false
      },
      {
        "id": "comp_002",
        "name": "B사",
        "x": 70.0,
        "y": 65.0,
        "is_us": false
      }
    ],

    "quadrant_labels": {
      "top_right": "고가/고기술",
      "top_left": "고가/저기술",
      "bottom_right": "저가/고기술",
      "bottom_left": "저가/저기술"
    }
  }
}
```

---

## 6. 이해관계자 API (Stakeholder)

### 6.1 이해관계자 목록 조회

```http
GET /api/v1/stakeholders
```

**Response:**

```json
{
  "data": [
    {
      "id": "stk_001",
      "name": "김부장",
      "title": "도로정책과장",
      "organization": "국토교통부",
      "power_level": 4,
      "interest_level": 5,
      "strategy": "manage_closely",
      "priority": 1
    }
  ]
}
```

### 6.2 Power-Interest Grid

```http
GET /api/v1/stakeholders/power-grid
```

**Response:**

```json
{
  "data": {
    "grid": {
      "manage_closely": [
        {
          "id": "stk_001",
          "name": "김부장",
          "organization": "국토교통부",
          "power": 4,
          "interest": 5
        }
      ],
      "keep_satisfied": [
        {
          "id": "stk_002",
          "name": "이사장",
          "organization": "한국도로공사",
          "power": 5,
          "interest": 2
        }
      ],
      "keep_informed": [...],
      "monitor": [...]
    },

    "statistics": {
      "total": 15,
      "by_strategy": {
        "manage_closely": 3,
        "keep_satisfied": 4,
        "keep_informed": 5,
        "monitor": 3
      }
    }
  }
}
```

### 6.3 관계 그래프 데이터

```http
GET /api/v1/stakeholders/graph
```

**Response:**

```json
{
  "data": {
    "nodes": [
      {
        "id": "stk_001",
        "name": "김부장",
        "type": "individual",
        "organization": "국토교통부",
        "power": 4,
        "interest": 5,
        "size": 40
      },
      {
        "id": "org_001",
        "name": "국토교통부",
        "type": "organization",
        "org_type": "government",
        "size": 60
      }
    ],

    "edges": [
      {
        "source": "stk_001",
        "target": "org_001",
        "type": "works_at",
        "strength": 1.0
      },
      {
        "source": "stk_001",
        "target": "stk_002",
        "type": "influences",
        "strength": 0.7
      }
    ],

    "influence_scores": {
      "stk_001": 85.5,
      "stk_002": 72.3,
      "org_001": 95.0
    }
  }
}
```

### 6.4 관계 추가

```http
POST /api/v1/stakeholders/relations
```

**Request Body:**

```json
{
  "from_stakeholder_id": "stk_001",
  "to_stakeholder_id": "stk_003",
  "relation_type": "influences",
  "strength": 0.8,
  "description": "예산 배정에 영향력 행사"
}
```

---

## 7. Timing Thesis API

### 7.1 Factor 목록 조회

```http
GET /api/v1/timing/factors
```

**Response:**

```json
{
  "data": [
    {
      "id": "tf_001",
      "name": "AI 기술 성숙",
      "category": "technology",
      "trend_direction": "accelerating",
      "maturity_level": 0.85,
      "impact_score": 0.9,
      "confidence": 0.85,

      "window": {
        "start": "2022-01-01",
        "peak": "2025-06-01",
        "end": "2028-12-31"
      },

      "current_state": "딥러닝 기반 컴퓨터 비전이 실용화 단계에 진입"
    }
  ]
}
```

### 7.2 Timing Score 계산

```http
GET /api/v1/timing/score
```

**Query Parameters:**

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| reference_date | string | No | 기준일 (default: today) |

**Response:**

```json
{
  "data": {
    "total_score": 0.78,
    "grade": "GOOD",
    "message": "좋은 타이밍, 실행 권장",

    "factor_scores": [
      {
        "factor_id": "tf_001",
        "name": "AI 기술 성숙",
        "category": "technology",
        "score": 0.85,
        "position": "in_window"
      },
      {
        "factor_id": "tf_002",
        "name": "정책 압박 강화",
        "category": "policy",
        "score": 0.72,
        "position": "in_window"
      }
    ],

    "reference_date": "2024-01-15"
  }
}
```

### 7.3 Thesis 생성 (AI)

```http
POST /api/v1/timing/thesis/generate
```

**Request Body:**

```json
{
  "product_name": "Lux-Guard",
  "product_description": "AI 기반 터널 직광 위험 감지 시스템",
  "industry_name": "터널/도로 안전",
  "target_audience": "investor",
  "factor_ids": ["tf_001", "tf_002", "tf_003"]
}
```

**Response:**

```json
{
  "data": {
    "thesis_statement": "터널/도로 안전 시장은 예전에도 존재했지만, Lux-Guard가 지금에서야 가능해진 이유는 AI 기술의 성숙, 정부 안전 규제 강화, 그리고 노후 인프라 증가 때문입니다.",

    "one_liner": "AI 성숙 + 정책 압박 + 인프라 노후화 = 지금이 최적의 타이밍",

    "evidences": [
      {
        "factor": "AI 기술 성숙",
        "explanation": "딥러닝 기반 컴퓨터 비전이 실용화 단계에 진입하여 실시간 위험 감지가 가능해짐",
        "data_point": "이미지 인식 정확도 99% 이상 달성 (2023년)"
      },
      {
        "factor": "정부 안전 규제 강화",
        "explanation": "연이은 터널 사고로 정부가 강력한 안전 대책 추진",
        "data_point": "2024년 터널 안전 예산 30% 증가"
      }
    ],

    "risk": "경기 침체로 인한 공공 투자 축소 가능성",

    "metadata": {
      "model_used": "gpt-4",
      "generated_at": "2024-01-15T12:00:00Z",
      "confidence": 0.82
    }
  }
}
```

### 7.4 Thesis 1-Pager 내보내기

```http
GET /api/v1/timing/export/onepager?format=pdf&thesis_id=th_001
```

**Response:** Binary file (application/pdf)

---

## 8. 대시보드 API

### 8.1 Dashboard Health Score

```http
GET /api/v1/dashboard/health
```

**Response:**

```json
{
  "data": {
    "total_score": 72.5,
    "grade": "B",
    "status": "대부분 준비됨, 일부 보완 필요",

    "breakdown": {
      "market_clarity": {
        "score": 85,
        "label": "시장 규모",
        "status": "good"
      },
      "competitive_awareness": {
        "score": 70,
        "label": "경쟁 인식",
        "status": "good"
      },
      "timing_readiness": {
        "score": 78,
        "label": "타이밍",
        "status": "good"
      },
      "policy_tracking": {
        "score": 60,
        "label": "정책 트래킹",
        "status": "warning"
      },
      "stakeholder_mapping": {
        "score": 55,
        "label": "이해관계자",
        "status": "warning"
      }
    },

    "recommendations": [
      "정책 모니터링 키워드 추가 필요",
      "핵심 이해관계자 파악 및 관계 구축 필요"
    ],

    "recent_updates": [
      {
        "type": "policy",
        "title": "새 정책 3건 수집됨",
        "timestamp": "2024-01-15T10:00:00Z"
      }
    ],

    "last_calculated": "2024-01-15T12:00:00Z"
  }
}
```

### 8.2 Dashboard Summary

```http
GET /api/v1/dashboard/summary
```

**Response:**

```json
{
  "data": {
    "market": {
      "tam": "7,500억원",
      "som": "250억원",
      "cagr": "12.5%"
    },

    "policy": {
      "total_tracked": 45,
      "high_relevance": 5,
      "this_week": 3
    },

    "competitors": {
      "total": 8,
      "direct": 3,
      "our_rank": 2
    },

    "stakeholders": {
      "total": 15,
      "key_decision_makers": 4,
      "strong_relationships": 2
    },

    "timing": {
      "score": 0.78,
      "grade": "GOOD",
      "message": "좋은 타이밍"
    },

    "alerts": [
      {
        "type": "policy",
        "severity": "high",
        "message": "국토부 안전 정책 발표 - 연관성 매우 높음",
        "link": "/policy/pol_abc123"
      }
    ]
  }
}
```

---

## 9. 내보내기 API

### 9.1 종합 보고서 내보내기

```http
POST /api/v1/export/report
```

**Request Body:**

```json
{
  "report_type": "investor_deck",
  "format": "pdf",
  "sections": [
    "market_size",
    "timing_thesis",
    "competitive_analysis",
    "team"
  ],
  "options": {
    "include_sources": true,
    "language": "ko"
  }
}
```

**Response:**

```json
{
  "data": {
    "job_id": "job_abc123",
    "status": "processing",
    "estimated_seconds": 30
  }
}
```

### 9.2 내보내기 상태 확인

```http
GET /api/v1/export/status/{job_id}
```

**Response:**

```json
{
  "data": {
    "job_id": "job_abc123",
    "status": "completed",
    "download_url": "/api/v1/export/download/job_abc123",
    "expires_at": "2024-01-15T13:00:00Z",
    "file_size": 2048576
  }
}
```

---

## 10. Webhook 설정 API

### 10.1 알림 설정 조회

```http
GET /api/v1/notifications/settings
```

**Response:**

```json
{
  "data": [
    {
      "id": "ns_001",
      "notification_type": "policy_new",
      "channel": "slack",
      "config": {
        "webhook_url": "https://hooks.slack.com/...",
        "channel": "#ceo-alerts"
      },
      "is_active": true,
      "filters": {
        "min_grade": 4
      }
    }
  ]
}
```

### 10.2 알림 설정 생성

```http
POST /api/v1/notifications/settings
```

**Request Body:**

```json
{
  "notification_type": "policy_new",
  "channel": "email",
  "config": {
    "address": "ceo@company.com"
  },
  "filters": {
    "min_grade": 4,
    "source_orgs": ["국토교통부", "행정안전부"]
  }
}
```

---

## 부록: 에러 코드

| 코드 | HTTP Status | 설명 |
|------|-------------|------|
| VALIDATION_ERROR | 400 | 입력 데이터 유효성 검증 실패 |
| UNAUTHORIZED | 401 | 인증 필요 |
| FORBIDDEN | 403 | 권한 없음 |
| NOT_FOUND | 404 | 리소스 없음 |
| CONFLICT | 409 | 중복 데이터 |
| RATE_LIMITED | 429 | 요청 제한 초과 |
| AI_ERROR | 502 | AI API 호출 실패 |
| INTERNAL_ERROR | 500 | 서버 내부 오류 |
