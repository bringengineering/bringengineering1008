#!/usr/bin/env python3
"""
R&D 프로젝트 폴더 구조 자동 생성 스크립트
새로운 프로젝트를 위한 표준 폴더 구조와 체크리스트를 생성합니다.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# 폴더 구조 정의
FOLDER_STRUCTURE = {
    "00_templates": [],
    "01_planning": {
        "1.1_problem_definition": [],
        "1.2_demand_survey": [],
        "1.3_technology_research": [],
        "1.4_research_objectives": [],
        "1.5_strategy_structure": [],
        "1.6_budget_approval": [],
    },
    "02_preparation": {
        "2.1_organization": [],
        "2.2_methodology": [],
        "2.3_demonstration_plan": [],
        "2.4_evaluation_criteria": [],
        "2.5_risk_management": [],
        "2.6_kickoff": [],
    },
    "03_execution": {
        "3.1_development": [],
        "3.2_demonstration": [],
        "3.3_evaluation": [],
        "3.4_reports": [],
        "3.5_budget_management": [],
    },
    "04_operation": {
        "4.1_results_analysis": [],
        "4.2_expansion_strategy": [],
        "4.3_final_reports": [],
        "4.4_ip_outputs": [],
    },
    "tools": [],
}

# 체크리스트 내용
CHECKLISTS = {
    "01_planning": """# 1. 기획 단계 (Planning) 체크리스트

## 1.1 정책·제도 기반 공공 문제 정의
- [ ] 1-1. 정책·제도 기반 공공 문제 정의
- [ ] 1-2. 과제 추진 필요성 및 공공 파급효과 도출
- [ ] 1-3. 수요기관(지자체·공기업·관리기관) 식별 및 정의

## 1.2 수요조사 및 요구사항
- [ ] 1-4. 수요조사 계획 수립(대상·방법·범위)
- [ ] 1-5. 수요기관 인터뷰 및 의견 수렴
- [ ] 1-6. 수요 요구사항 정리 및 우선순위 도출

## 1.3 기술 동향 및 선행 연구 조사
- [ ] 1-7. 기존 기술·선행 연구·유사 과제 조사
- [ ] 1-8. 국내·외 기술 동향 및 정책 연계성 분석
- [ ] 1-9. 경쟁 기술·대체 수단 비교 분석
- [ ] 1-10. 기존 방식의 한계 및 문제점 정리
- [ ] 1-11. 연구 필요성 및 차별성 논리 확정

## 1.4 연구 목표 및 범위 설정
- [ ] 1-12. 연구 목표(정량·정성) 설정
- [ ] 1-13. 단계별 목표(연차/TRL) 정의
- [ ] 1-14. 연구 범위 및 제외 범위 명확화
- [ ] 1-15. 기술·운영·제도 영역 구분

## 1.5 추진 전략 및 사업 구조 설계
- [ ] 1-16. 연구 추진 전략 수립
- [ ] 1-17. 전체 사업 구조(주관·참여·위탁) 설계
- [ ] 1-18. 총괄 일정 로드맵 수립

## 1.6 예산 편성 및 내부 승인
- [ ] 1-19. 예산 편성 기준 설정
- [ ] 1-20. 연구비(인건비·장비·외주·실증·간접비) 산정
- [ ] 1-21. 정부출연금·민간부담금·현물 구성 설계
- [ ] 1-22. 과제 기획 보고 및 내부 승인

---
## 산출물 체크리스트
- [ ] 공공 문제 정의서
- [ ] 수요조사 결과 보고서
- [ ] 기술 동향 분석 보고서
- [ ] 연구 목표 및 범위 정의서
- [ ] 사업 구조 설계서
- [ ] 예산 편성안
- [ ] 기획 보고서 (내부 승인용)

## 진행 상태
- 시작일:
- 완료일:
- 담당자:
- 진행률: 0%
""",

    "02_preparation": """# 2. 준비 단계 (Preparation) 체크리스트

## 2.1 조직 체계 및 R&R 확정
- [ ] 2-1. 주관기관 역할 및 책임(R&R) 확정
- [ ] 2-2. 참여기관·위탁기관 선정 기준 수립
- [ ] 2-3. 참여기관 협약 범위 및 역할 정의
- [ ] 2-4. 연구책임자·세부책임자 지정
- [ ] 2-5. 의사결정 및 보고 체계 수립
- [ ] 2-6. 연구관리(PM) 체계 구축

## 2.2 연구 방법론 및 아키텍처 설계
- [ ] 2-7. 연구 방법론 정의
- [ ] 2-8. 기술 아키텍처(하드웨어/소프트웨어/운영) 설계
- [ ] 2-9. 데이터 수집·처리·활용 구조 설계

## 2.3 실증 계획 수립
- [ ] 2-10. 실증 대상 및 실증 환경 후보군 도출
- [ ] 2-11. 실증 장소 협의 및 행정 절차 검토
- [ ] 2-12. 실증 시나리오 정의

