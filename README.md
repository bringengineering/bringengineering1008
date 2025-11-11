# bringengineering1008

터널 직광위험 MVP 백엔드 스켈레톤입니다. FastAPI 기반으로 주요 엔드포인트 골격과 위험도 계산 유틸리티가 포함되어 있습니다.

## 구성

- `backend/app/main.py` – FastAPI 엔드포인트 정의
- `backend/app/schemas.py` – 요청/응답 및 계산에 필요한 Pydantic 스키마
- `backend/app/services.py` – Sg, St, Risk% 계산 로직
- `backend/app/config.py` – 환경 변수 기반 설정 로딩
- `backend/requirements.txt` – 백엔드 의존성 목록
- `.env.example` – API 키 및 엔드포인트 템플릿

## 실행 방법

1. Python 3.11 이상 환경에서 의존성 설치

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. 루트 디렉터리에 `.env` 파일 생성 후 발급받은 API 키와 엔드포인트 입력

   ```bash
   cp ../.env.example ../.env
   # 편집기로 실제 키 입력
   ```

   필수 항목:

   | 변수 | 설명 |
   | --- | --- |
   | `ROAD_CORP_API_KEY` | 한국도로공사 OpenAPI 서비스 키 |
   | `ROAD_CORP_ENDPOINT` | 교통량 API URL (예: `https://openapi.ex.co.kr/...`) |
   | `KMA_API_KEY` | 기상청 OpenAPI 서비스 키 |
   | `KMA_WEATHER_ENDPOINT` | 기상청 API URL |
   | `KASI_API_KEY` | 한국천문연구원 서비스 키 |
   | `KASI_SOLAR_ENDPOINT` | 태양고도 API URL |
   | `HTTP_TIMEOUT` | 외부 API 타임아웃(초) |

3. 개발 서버 실행

   ```bash
   uvicorn app.main:app --reload
   ```

4. 브라우저에서 `http://127.0.0.1:8000/docs` 접속하여 OpenAPI 문서를 통해 엔드포인트를 확인할 수 있습니다.

## 주요 엔드포인트

| 메서드 | 경로 | 설명 |
| --- | --- | --- |
| `GET` | `/api/solar` | 설정된 KASI 태양고도 API 프록시. 위도/경도, 날짜를 받아 원본 응답을 반환합니다. |
| `GET` | `/api/traffic` | 한국도로공사 교통량 API 프록시. 스테이션 ID와 날짜를 받아 원본 응답을 반환합니다. |
| `GET` | `/api/weather` | 기상청 날씨 API 프록시. 스테이션 ID와 날짜를 받아 원본 응답을 반환합니다. |
| `POST` | `/api/risk` | 입력된 태양/교통/기상 시계열로 직광 위험도를 계산합니다. |

각 프록시는 네트워크 오류나 인증 실패 시 502 에러를 반환하며, `_type=json`/`dataType=JSON` 파라미터를 자동으로 포함해 JSON 응답을 우선 시도합니다.

## 다음 단계 제안

- PostGIS 연동 후 터널/관측소 조회 API 확장
- 프록시 응답 캐싱 및 재시도 로직 추가
- PDF 리포트 생성(WeasyPrint 등) 추가
- 인증/로깅/모니터링 구성
