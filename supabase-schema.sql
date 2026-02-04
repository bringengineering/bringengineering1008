-- IP Bridge 데이터베이스 스키마
-- Supabase SQL Editor에서 실행하세요

-- 1. 사용자 프로필 테이블 (Supabase Auth와 연동)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  email TEXT NOT NULL,
  name TEXT,
  role TEXT DEFAULT 'submitter' CHECK (role IN ('submitter', 'expert', 'admin', 'company')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 아이디어 테이블
CREATE TABLE IF NOT EXISTS ideas (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL, -- 프로토타입에서는 TEXT, 실제로는 UUID REFERENCES profiles(id)
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  problem TEXT NOT NULL,
  field TEXT NOT NULL,
  existing_tech TEXT,
  attachments JSONB DEFAULT '[]',
  status TEXT DEFAULT 'submitted' CHECK (status IN (
    'submitted', 'ai_analyzing', 'ai_reviewed', 'expert_review',
    'approved', 'rejected', 'patent_filed', 'patent_registered', 'on_sale', 'sold'
  )),
  nda_agreed BOOLEAN DEFAULT FALSE,
  nda_agreed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. AI 분석 결과 테이블
CREATE TABLE IF NOT EXISTS ai_analyses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  idea_id UUID REFERENCES ideas(id) ON DELETE CASCADE,

  -- 키워드 추출
  keywords_kr JSONB DEFAULT '[]',
  keywords_en JSONB DEFAULT '[]',
  ipc_codes JSONB DEFAULT '[]',

  -- 선행기술 검색 결과
  prior_arts JSONB DEFAULT '[]',

  -- 유사도 분석
  similarity_analysis JSONB DEFAULT '[]',

  -- 특허 가능성 점수
  scores JSONB DEFAULT '{}',
  total_score INTEGER DEFAULT 0,
  grade TEXT CHECK (grade IN ('S', 'A', 'B', 'C', 'D')),

  -- 종합 의견
  overall_opinion TEXT,
  improvement_suggestions JSONB DEFAULT '[]',

  -- 명세서 초안
  specification_draft JSONB,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. 전문가 평가 테이블
CREATE TABLE IF NOT EXISTS expert_evaluations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  idea_id UUID REFERENCES ideas(id) ON DELETE CASCADE,
  expert_id UUID, -- REFERENCES profiles(id)
  stage INTEGER DEFAULT 1 CHECK (stage IN (1, 2)),

  -- 평가 점수
  technical_score INTEGER DEFAULT 0,
  patent_score INTEGER DEFAULT 0,
  market_score INTEGER DEFAULT 0,
  commercialization_score INTEGER DEFAULT 0,
  total_score INTEGER DEFAULT 0,

  feedback TEXT,
  result TEXT CHECK (result IN ('pass', 'hold', 'reject')),

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. 특허 테이블
CREATE TABLE IF NOT EXISTS patents (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  idea_id UUID REFERENCES ideas(id) ON DELETE CASCADE,
  application_number TEXT,
  registration_number TEXT,
  status TEXT DEFAULT 'drafting' CHECK (status IN (
    'drafting', 'filed', 'examining', 'registered', 'rejected'
  )),
  filed_at TIMESTAMPTZ,
  registered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. 계약 테이블
CREATE TABLE IF NOT EXISTS contracts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  idea_id UUID REFERENCES ideas(id) ON DELETE CASCADE,
  company_id UUID, -- REFERENCES profiles(id)
  type TEXT CHECK (type IN ('sale', 'licensing')),
  amount DECIMAL(15, 2),
  revenue_share JSONB DEFAULT '{"submitter": 60, "platform": 30, "expert": 10}',
  status TEXT DEFAULT 'negotiating' CHECK (status IN ('negotiating', 'signed', 'completed')),
  signed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. 정산 테이블
CREATE TABLE IF NOT EXISTS transactions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  contract_id UUID REFERENCES contracts(id) ON DELETE CASCADE,
  user_id UUID, -- REFERENCES profiles(id)
  amount DECIMAL(15, 2),
  type TEXT CHECK (type IN ('revenue', 'payout')),
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_ideas_user_id ON ideas(user_id);
CREATE INDEX IF NOT EXISTS idx_ideas_status ON ideas(status);
CREATE INDEX IF NOT EXISTS idx_ai_analyses_idea_id ON ai_analyses(idea_id);
CREATE INDEX IF NOT EXISTS idx_expert_evaluations_idea_id ON expert_evaluations(idea_id);

-- updated_at 자동 업데이트 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- 트리거 생성
DROP TRIGGER IF EXISTS update_ideas_updated_at ON ideas;
CREATE TRIGGER update_ideas_updated_at
  BEFORE UPDATE ON ideas
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_profiles_updated_at ON profiles;
CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- RLS (Row Level Security) 정책 (프로토타입에서는 비활성화)
-- 실제 배포 시 활성화 필요
-- ALTER TABLE ideas ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE ai_analyses ENABLE ROW LEVEL SECURITY;