## 2.4 성능 지표 및 평가 기준
- [ ] 2-13. 성능 지표(KPI) 및 평가 기준 설정
- [ ] 2-14. 안전성·신뢰성 검증 항목 정의

## 2.5 위험 관리 및 IP 전략
- [ ] 2-15. 데이터 관리 계획(DMP) 수립
- [ ] 2-16. 개인정보·보안·윤리 검토
- [ ] 2-17. 지식재산(IP) 확보 전략 수립
- [ ] 2-18. 특허·논문·성과물 관리 계획 수립
- [ ] 2-19. 위험요소(Risk) 식별 및 대응 계획 수립

## 2.6 착수보고 및 개시 승인
- [ ] 2-20. 연구 일정 세부화(WBS)
- [ ] 2-21. 착수보고서 작성
- [ ] 2-22. 과제 착수 및 연구 개시 승인

---
## 산출물 체크리스트
- [ ] 조직 체계도 및 R&R 매트릭스
- [ ] 참여기관 협약서
- [ ] 기술 아키텍처 설계서
- [ ] 데이터 관리 계획(DMP)
- [ ] 실증 계획서
- [ ] KPI 정의서
- [ ] 위험관리 계획서
- [ ] IP 확보 전략서
- [ ] WBS (Work Breakdown Structure)
- [ ] 착수보고서

## 진행 상태
- 시작일:
- 완료일:
- 담당자:
- 진행률: 0%
""",

    "03_execution": """# 3. 수행 단계 (Execution) 체크리스트

## 3.1 연구개발 수행
- [ ] 3-1. 연차별·단계별 연구개발 수행
- [ ] 3-2. 데이터 수집 및 전처리 수행
- [ ] 3-3. 핵심 기술 개발 및 고도화
- [ ] 3-4. 시스템 통합 및 기능 구현
- [ ] 3-5. 내부 시험 및 기능 검증

## 3.2 실증 수행
- [ ] 3-6. 실증 환경 설치 및 운영 준비
- [ ] 3-7. 실증 수행(파일럿/실환경)

## 3.3 성능 평가 및 피드백
- [ ] 3-8. 성능 측정 및 정량 평가
- [ ] 3-9. 운영 적합성 및 현장 적용성 검증
- [ ] 3-10. 문제점 분석 및 개선안 도출
- [ ] 3-11. 수요기관 현장 피드백 수렴
- [ ] 3-12. 피드백 반영 및 기술 개선

## 3.4 중간보고 및 평가 대응
- [ ] 3-13. 중간보고서 작성
- [ ] 3-14. 중간평가 대응 및 보완

## 3.5 연구비 집행 관리
- [ ] 3-15. 연구비 집행 관리 및 정산 점검
- [ ] 3-16. 연구 일정·범위 조정(필요 시)

## 3.6 최종 기술 완성
- [ ] 3-17. 최종 기술 완성도 확보
- [ ] 3-18. 목표 TRL 단계 달성
- [ ] 3-19. 실증 결과 종합 분석
- [ ] 3-20. 연구 성과 정리

---
## 산출물 체크리스트
- [ ] 연구개발 수행 보고서
- [ ] 데이터 수집/처리 보고서
- [ ] 기술 개발 결과물 (소프트웨어, 하드웨어 등)
- [ ] 내부 시험 결과서
- [ ] 실증 수행 결과 보고서
- [ ] 성능 평가 보고서
- [ ] 중간보고서
- [ ] 연구비 정산 자료
- [ ] 연구 성과 정리표

## 진행 상태
- 시작일:
- 완료일:
- 담당자:
- 진행률: 0%
""",

    "04_operation": """# 4. 운영·확산 단계 (Operation & Scale-up) 체크리스트

## 4.1 연구 성과 종합 분석
- [ ] 4-1. 연구 성과 종합 분석
- [ ] 4-2. 비용 절감·사고 저감·효과 검증
- [ ] 4-3. 공공 도입 타당성 검토

## 4.2 확산 및 사업화 전략
- [ ] 4-4. 시범사업 → 본사업 전환 전략 수립
- [ ] 4-5. 조달·구매·확산 경로 설계
- [ ] 4-6. 지자체·공기업 적용 시나리오 수립
- [ ] 4-7. 사업화 모델(B2G/B2B) 연계 검토
- [ ] 4-8. 후속 R&D 및 기술 고도화 과제 도출
- [ ] 4-9. 정책·제도·표준 반영 가능성 검토
- [ ] 4-10. 가이드라인·매뉴얼화 검토

## 4.3 최종보고서 및 성과 공유
- [ ] 4-11. 최종보고서 작성
- [ ] 4-12. 성과 보고회 및 결과 공유

## 4.4 특허·논문·성과물 관리
- [ ] 4-13. 특허·논문·성과물 제출
- [ ] 4-14. 연구 종료 및 사후 관리 계획 수립

