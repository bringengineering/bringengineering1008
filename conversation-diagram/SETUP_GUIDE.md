# 🚀 Conversation-to-Diagram 실행 가이드 (초보자용)

> 코딩을 처음 해보는 분도 5-10분 안에 실행할 수 있습니다!

---

## 📋 준비물

1. ✅ 컴퓨터 (Windows, Mac, Linux 모두 가능)
2. ✅ 인터넷 연결
3. ✅ Anthropic API 키 (무료로 받을 수 있음, 아래에서 설명)

---

## 🎯 Step 1: Anthropic API 키 받기 (5분)

### 1-1. 웹사이트 접속
1. 브라우저를 열고 이 주소로 이동: **https://console.anthropic.com/**
2. 계정이 없으면 **"Sign Up"** 클릭해서 회원가입
3. 계정이 있으면 **"Sign In"** 클릭해서 로그인

### 1-2. API 키 생성
1. 로그인 후 왼쪽 메뉴에서 **"API Keys"** 클릭
2. **"Create Key"** 버튼 클릭
3. 이름 입력 (예: "conversation-diagram")
4. **"Create Key"** 클릭
5. 🔑 **중요!** 나타나는 API 키를 복사해서 안전한 곳에 저장하세요!
   - 형태: `sk-ant-api03-...` 이런 식으로 생김
   - 다시 볼 수 없으니 꼭 복사하세요!

### 1-3. 무료 크레딧 확인
- 신규 가입 시 $5 무료 크레딧 제공
- 이 프로젝트는 대화 1회당 약 $0.01-0.05 정도 사용
- 약 100-500회 대화 가능

---

## 💻 Step 2: 터미널(명령창) 열기

### Windows 사용자:
1. 키보드에서 `윈도우 키 + R` 누르기
2. 나타나는 창에 `cmd` 입력 후 엔터
3. 검은색 창이 열림 → 이게 터미널입니다!

### Mac 사용자:
1. `Command + 스페이스` 누르기
2. "터미널" 또는 "terminal" 입력 후 엔터
3. 흰색/검은색 창이 열림 → 이게 터미널입니다!

### Linux 사용자:
1. `Ctrl + Alt + T` 누르기
2. 터미널 창 열림

---

## 📁 Step 3: 프로젝트 폴더로 이동

### 3-1. 현재 위치 확인
터미널에 아래 명령어를 **복사해서 붙여넣고** 엔터:

```bash
pwd
```

→ 현재 어디에 있는지 경로가 표시됩니다

### 3-2. 프로젝트 폴더로 이동
터미널에 아래 명령어를 **한 줄씩** 복사해서 붙여넣고 엔터:

```bash
cd /home/user/bringengineering1008/conversation-diagram
```

### 3-3. 제대로 이동했는지 확인
```bash
ls
```

→ 다음과 같은 파일들이 보이면 성공:
```
app/
components/
lib/
store/
package.json
README.md
...
```

---

## 🔑 Step 4: API 키 설정 (가장 중요!)

### 4-1. 환경 변수 파일 생성

터미널에서 아래 명령어 실행:

**Mac/Linux:**
```bash
cp .env.local.example .env.local
```

**Windows (cmd):**
```bash
copy .env.local.example .env.local
```

### 4-2. 파일 열어서 API 키 넣기

#### 방법 1: 텍스트 에디터로 열기 (추천)

**Mac:**
```bash
open .env.local
```

**Windows:**
```bash
notepad .env.local
```

**Linux:**
```bash
nano .env.local
```

#### 방법 2: VS Code가 설치되어 있다면
```bash
code .env.local
```

### 4-3. 파일 내용 수정

파일이 열리면 이렇게 보일 거예요:

```
# Anthropic API Key
# Get your API key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=placeholder_key
```

**`placeholder_key` 부분을 지우고** Step 1에서 복사한 실제 API 키를 붙여넣으세요:

```
# Anthropic API Key
# Get your API key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-여기에실제키를붙여넣기
```

### 4-4. 저장하고 닫기

- **Windows 메모장**: `Ctrl + S` 눌러서 저장 후 창 닫기
- **Mac TextEdit**: `Command + S` 눌러서 저장 후 창 닫기
- **nano (Linux)**: `Ctrl + O` (저장) → 엔터 → `Ctrl + X` (종료)
- **VS Code**: `Ctrl + S` (저장) 후 창 닫기

---

## 🚀 Step 5: 프로그램 실행!

### 5-1. 개발 서버 시작

터미널에서 아래 명령어 실행:

```bash
npm run dev
```

### 5-2. 성공 메시지 확인

다음과 같은 메시지가 나타나면 성공!

```
  ▲ Next.js 15.1.7
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.5s
```

### 5-3. 브라우저에서 열기

1. 웹 브라우저(Chrome, Firefox, Safari 등) 열기
2. 주소창에 입력: **http://localhost:3000**
3. 엔터!

---

## 🎉 Step 6: 사용해보기!

### 화면 설명

브라우저에 이런 화면이 나타납니다:

```
┌────────────────────────────────────────────────┐
│  Conversation to Diagram        [Export MD]    │
├─────────────────────┬──────────────────────────┤
│                     │                          │
│  [좌측]             │    [우측]                │
│                     │                          │
│  💬 대화            │    🗺️ (처음엔 비어있음)  │
│                     │                          │
│  "대화를 시작하세요" │    "대화를 시작하세요"    │
│                     │                          │
│  [메시지 입력창]    │                          │
│  [전송 버튼]        │                          │
│                     │                          │
└─────────────────────┴──────────────────────────┘
```

