# FD HOLDINGS - 아이디어를 산업 자산으로

AI 기반 특허 가능성 분석 및 IP 유통 플랫폼 프로토타입

## 주요 기능

- **아이디어 제출**: NDA 자동 체결, 타임스탬프 기록
- **AI 자동 분석**: KIPRIS 선행기술 조사, 유사도 분석, 특허 가능성 점수화
- **명세서 초안 생성**: 등급 A 이상 시 특허 명세서 자동 생성
- **대시보드**: 제출 현황, 분석 결과 확인

## 기술 스택

- **Frontend**: Next.js 14, React, Tailwind CSS
- **Backend**: Next.js API Routes
- **Database**: Supabase (PostgreSQL)
- **AI**: Claude API (Anthropic)
- **특허 검색**: KIPRIS API

## 설치 및 실행

### 1. 의존성 설치
npm install

### 2. 환경변수 설정
.env.example을 .env.local로 복사하고 API 키 설정

### 3. 데이터베이스 설정
Supabase SQL Editor에서 supabase-schema.sql 실행

### 4. 개발 서버 실행
npm run dev

http://localhost:3000 에서 확인

## 라이선스
© 2024 FD HOLDINGS. All rights reserved.