---
## 산출물 체크리스트
- [ ] 연구 성과 종합 분석 보고서
- [ ] 효과 검증 보고서
- [ ] 공공 도입 타당성 검토서
- [ ] 확산 전략 보고서
- [ ] 사업화 계획서
- [ ] 가이드라인/매뉴얼
- [ ] 최종보고서
- [ ] 특허 출원서/등록증
- [ ] 논문 게재 증빙
- [ ] 사후 관리 계획서

## 진행 상태
- 시작일:
- 완료일:
- 담당자:
- 진행률: 0%
"""
}


def create_folder_structure(base_path: Path, structure: dict, depth=0):
    """폴더 구조 재귀적으로 생성"""
    for name, contents in structure.items():
        folder_path = base_path / name
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"{'  ' * depth}📁 {name}/")

        if isinstance(contents, dict):
            create_folder_structure(folder_path, contents, depth + 1)


def create_checklists(base_path: Path):
    """체크리스트 파일 생성"""
    for folder_name, content in CHECKLISTS.items():
        checklist_path = base_path / folder_name / "CHECKLIST.md"
        with open(checklist_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {folder_name}/CHECKLIST.md 생성됨")


def create_readme(base_path: Path, project_name: str):
    """README 파일 생성"""
    readme_content = f"""# {project_name} - R&D 프로젝트 관리

## 개요
공공 R&D 과제의 전 생애주기를 관리하기 위한 PM 프레임워크입니다.

## 폴더 구조

```
project_management/
├── 00_templates/           # 공통 문서 템플릿
├── 01_planning/            # 1. 기획 단계 (Planning)
├── 02_preparation/         # 2. 준비 단계 (Preparation)
├── 03_execution/           # 3. 수행 단계 (Execution)
├── 04_operation/           # 4. 운영·확산 단계 (Operation & Scale-up)
└── tools/                  # PM 도구
```

## 빠른 시작

```bash
# 프로젝트 대시보드 실행
python tools/pm_dashboard.py

# 체크리스트 상태 확인
python tools/checklist_manager.py status

# 진행률 추적
python tools/progress_tracker.py
```

## 생성일
{datetime.now().strftime('%Y-%m-%d')}
"""
    readme_path = base_path / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("  ✅ README.md 생성됨")


def copy_tools(source_path: Path, target_path: Path):
    """도구 파일 복사"""
    tools_source = source_path / "tools"
    tools_target = target_path / "tools"

    if tools_source.exists():
        for tool_file in tools_source.glob("*.py"):
            shutil.copy(tool_file, tools_target / tool_file.name)
            print(f"  ✅ tools/{tool_file.name} 복사됨")


def setup_new_project(target_path: Path, project_name: str = "R&D 프로젝트"):
    """새 프로젝트 설정"""
    print(f"\n{'=' * 60}")
    print(f"  R&D 프로젝트 폴더 구조 생성")
    print(f"  프로젝트: {project_name}")
    print(f"  경로: {target_path}")
    print(f"{'=' * 60}\n")

    # 폴더 구조 생성
    print("📂 폴더 구조 생성 중...")
    create_folder_structure(target_path, FOLDER_STRUCTURE)

    # 체크리스트 생성
    print("\n📝 체크리스트 생성 중...")
    create_checklists(target_path)

    # README 생성
    print("\n📄 README 생성 중...")
    create_readme(target_path, project_name)

    # 현재 스크립트의 도구 복사 (같은 위치에 있다면)
    script_path = Path(__file__).parent.parent
    if script_path != target_path:
        print("\n🔧 도구 복사 중...")
        copy_tools(script_path, target_path)

    print(f"\n{'=' * 60}")
    print("  ✅ 프로젝트 설정 완료!")
    print(f"{'=' * 60}")
    print(f"\n다음 단계:")
    print(f"  1. cd {target_path}")
    print(f"  2. python tools/pm_dashboard.py init  (프로젝트 초기화)")
    print(f"  3. python tools/pm_dashboard.py       (대시보드 확인)")
    print()


def main():
    if len(sys.argv) < 2:
        print("""
R&D 프로젝트 폴더 구조 생성 도구

사용법:
  python setup_project.py <대상경로> [프로젝트명]

예시:
  python setup_project.py ./new_project "스마트시티 R&D"
  python setup_project.py /path/to/project
        """)
        return

    target = Path(sys.argv[1]).resolve()
    project_name = sys.argv[2] if len(sys.argv) > 2 else "R&D 프로젝트"

    if target.exists() and any(target.iterdir()):
        confirm = input(f"⚠️  '{target}' 폴더가 비어있지 않습니다. 계속하시겠습니까? (y/N): ")
        if confirm.lower() != 'y':
            print("취소되었습니다.")
            return

    setup_new_project(target, project_name)


if __name__ == "__main__":
    main()
