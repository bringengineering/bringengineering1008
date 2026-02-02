@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   R^&D 프로젝트 관리 폴더 자동 생성기
echo ============================================================
echo.

set "DESKTOP=%USERPROFILE%\Desktop"
set "PROJECT=RnD_프로젝트관리"
set "BASE=%DESKTOP%\%PROJECT%"

echo 생성 위치: %BASE%
echo.

if exist "%BASE%" (
    echo [!] 폴더가 이미 존재합니다.
    set /p confirm="    덮어쓰시겠습니까? (y/N): "
    if /i not "!confirm!"=="y" (
        echo 취소되었습니다.
        pause
        exit /b
    )
)

echo.
echo [1/4] 폴더 구조 생성 중...

:: 메인 폴더 생성
mkdir "%BASE%" 2>nul
mkdir "%BASE%\00_templates" 2>nul

:: 01_planning
mkdir "%BASE%\01_planning" 2>nul
mkdir "%BASE%\01_planning\1.1_problem_definition" 2>nul
mkdir "%BASE%\01_planning\1.2_demand_survey" 2>nul
mkdir "%BASE%\01_planning\1.3_technology_research" 2>nul
mkdir "%BASE%\01_planning\1.4_research_objectives" 2>nul
mkdir "%BASE%\01_planning\1.5_strategy_structure" 2>nul
mkdir "%BASE%\01_planning\1.6_budget_approval" 2>nul
echo   [+] 01_planning/

:: 02_preparation
mkdir "%BASE%\02_preparation" 2>nul
mkdir "%BASE%\02_preparation\2.1_organization" 2>nul
mkdir "%BASE%\02_preparation\2.2_methodology" 2>nul
mkdir "%BASE%\02_preparation\2.3_demonstration_plan" 2>nul
mkdir "%BASE%\02_preparation\2.4_evaluation_criteria" 2>nul
mkdir "%BASE%\02_preparation\2.5_risk_management" 2>nul
mkdir "%BASE%\02_preparation\2.6_kickoff" 2>nul
echo   [+] 02_preparation/

:: 03_execution
mkdir "%BASE%\03_execution" 2>nul
mkdir "%BASE%\03_execution\3.1_development" 2>nul
mkdir "%BASE%\03_execution\3.2_demonstration" 2>nul
mkdir "%BASE%\03_execution\3.3_evaluation" 2>nul
mkdir "%BASE%\03_execution\3.4_reports" 2>nul
mkdir "%BASE%\03_execution\3.5_budget_management" 2>nul
echo   [+] 03_execution/

:: 04_operation
mkdir "%BASE%\04_operation" 2>nul
mkdir "%BASE%\04_operation\4.1_results_analysis" 2>nul
mkdir "%BASE%\04_operation\4.2_expansion_strategy" 2>nul
mkdir "%BASE%\04_operation\4.3_final_reports" 2>nul
mkdir "%BASE%\04_operation\4.4_ip_outputs" 2>nul
echo   [+] 04_operation/

echo.
echo [2/4] 체크리스트 생성 중...

