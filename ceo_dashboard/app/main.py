"""
CEO Strategic Analysis Dashboard
5개 산업 지원 Multi-Industry Version

산업:
1. 건설 및 인프라 자산 관리 (Civil Engineering & Asset Management)
2. 보험 및 리스크 금융 (Insurance & Risk Finance)
3. 물류 및 공급망 관리 (Logistics & SCM)
4. AI 및 데이터 엔지니어링 (AI & Data Science)
5. 공공 행정 및 법률 (Public Affairs & Law)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 생명주기 관리"""
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print("📊 5개 산업 분석 지원:")
    print("   - civil_infra: 건설 및 인프라 자산 관리")
    print("   - insurance_risk: 보험 및 리스크 금융")
    print("   - logistics_scm: 물류 및 공급망 관리")
    print("   - ai_data: AI 및 데이터 엔지니어링")
    print("   - public_law: 공공 행정 및 법률")
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## CEO 전략 분석 대시보드

대표가 "판을 설명하는 보고서"를 머릿속에 항상 갖고 있을 수 있도록 지원하는 도구.

### 지원 산업 (5개)

| 코드 | 산업명 | 설명 |
|------|--------|------|
| `civil_infra` | 건설 및 인프라 | BIM, 시설물 안전, 노후 시설물 |
| `insurance_risk` | 보험 및 리스크 금융 | 지수보험, 재보험, 언더라이팅 |
| `logistics_scm` | 물류 및 공급망 | VPC, 공급망 최적화, 기회비용 |
| `ai_data` | AI 및 데이터 | MLOps, XAI, 디지털 트윈 |
| `public_law` | 공공 행정 및 법률 | 중대재해법, 시설물안전법, G2B |

### 분석 기능 (7종)

1. **산업 구조 분석** - Porter's 5 Forces
2. **시장 규모 계산** - TAM/SAM/SOM
3. **정책 트래킹** - 키워드 기반 연관성 분석
4. **기술 트렌드** - Technology Radar
5. **경쟁사 분석** - 기능 비교 매트릭스
6. **이해관계자 맵** - Power-Interest Grid
7. **Timing Thesis** - "왜 지금인가" 논리

### 사용 예시

```bash
# 산업 목록 조회
GET /api/v1/industries

# 시장 규모 계산
POST /api/v1/industries/civil_infra/market/calculate

# Timing Thesis 생성
POST /api/v1/industries/insurance_risk/timing/thesis
```
""",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router, prefix="/api/v1")


# Health Check
@app.get("/health", tags=["System"])
async def health_check():
    """서버 상태 확인"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/", tags=["System"])
async def root():
    """루트 엔드포인트"""
    return {
        "message": "CEO Strategic Analysis Dashboard API",
        "docs": "/docs",
        "industries": [
            "civil_infra",
            "insurance_risk",
            "logistics_scm",
            "ai_data",
            "public_law"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
