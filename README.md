# bringengineering1008

터널 직광위험 MVP 백엔드 스켈레톤입니다. FastAPI 기반으로 주요 엔드포인트 골격과 위험도 계산 유틸리티가 포함되어 있습니다.

## 구성

- `backend/app/main.py` – FastAPI 엔드포인트 정의
- `backend/app/schemas.py` – 요청/응답 및 계산에 필요한 Pydantic 스키마
- `backend/app/services.py` – Sg, St, Risk% 계산 로직
- `backend/app/config.py` – 환경 변수 기반 설정 로딩
- `backend/requirements.txt` – 백엔드 의존성 목록
- `.env.example` – API 키 템플릿

## 실행 방법

1. Python 3.11 이상 환경에서 의존성 설치

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. 루트 디렉터리에 `.env` 파일 생성 후 발급받은 API 키 입력

   ```bash
   cp ../.env.example ../.env
   # 편집기로 실제 키 입력
   ```

3. 개발 서버 실행

   ```bash
   uvicorn app.main:app --reload
   ```

4. 브라우저에서 `http://127.0.0.1:8000/docs` 접속하여 OpenAPI 문서를 통해 엔드포인트를 확인할 수 있습니다.

## 다음 단계 제안

- 실제 공공 API 연동 및 응답 캐싱 로직 구현
- PostGIS 연동 후 터널/관측소 조회 API 확장
- PDF 리포트 생성(WeasyPrint 등) 추가
- 인증/로깅/모니터링 구성