:: 01_planning CHECKLIST
(
echo # 1. 기획 단계 ^(Planning^) 체크리스트
echo.
echo ## 1.1 정책·제도 기반 공공 문제 정의
echo - [ ] 1-1. 정책·제도 기반 공공 문제 정의
echo - [ ] 1-2. 과제 추진 필요성 및 공공 파급효과 도출
echo - [ ] 1-3. 수요기관^(지자체·공기업·관리기관^) 식별 및 정의
echo.
echo ## 1.2 수요조사 및 요구사항
echo - [ ] 1-4. 수요조사 계획 수립^(대상·방법·범위^)
echo - [ ] 1-5. 수요기관 인터뷰 및 의견 수렴
echo - [ ] 1-6. 수요 요구사항 정리 및 우선순위 도출
echo.
echo ## 1.3 기술 동향 및 선행 연구 조사
echo - [ ] 1-7. 기존 기술·선행 연구·유사 과제 조사
echo - [ ] 1-8. 국내·외 기술 동향 및 정책 연계성 분석
echo - [ ] 1-9. 경쟁 기술·대체 수단 비교 분석
echo - [ ] 1-10. 기존 방식의 한계 및 문제점 정리
echo - [ ] 1-11. 연구 필요성 및 차별성 논리 확정
echo.
echo ## 1.4 연구 목표 및 범위 설정
echo - [ ] 1-12. 연구 목표^(정량·정성^) 설정
echo - [ ] 1-13. 단계별 목표^(연차/TRL^) 정의
echo - [ ] 1-14. 연구 범위 및 제외 범위 명확화
echo - [ ] 1-15. 기술·운영·제도 영역 구분
echo.
echo ## 1.5 추진 전략 및 사업 구조 설계
echo - [ ] 1-16. 연구 추진 전략 수립
echo - [ ] 1-17. 전체 사업 구조^(주관·참여·위탁^) 설계
echo - [ ] 1-18. 총괄 일정 로드맵 수립
echo.
echo ## 1.6 예산 편성 및 내부 승인
echo - [ ] 1-19. 예산 편성 기준 설정
echo - [ ] 1-20. 연구비^(인건비·장비·외주·실증·간접비^) 산정
echo - [ ] 1-21. 정부출연금·민간부담금·현물 구성 설계
echo - [ ] 1-22. 과제 기획 보고 및 내부 승인
) > "%BASE%\01_planning\CHECKLIST.md"
echo   [+] 01_planning/CHECKLIST.md

:: 02_preparation CHECKLIST
(
echo # 2. 준비 단계 ^(Preparation^) 체크리스트
echo.
echo ## 2.1 조직 체계 및 R^&R 확정
echo - [ ] 2-1. 주관기관 역할 및 책임^(R^&R^) 확정
echo - [ ] 2-2. 참여기관·위탁기관 선정 기준 수립
echo - [ ] 2-3. 참여기관 협약 범위 및 역할 정의
echo - [ ] 2-4. 연구책임자·세부책임자 지정
echo - [ ] 2-5. 의사결정 및 보고 체계 수립
echo - [ ] 2-6. 연구관리^(PM^) 체계 구축
echo.
echo ## 2.2 연구 방법론 및 아키텍처 설계
echo - [ ] 2-7. 연구 방법론 정의
echo - [ ] 2-8. 기술 아키텍처^(하드웨어/소프트웨어/운영^) 설계
echo - [ ] 2-9. 데이터 수집·처리·활용 구조 설계
echo.
echo ## 2.3 실증 계획 수립
echo - [ ] 2-10. 실증 대상 및 실증 환경 후보군 도출
echo - [ ] 2-11. 실증 장소 협의 및 행정 절차 검토
echo - [ ] 2-12. 실증 시나리오 정의
echo.
echo ## 2.4 성능 지표 및 평가 기준
echo - [ ] 2-13. 성능 지표^(KPI^) 및 평가 기준 설정
echo - [ ] 2-14. 안전성·신뢰성 검증 항목 정의
echo.
echo ## 2.5 위험 관리 및 IP 전략
echo - [ ] 2-15. 데이터 관리 계획^(DMP^) 수립
echo - [ ] 2-16. 개인정보·보안·윤리 검토
echo - [ ] 2-17. 지식재산^(IP^) 확보 전략 수립
echo - [ ] 2-18. 특허·논문·성과물 관리 계획 수립
echo - [ ] 2-19. 위험요소^(Risk^) 식별 및 대응 계획 수립
echo.
echo ## 2.6 착수보고 및 개시 승인
echo - [ ] 2-20. 연구 일정 세부화^(WBS^)
echo - [ ] 2-21. 착수보고서 작성
echo - [ ] 2-22. 과제 착수 및 연구 개시 승인
) > "%BASE%\02_preparation\CHECKLIST.md"
echo   [+] 02_preparation/CHECKLIST.md

