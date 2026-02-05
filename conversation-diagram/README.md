# Conversation to Diagram

> AI와의 대화를 실시간으로 구조화/도식화하는 **사고 시각화 엔진**

## 🎯 핵심 컨셉

기존 도구들은 "정리된 텍스트 → 다이어그램"을 생성합니다.
하지만 **Conversation to Diagram**은 **"자유로운 대화 → 실시간 구조 진화"**를 구현합니다.

### 차별화 포인트

| 기존 도구 (Miro, GenSpark 등) | Conversation to Diagram |
|-------------------------------|-------------------------|
| 정리된 텍스트 입력 필요 | 자유로운 대화 |
| 단발성 생성 | 실시간 구조 진화 |
| 예쁜 다이어그램 | 사고 과정 추적 + 히스토리 |
| 결과물 중심 | 의사결정 과정 포함 |

## 🖥️ 화면 구성

```
┌─────────────────────────────────────────────────┐
│          Conversation to Diagram                │
├─────────────────────┬───────────────────────────┤
│                     │                           │
│   [좌측: 채팅]      │    [우측: 도식화]         │
│                     │                           │
│   • 자유로운 대화    │    • 실시간 트리 구조     │
│   • AI 응답         │    • L1 → L2 → L3 → L4   │
│   • 메시지 히스토리  │    • 계층적 시각화        │
│                     │                           │
└─────────────────────┴───────────────────────────┘
```

## 📊 구조 레벨 (L1 ~ L4)

대화는 자동으로 4단계 계층 구조로 분석됩니다:

- **L1 (Goal)**: 프로젝트 목표, 문제 정의, 핵심 가치
- **L2 (Strategy)**: 전략적 접근 (기술, 사업, 제약조건)
- **L3 (Tactic)**: 전술적 구현 방법
- **L4 (Action)**: 구체적 액션, 기능, 태스크

## 🚀 Quick Start

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 변수 설정

```bash
cp .env.local.example .env.local
```

`.env.local` 파일을 열고 Anthropic API 키를 입력하세요:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

**API 키 발급**: [https://console.anthropic.com/](https://console.anthropic.com/)

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000) 접속

### 4. 대화 시작!

예시:
```
"웹 기반 터널 직광 위험도 분석 시스템을 만들고 싶어요"
```

## 🛠️ 기술 스택

- **Frontend**: Next.js 15 (App Router), React 19, TypeScript
- **Diagram**: React Flow
- **Styling**: Tailwind CSS
- **State**: Zustand (with localStorage persistence)
- **LLM**: Anthropic Claude 3.5 Sonnet
- **Markdown**: react-markdown

## 📁 프로젝트 구조

```
conversation-diagram/
├── app/
│   ├── api/chat/route.ts     # 채팅 API 엔드포인트
│   ├── layout.tsx
│   ├── page.tsx              # 메인 화면
│   └── globals.css
├── components/
│   ├── ChatPanel.tsx         # 좌측 채팅 패널
│   ├── DiagramPanel.tsx      # 우측 도식화 패널
│   └── CustomNode.tsx        # React Flow 커스텀 노드
├── lib/
│   ├── types.ts              # TypeScript 타입 정의
│   └── structure-extractor.ts # 구조 추출 엔진
├── store/
│   └── conversation-store.ts # Zustand 상태 관리
└── package.json
```

## 🎨 주요 기능

### ✅ 구현된 기능 (MVP)

- [x] 좌우 분할 레이아웃 (채팅 + 도식)
- [x] AI와 실시간 대화
- [x] 대화 → 구조 자동 추출 (L1~L4)
- [x] React Flow 기반 계층적 트리 시각화
- [x] localStorage 자동 저장
- [x] Markdown Export
- [x] 대화/구조 초기화

### 🔜 향후 계획

- [ ] PNG/PDF Export
- [ ] 계층 접기/펼치기 UI
- [ ] 마인드맵/플로우차트 타입 추가
- [ ] 다중 프로젝트 관리
- [ ] 협업 기능 (멀티플레이어)
- [ ] PPT 자동 생성
- [ ] 음성 입력 지원

## 💡 사용 예시

### 1단계: 프로젝트 아이디어 던지기
```
User: "웹 기반 터널 직광 위험도 분석 시스템을 만들고 싶어요"
AI: "흥미로운 프로젝트네요! 구체적으로..."
```

→ **L1 노드 생성**: "터널 직광 위험도 분석 시스템"

### 2단계: 세부사항 논의
```
User: "FastAPI 백엔드와 Next.js 프론트엔드로 구성하려고 합니다"
AI: "좋은 선택입니다. 각 레이어별로..."
```

→ **L2 노드 생성**:
- "FastAPI 백엔드 아키텍처"
- "Next.js 프론트엔드"

### 3단계: 구현 방법 구체화
```
User: "PostGIS로 공간 데이터를 다루고, 태양 위치 계산은 Skyfield를 쓸게요"
```

→ **L3 노드 생성**:
- "PostGIS 공간 데이터 처리"
- "Skyfield 태양 위치 계산"

## 🎯 타겟 사용자

- 프로젝트 리더 (R&D, 엔지니어링)
- 기술 컨설턴트
- 정부과제/제안서 작성자
- 스타트업 대표/CTO
- 사고 정리가 필요한 모든 리더

## 🔑 핵심 가치

1. **사고 흐름을 방해하지 않음**: 정리하려고 멈출 필요 없이, 말하면 구조가 됩니다
2. **히스토리 보존**: 왜 이런 결정을 내렸는지 대화 맥락이 남습니다
3. **바로 사용 가능**: Export한 구조도를 발표 자료로 즉시 활용
4. **점진적 진화**: 구조가 흔들리지 않고 대화에 따라 성장합니다

## 📝 License

MIT

## 🤝 Contributing

Pull requests are welcome!

---

**Made with ❤️ for project leaders who think fast**
