#!/usr/bin/env python3
"""
산출물 관리 도구
R&D 프로젝트의 산출물을 추적하고 관리하는 CLI 도구
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "tools" / ".deliverables.json"

# 단계별 표준 산출물 정의
STANDARD_DELIVERABLES = {
    "01_planning": [
        {"id": "P-001", "name": "공공 문제 정의서", "required": True},
        {"id": "P-002", "name": "수요조사 결과 보고서", "required": True},
        {"id": "P-003", "name": "기술 동향 분석 보고서", "required": True},
        {"id": "P-004", "name": "연구 목표 및 범위 정의서", "required": True},
        {"id": "P-005", "name": "사업 구조 설계서", "required": True},
        {"id": "P-006", "name": "예산 편성안", "required": True},
        {"id": "P-007", "name": "기획 보고서", "required": True},
    ],
    "02_preparation": [
        {"id": "R-001", "name": "조직 체계도 및 R&R 매트릭스", "required": True},
        {"id": "R-002", "name": "참여기관 협약서", "required": True},
        {"id": "R-003", "name": "기술 아키텍처 설계서", "required": True},
        {"id": "R-004", "name": "데이터 관리 계획(DMP)", "required": True},
        {"id": "R-005", "name": "실증 계획서", "required": True},
        {"id": "R-006", "name": "KPI 정의서", "required": True},
        {"id": "R-007", "name": "위험관리 계획서", "required": True},
        {"id": "R-008", "name": "IP 확보 전략서", "required": False},
        {"id": "R-009", "name": "WBS", "required": True},
        {"id": "R-010", "name": "착수보고서", "required": True},
    ],
    "03_execution": [
        {"id": "E-001", "name": "연구개발 수행 보고서", "required": True},
        {"id": "E-002", "name": "데이터 수집/처리 보고서", "required": True},
        {"id": "E-003", "name": "기술 개발 결과물", "required": True},
        {"id": "E-004", "name": "내부 시험 결과서", "required": True},
        {"id": "E-005", "name": "실증 수행 결과 보고서", "required": True},
        {"id": "E-006", "name": "성능 평가 보고서", "required": True},
        {"id": "E-007", "name": "중간보고서", "required": True},
        {"id": "E-008", "name": "연구비 정산 자료", "required": True},
        {"id": "E-009", "name": "연구 성과 정리표", "required": True},
    ],
    "04_operation": [
        {"id": "O-001", "name": "연구 성과 종합 분석 보고서", "required": True},
        {"id": "O-002", "name": "효과 검증 보고서", "required": True},
        {"id": "O-003", "name": "공공 도입 타당성 검토서", "required": False},
        {"id": "O-004", "name": "확산 전략 보고서", "required": False},
        {"id": "O-005", "name": "사업화 계획서", "required": False},
        {"id": "O-006", "name": "가이드라인/매뉴얼", "required": False},
        {"id": "O-007", "name": "최종보고서", "required": True},
        {"id": "O-008", "name": "특허 출원서/등록증", "required": False},
        {"id": "O-009", "name": "논문 게재 증빙", "required": False},
        {"id": "O-010", "name": "사후 관리 계획서", "required": True},
    ]
}

PHASE_NAMES = {
    "01_planning": "기획 단계",
    "02_preparation": "준비 단계",
    "03_execution": "수행 단계",
    "04_operation": "운영·확산 단계"
}

def load_data() -> Dict:
    """데이터 로드"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"deliverables": {}}