### 첫 대화 시작!

**1단계: 아래 메시지 입력창에 이렇게 입력해보세요:**

```
웹 기반 터널 직광 위험도 분석 시스템을 만들고 싶어요
```

**2단계: [전송] 버튼 클릭**

**3단계: 기다리기 (5-10초)**
- AI가 응답하면서
- 오른쪽에 자동으로 도식이 나타납니다!

**4단계: 계속 대화하기**

```
FastAPI 백엔드와 Next.js 프론트엔드로 구성하고,
PostGIS로 공간 데이터를 처리하려고 합니다
```

→ 오른쪽 도식이 **실시간으로 확장**됩니다!

---

## 🎨 화면에 나타나는 것들

### 우측 도식 패널:

- **보라색 박스 (L1)**: 프로젝트의 핵심 목표
- **파란색 박스 (L2)**: 주요 전략/접근법
- **초록색 박스 (L3)**: 구체적 구현 방법
- **노란색 박스 (L4)**: 세부 액션

### 각 박스에는:
- ✓ 마크: 확정된 아이디어
- 💡 마크: 제안된 아이디어
- 🔥 마크: 진행 중인 아이디어

---

## 📥 Step 7: Export 하기

### Markdown으로 저장

1. 우측 상단의 **[📄 Export MD]** 버튼 클릭
2. 파일이 자동으로 다운로드됩니다
3. 파일 이름: `conversation-structure-xxx.md`
4. 메모장이나 노션에서 열어서 확인 가능!

---

## ⚠️ 문제 해결

### Q1: "npm: command not found" 에러가 나요!
**A:** Node.js가 설치되지 않았습니다.
1. https://nodejs.org/ 접속
2. "LTS" 버전 다운로드 (녹색 버튼)
3. 설치 후 터미널 다시 시작
4. `npm --version` 입력해서 버전 확인

### Q2: "ANTHROPIC_API_KEY not configured" 에러가 나요!
**A:** API 키 설정이 안 되었습니다.
1. Step 4로 돌아가기
2. `.env.local` 파일에 API 키가 제대로 들어갔는지 확인
3. 파일 저장했는지 확인
4. 터미널에서 `Ctrl + C` 눌러서 서버 중지
5. `npm run dev` 다시 실행

### Q3: 브라우저에서 "This site can't be reached" 나와요!
**A:** 서버가 실행되지 않았습니다.
1. 터미널에서 `npm run dev`가 실행 중인지 확인
2. "Ready in x.xs" 메시지가 나타났는지 확인
3. `http://localhost:3000` 주소가 정확한지 확인

### Q4: 대화를 보냈는데 응답이 없어요!
**A:** API 키나 네트워크 문제일 수 있습니다.
1. 브라우저의 개발자 도구 열기 (F12)
2. Console 탭에서 에러 메시지 확인
3. API 키가 유효한지 확인 (https://console.anthropic.com/)
4. 인터넷 연결 확인

### Q5: 서버를 종료하고 싶어요!
**A:** 터미널에서 `Ctrl + C` 누르면 됩니다.

---

## 🔄 다시 실행하려면?

**언제든지 다시 시작하려면:**

1. 터미널 열기
2. 프로젝트 폴더로 이동:
   ```bash
   cd /home/user/bringengineering1008/conversation-diagram
   ```
3. 서버 실행:
   ```bash
   npm run dev
   ```
4. 브라우저에서 http://localhost:3000 열기

**대화 내용은 자동으로 저장됩니다!**
- 브라우저의 localStorage에 저장
- 브라우저를 닫았다가 다시 열어도 이전 대화가 남아있습니다
- 완전히 초기화하려면 화면 우측 상단의 **[🗑️ Clear]** 버튼 클릭

---

## 💡 팁

### 더 좋은 결과를 얻으려면:

1. **구체적으로 말하기**
   - ❌ "웹사이트 만들고 싶어요"
   - ✅ "FastAPI와 React로 사용자 인증 기능이 있는 대시보드를 만들고 싶어요"

2. **단계적으로 대화하기**
   - 처음: 프로젝트의 목적
   - 다음: 기술 스택
   - 그 다음: 세부 기능
   - 마지막: 구체적 구현 방법

3. **변경사항 말하기**
   - "아까 말한 PostgreSQL 대신 MongoDB를 쓰고 싶어요"
   - → 구조가 자동으로 업데이트됩니다!

---

## 🎓 다음 단계

### 이 프로젝트를 더 발전시키려면:

1. **코드 수정해보기**
   - `app/page.tsx`: 화면 레이아웃 변경
   - `components/CustomNode.tsx`: 노드 디자인 변경
   - `lib/structure-extractor.ts`: 구조 추출 규칙 변경

2. **기능 추가하기**
   - PNG Export
   - 색상 테마 변경
   - 음성 입력

3. **배포하기**
   - Vercel (무료): https://vercel.com/
   - Netlify (무료): https://netlify.com/

---

## 📞 도움이 필요하면?

- GitHub Issues: https://github.com/bringengineering/bringengineering1008/issues
- 문서 다시 읽기: `README.md`

---

**즐겁게 사용하세요! 🚀**
