# Conversation-to-Diagram MVP

## 핵심 컨셉
AI와의 대화를 실시간으로 구조화/도식화하는 "사고 시각화 엔진"

## 타겟 사용자
- 프로젝트 리더 (R&D, 엔지니어링, 스타트업)
- 기술 컨설턴트
- 정부과제/제안서 작성자

## 핵심 기능 (MVP)

### 1. 분할 화면 인터페이스
```
┌─────────────────────────────────────┐
│   [좌측: 채팅]   │  [우측: 도식]   │
│                  │                  │
│  대화 입력창      │  실시간 트리맵   │
│  메시지 히스토리  │  계층 구조       │
│                  │  (L1→L2→L3→L4)  │
└─────────────────────────────────────┘
```

### 2. 구조 추출 엔진
**입력**: 자연어 대화
**처리**: LLM이 대화를 분석하여 구조 JSON 생성
**출력**: 계층적 노드 트리

#### 구조 스키마
```typescript
interface ConversationStructure {
  nodes: Node[]
  edges: Edge[]
  metadata: {
    projectGoal: string    // L1: 프로젝트 목적
    lastUpdated: string
    version: number
  }
}

interface Node {
  id: string
  type: 'goal' | 'strategy' | 'tactic' | 'action'  // L1~L4
  level: 1 | 2 | 3 | 4
  label: string
  description?: string
  status?: 'proposed' | 'decided' | 'deprecated'
  relatedMessages: string[]  // 참조 메시지 ID
}
```

### 3. 실시간 업데이트 규칙

#### Anchor 규칙 (안정성)
- **L1 (목표/문제정의)**: 쉽게 변경되지 않음
  - 변경 시 사용자 확인 필요
  - 이전 버전 자동 저장
- **L2-L4**: 대화에 따라 유연하게 업데이트

#### 업데이트 모드
1. **Append**: 새 노드 추가
2. **Update**: 기존 노드 수정
3. **Merge**: 유사 개념 병합
4. **Archive**: 폐기된 아이디어 보관

### 4. 도식화 타입 (Phase 1: 트리형)
```
[L1] 프로젝트 목표
  ├── [L2] 기술 전략
  │   ├── [L3] 백엔드 아키텍처
  │   │   └── [L4] API 설계
  │   └── [L3] 프론트엔드
  ├── [L2] 사업 전략
  │   └── [L3] 타겟 고객
  └── [L2] 제약 조건
```

### 5. Export 기능
- **PNG**: 다이어그램 이미지
- **Markdown**: 구조화된 문서
- **JSON**: 전체 구조 데이터

## 기술 스택

### Frontend
- **Next.js 14** (App Router, TypeScript)
- **React Flow**: 도식화 라이브러리
- **Tailwind CSS**: 스타일링
- **Zustand**: 상태 관리
- **react-markdown**: 메시지 렌더링

### Backend/API
- **Next.js API Routes**: `/api/chat`
- **Anthropic Claude API**: 구조 추출
- **SSE (Server-Sent Events)**: 실시간 스트리밍

### Storage (MVP는 브라우저 로컬)
- **localStorage**: 대화 및 구조 저장
- (향후: PostgreSQL + Vector DB)

## 프로젝트 구조
```
conversation-diagram/
├── src/
│   ├── app/
│   │   ├── page.tsx              # 메인 페이지
│   │   ├── layout.tsx
│   │   └── api/
│   │       └── chat/
│   │           └── route.ts      # 채팅 API
│   ├── components/
│   │   ├── ChatPanel.tsx         # 좌측 채팅
│   │   ├── DiagramPanel.tsx      # 우측 도식
│   │   ├── MessageList.tsx
│   │   ├── InputBox.tsx
│   │   └── StructureTree.tsx     # React Flow 기반
│   ├── lib/
│   │   ├── anthropic.ts          # Claude API 클라이언트
│   │   ├── structure-extractor.ts # 구조 추출 로직
│   │   └── types.ts              # TypeScript 타입
│   └── store/
│       └── conversation-store.ts  # Zustand 스토어
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## 핵심 프롬프트 (구조 추출 엔진)

### System Prompt
```
You are a conversation structure analyzer. Your job is to:

1. Analyze the conversation and extract hierarchical structure
2. Identify:
   - L1: Project goal/problem definition (rarely changes)
   - L2: Strategic approaches (tech, business, constraints)
   - L3: Tactical implementations
   - L4: Specific actions/features

3. Output format: JSON only
   - nodes: array of {id, type, level, label, description}
   - edges: array of {from, to}
   - operation: "add" | "update" | "merge" | "archive"

4. Rules:
   - L1 should be stable and clear
   - New ideas → add nodes
   - Refined ideas → update existing nodes
   - Similar concepts → suggest merge

Output must be valid JSON matching this schema:
{schema here}
```

## 개발 단계

### Phase 1: 기본 UI (1-2일)
- [ ] Next.js 프로젝트 setup
- [ ] 좌우 분할 레이아웃
- [ ] 채팅 입력/출력 컴포넌트
- [ ] 더미 데이터로 React Flow 트리 렌더링

### Phase 2: LLM 통합 (1-2일)
- [ ] Anthropic API 연동
- [ ] 구조 추출 프롬프트 설계
- [ ] JSON 스키마 검증
- [ ] SSE 스트리밍 구현

### Phase 3: 실시간 업데이트 (2-3일)
- [ ] 대화 → 구조 변환 파이프라인
- [ ] 노드 추가/수정/병합 로직
- [ ] L1 안정화 규칙
- [ ] 애니메이션 및 시각적 피드백

### Phase 4: Export & Polish (1일)
- [ ] PNG export (html-to-image)
- [ ] Markdown export
- [ ] 계층 접기/펼치기
- [ ] 로컬 저장

## 성공 지표 (MVP)
- ✅ 3-5턴 대화 후 명확한 L1-L3 구조 생성
- ✅ 도식이 흔들리지 않고 점진적으로 성장
- ✅ Export한 결과물을 발표 자료로 바로 사용 가능
- ✅ 평균 응답 시간 < 3초

## 차별화 포인트
| 기존 도구 | Conversation-to-Diagram |
|-----------|------------------------|
| 정리된 텍스트 입력 | 자유로운 대화 |
| 단발성 생성 | 실시간 구조 진화 |
| 예쁜 다이어그램 | 사고 과정 추적 |
| 결과물 중심 | 히스토리 포함 |

## 다음 단계 (MVP 이후)
1. 마인드맵/플로우차트 타입 추가
2. 다중 프로젝트 관리
3. 협업 기능 (멀티플레이어)
4. PPT 자동 생성
5. 음성 입력 지원