def save_data(data: Dict):
    """데이터 저장"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def show_deliverables(phase: str = None):
    """산출물 현황 표시"""
    data = load_data()
    deliverables = data.get("deliverables", {})

    print("\n" + "=" * 70)
    print("        산출물 관리 현황")
    print("=" * 70)

    phases = [phase] if phase else STANDARD_DELIVERABLES.keys()

    total_required = 0
    total_completed = 0

    for ph in phases:
        if ph not in STANDARD_DELIVERABLES:
            continue

        phase_name = PHASE_NAMES.get(ph, ph)
        items = STANDARD_DELIVERABLES[ph]
        phase_data = deliverables.get(ph, {})

        print(f"\n📁 {phase_name}")
        print("-" * 60)

        for item in items:
            item_id = item["id"]
            item_data = phase_data.get(item_id, {})

            status = item_data.get("status", "pending")
            required = "⚠️" if item["required"] else "  "

            if status == "completed":
                icon = "✅"
                total_completed += 1 if item["required"] else 0
            elif status == "in_progress":
                icon = "🔄"
            else:
                icon = "⬜"

            total_required += 1 if item["required"] else 0

            file_path = item_data.get("file_path", "")
            path_info = f" → {file_path}" if file_path else ""

            print(f"  {required} {icon} [{item_id}] {item['name']}{path_info}")

    # 요약
    print("\n" + "=" * 70)
    print(f"📊 필수 산출물 완료율: {total_completed}/{total_required} ", end="")
    if total_required > 0:
        print(f"({total_completed/total_required*100:.1f}%)")
    else:
        print("(0%)")
    print("=" * 70 + "\n")

def register_deliverable(deliverable_id: str, file_path: str = None, note: str = None):
    """산출물 등록/완료 처리"""
    data = load_data()

    # ID로 단계 찾기
    target_phase = None
    target_item = None

    for phase, items in STANDARD_DELIVERABLES.items():
        for item in items:
            if item["id"] == deliverable_id:
                target_phase = phase
                target_item = item
                break
        if target_phase:
            break

    if not target_phase:
        print(f"❌ 산출물 ID '{deliverable_id}'를 찾을 수 없습니다.")
        return

    # 데이터 업데이트
    if target_phase not in data["deliverables"]:
        data["deliverables"][target_phase] = {}

    data["deliverables"][target_phase][deliverable_id] = {
        "status": "completed",
        "file_path": file_path or "",
        "note": note or "",
        "completed_at": datetime.now().isoformat()
    }

    save_data(data)
    print(f"\n✅ 산출물 등록 완료: [{deliverable_id}] {target_item['name']}")
    if file_path:
        print(f"   파일 경로: {file_path}")

def set_in_progress(deliverable_id: str):
    """산출물 작성 중 표시"""
    data = load_data()

    # ID로 단계 찾기
    target_phase = None
    target_item = None

    for phase, items in STANDARD_DELIVERABLES.items():
        for item in items:
            if item["id"] == deliverable_id:
                target_phase = phase
                target_item = item
                break
        if target_phase:
            break

    if not target_phase:
        print(f"❌ 산출물 ID '{deliverable_id}'를 찾을 수 없습니다.")
        return

    if target_phase not in data["deliverables"]:
        data["deliverables"][target_phase] = {}

    existing = data["deliverables"][target_phase].get(deliverable_id, {})
    existing["status"] = "in_progress"
    existing["updated_at"] = datetime.now().isoformat()
    data["deliverables"][target_phase][deliverable_id] = existing

    save_data(data)
    print(f"\n🔄 '{target_item['name']}' 작성 중 표시됨")

def list_ids():
    """모든 산출물 ID 목록 표시"""
    print("\n📋 산출물 ID 목록\n")

    for phase, items in STANDARD_DELIVERABLES.items():
        phase_name = PHASE_NAMES.get(phase, phase)
        print(f"{phase_name}:")
        for item in items:
            req = "*" if item["required"] else " "
            print(f"  {req} {item['id']}: {item['name']}")
        print()

    print("* = 필수 산출물")

def main():
    if len(sys.argv) < 2:
        show_deliverables()
        return

    cmd = sys.argv[1].lower()

    if cmd == 'status' or cmd == 's':
        phase = sys.argv[2] if len(sys.argv) > 2 else None
        show_deliverables(phase)
    elif cmd == 'complete' or cmd == 'c':
        if len(sys.argv) < 3:
            print("사용법: deliverable_tracker.py complete <ID> [파일경로]")
            return
        deliverable_id = sys.argv[2].upper()
        file_path = sys.argv[3] if len(sys.argv) > 3 else None
        register_deliverable(deliverable_id, file_path)
    elif cmd == 'progress' or cmd == 'p':
        if len(sys.argv) < 3:
            print("사용법: deliverable_tracker.py progress <ID>")
            return
        set_in_progress(sys.argv[2].upper())
    elif cmd == 'list' or cmd == 'l':
        list_ids()
    elif cmd == 'help':
        print("""
산출물 관리 도구 사용법:

  python deliverable_tracker.py              전체 현황 보기
  python deliverable_tracker.py status       전체 현황 보기
  python deliverable_tracker.py status 01_planning   특정 단계 보기
  python deliverable_tracker.py list         산출물 ID 목록
  python deliverable_tracker.py complete P-001 ./path/file.pdf   산출물 완료 등록
  python deliverable_tracker.py progress P-001   작성 중 표시
        """)
    else:
        print("알 수 없는 명령어입니다. 'help' 명령어를 사용하세요.")

if __name__ == "__main__":
    main()