:: 03_execution CHECKLIST
(
echo # 3. 수행 단계 ^(Execution^) 체크리스트
echo.
echo ## 3.1 연구개발 수행
echo - [ ] 3-1. 연차별·단계별 연구개발 수행
echo - [ ] 3-2. 데이터 수집 및 전처리 수행
echo - [ ] 3-3. 핵심 기술 개발 및 고도화
echo - [ ] 3-4. 시스템 통합 및 기능 구현
echo - [ ] 3-5. 내부 시험 및 기능 검증
echo.
echo ## 3.2 실증 수행
echo - [ ] 3-6. 실증 환경 설치 및 운영 준비
echo - [ ] 3-7. 실증 수행^(파일럿/실환경^)
echo.
echo ## 3.3 성능 평가 및 피드백
echo - [ ] 3-8. 성능 측정 및 정량 평가
echo - [ ] 3-9. 운영 적합성 및 현장 적용성 검증
echo - [ ] 3-10. 문제점 분석 및 개선안 도출
echo - [ ] 3-11. 수요기관 현장 피드백 수렴
echo - [ ] 3-12. 피드백 반영 및 기술 개선
echo.
echo ## 3.4 중간보고 및 평가 대응
echo - [ ] 3-13. 중간보고서 작성
echo - [ ] 3-14. 중간평가 대응 및 보완
echo.
echo ## 3.5 연구비 집행 관리
echo - [ ] 3-15. 연구비 집행 관리 및 정산 점검
echo - [ ] 3-16. 연구 일정·범위 조정^(필요 시^)
echo.
echo ## 3.6 최종 기술 완성
echo - [ ] 3-17. 최종 기술 완성도 확보
echo - [ ] 3-18. 목표 TRL 단계 달성
echo - [ ] 3-19. 실증 결과 종합 분석
echo - [ ] 3-20. 연구 성과 정리
) > "%BASE%\03_execution\CHECKLIST.md"
echo   [+] 03_execution/CHECKLIST.md

:: 04_operation CHECKLIST
(
echo # 4. 운영·확산 단계 ^(Operation ^& Scale-up^) 체크리스트
echo.
echo ## 4.1 연구 성과 종합 분석
echo - [ ] 4-1. 연구 성과 종합 분석
echo - [ ] 4-2. 비용 절감·사고 저감·효과 검증
echo - [ ] 4-3. 공공 도입 타당성 검토
echo.
echo ## 4.2 확산 및 사업화 전략
echo - [ ] 4-4. 시범사업 → 본사업 전환 전략 수립
echo - [ ] 4-5. 조달·구매·확산 경로 설계
echo - [ ] 4-6. 지자체·공기업 적용 시나리오 수립
echo - [ ] 4-7. 사업화 모델^(B2G/B2B^) 연계 검토
echo - [ ] 4-8. 후속 R^&D 및 기술 고도화 과제 도출
echo - [ ] 4-9. 정책·제도·표준 반영 가능성 검토
echo - [ ] 4-10. 가이드라인·매뉴얼화 검토
echo.
echo ## 4.3 최종보고서 및 성과 공유
echo - [ ] 4-11. 최종보고서 작성
echo - [ ] 4-12. 성과 보고회 및 결과 공유
echo.
echo ## 4.4 특허·논문·성과물 관리
echo - [ ] 4-13. 특허·논문·성과물 제출
echo - [ ] 4-14. 연구 종료 및 사후 관리 계획 수립
) > "%BASE%\04_operation\CHECKLIST.md"
echo   [+] 04_operation/CHECKLIST.md

echo.
echo [3/4] README 생성 중...

(
echo # R^&D 프로젝트 관리 프레임워크
echo.
echo ## 폴더 구조
echo.
echo ```
echo RnD_프로젝트관리/
echo ├── 00_templates/           # 공통 문서 템플릿
echo ├── 01_planning/            # 1. 기획 단계
echo ├── 02_preparation/         # 2. 준비 단계
echo ├── 03_execution/           # 3. 수행 단계
echo └── 04_operation/           # 4. 운영·확산 단계
echo ```
echo.
echo ## 사용 방법
echo.
echo 1. 각 단계 폴더의 CHECKLIST.md를 확인하여 진행 상황 관리
echo 2. 완료된 항목은 [ ]를 [x]로 변경
echo.
echo 생성일: %date%
) > "%BASE%\README.md"
echo   [+] README.md

echo.
echo [4/4] 완료!
echo.
echo ============================================================
echo   폴더가 생성되었습니다: %BASE%
echo ============================================================
echo.
echo 각 단계 폴더의 CHECKLIST.md 파일을 확인하세요.
echo.

pause
