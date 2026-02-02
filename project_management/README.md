# R&D 프로젝트 관리 프레임워크

## 개요
공공 R&D 과제의 전 생애주기를 관리하기 위한 PM 프레임워크입니다.

## 폴더 구조

```
project_management/
├── 00_templates/           # 공통 문서 템플릿
├── 01_planning/            # 1. 기획 단계 (Planning)
│   ├── 1.1_problem_definition/    # 정책·제도 기반 공공 문제 정의
│   ├── 1.2_demand_survey/         # 수요조사 및 요구사항 정리
│   ├── 1.3_technology_research/   # 기술 동향 및 선행 연구 조사
│   ├── 1.4_research_objectives/   # 연구 목표 및 범위 설정
│   ├── 1.5_strategy_structure/    # 추진 전략 및 사업 구조 설계
│   └── 1.6_budget_approval/       # 예산 편성 및 내부 승인
├── 02_preparation/         # 2. 준비 단계 (Preparation)
│   ├── 2.1_organization/          # 조직 체계 및 R&R 확정
│   ├── 2.2_methodology/           # 연구 방법론 및 아키텍처 설계
│   ├── 2.3_demonstration_plan/    # 실증 계획 수립
│   ├── 2.4_evaluation_criteria/   # 성능 지표 및 평가 기준
│   ├── 2.5_risk_management/       # 위험 관리 및 IP 전략
│   └── 2.6_kickoff/               # 착수보고 및 개시 승인
├── 03_execution/           # 3. 수행 단계 (Execution)
│   ├── 3.1_development/           # 연구개발 수행
│   ├── 3.2_demonstration/         # 실증 수행
│   ├── 3.3_evaluation/            # 성능 평가 및 피드백
│   ├── 3.4_reports/               # 중간보고 및 평가 대응
│   └── 3.5_budget_management/     # 연구비 집행 관리
├── 04_operation/           # 4. 운영·확산 단계 (Operation & Scale-up)
│   ├── 4.1_results_analysis/      # 연구 성과 종합 분석
│   ├── 4.2_expansion_strategy/    # 확산 및 사업화 전략
│   ├── 4.3_final_reports/         # 최종보고서 및 성과 공유
│   └── 4.4_ip_outputs/            # 특허·논문·성과물 관리
└── tools/                  # PM 도구
    ├── pm_dashboard.py            # 프로젝트 대시보드
    ├── checklist_manager.py       # 체크리스트 관리
    └── progress_tracker.py        # 진행 상황 추적
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

## 단계별 주요 산출물

| 단계 | 주요 산출물 |
|------|------------|
| 1. 기획 | 과제 기획서, 예산안, 내부 승인 문서 |
| 2. 준비 | 착수보고서, WBS, DMP, 위험관리 계획 |
| 3. 수행 | 중간보고서, 실증 결과 보고서, 성과 정리 |
| 4. 운영·확산 | 최종보고서, 특허/논문, 사업화 계획 |

## PM 체크리스트

각 폴더의 `CHECKLIST.md` 파일을 참조하여 진행 상황을 관리하세요.
