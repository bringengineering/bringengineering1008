#!/usr/bin/env python3
"""
R&D 프로젝트 PM 대시보드
프로젝트 전체 현황을 한눈에 파악할 수 있는 CLI 대시보드
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "tools" / ".project_data.json"

@dataclass
class PhaseInfo:
    """단계 정보"""
    name: str
    folder: str
    checklist_file: str
    total_tasks: int = 0
    completed_tasks: int = 0

PHASES = [
    PhaseInfo("1. 기획 단계", "01_planning", "CHECKLIST.md"),
    PhaseInfo("2. 준비 단계", "02_preparation", "CHECKLIST.md"),
    PhaseInfo("3. 수행 단계", "03_execution", "CHECKLIST.md"),
    PhaseInfo("4. 운영·확산 단계", "04_operation", "CHECKLIST.md"),
]

def load_project_data() -> Dict:
    """프로젝트 데이터 로드"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "project_name": "R&D 프로젝트",
        "start_date": "",
        "end_date": "",
        "pm_name": "",
        "current_phase": 1,
        "milestones": [],
        "issues": [],
        "notes": []
    }

def save_project_data(data: Dict):
    """프로젝트 데이터 저장"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse_checklist(filepath: Path) -> tuple:
    """체크리스트 파일 파싱"""
    if not filepath.exists():
        return 0, 0

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 체크박스 찾기
    checked = len(re.findall(r'- \[x\]', content, re.IGNORECASE))
    unchecked = len(re.findall(r'- \[ \]', content))

    return checked, checked + unchecked

def get_phase_status() -> List[PhaseInfo]:
    """각 단계 상태 가져오기"""
    phases = []
    for phase in PHASES:
        checklist_path = PROJECT_ROOT / phase.folder / phase.checklist_file
        completed, total = parse_checklist(checklist_path)
        phase.completed_tasks = completed
        phase.total_tasks = total
        phases.append(phase)
    return phases

def print_header():
    """헤더 출력"""
    print("\n" + "=" * 70)
    print("        R&D 프로젝트 관리 대시보드")
    print("=" * 70)

def print_progress_bar(completed: int, total: int, width: int = 30) -> str:
    """진행 바 생성"""
    if total == 0:
        return "[" + "-" * width + "] 0%"

    ratio = completed / total
    filled = int(width * ratio)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {ratio*100:.1f}%"

def show_dashboard():
    """대시보드 표시"""
    print_header()

    data = load_project_data()
    phases = get_phase_status()

    # 프로젝트 기본 정보
    print(f"\n📋 프로젝트: {data.get('project_name', 'R&D 프로젝트')}")
    if data.get('pm_name'):
        print(f"👤 PM: {data['pm_name']}")
    if data.get('start_date'):
        print(f"📅 기간: {data['start_date']} ~ {data.get('end_date', '진행중')}")

    print(f"\n⏰ 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # 전체 진행률
    total_completed = sum(p.completed_tasks for p in phases)
    total_tasks = sum(p.total_tasks for p in phases)

    print("\n" + "-" * 70)
    print("📊 전체 진행 현황")
    print("-" * 70)
    print(f"   {print_progress_bar(total_completed, total_tasks, 40)}")
    print(f"   완료: {total_completed} / {total_tasks} 태스크")

    # 단계별 진행률
    print("\n" + "-" * 70)
    print("📈 단계별 진행 현황")
    print("-" * 70)

    current_phase = data.get('current_phase', 1)

    for i, phase in enumerate(phases, 1):
        status_icon = "🔵" if i == current_phase else ("✅" if phase.completed_tasks == phase.total_tasks and phase.total_tasks > 0 else "⚪")
        progress = print_progress_bar(phase.completed_tasks, phase.total_tasks, 20)
        print(f"   {status_icon} {phase.name}")
        print(f"      {progress} ({phase.completed_tasks}/{phase.total_tasks})")
        print()

    # 주요 마일스톤
    if data.get('milestones'):
        print("-" * 70)
        print("🎯 주요 마일스톤")
        print("-" * 70)
        for milestone in data['milestones'][-5:]:  # 최근 5개
            status = "✅" if milestone.get('completed') else "⏳"
            print(f"   {status} [{milestone.get('date', 'TBD')}] {milestone.get('title', '')}")

    # 이슈/리스크
    if data.get('issues'):
        active_issues = [i for i in data['issues'] if not i.get('resolved')]
        if active_issues:
            print("\n" + "-" * 70)
            print("⚠️  활성 이슈")
            print("-" * 70)
            for issue in active_issues[-3:]:  # 최근 3개
                priority = "🔴" if issue.get('priority') == 'high' else ("🟡" if issue.get('priority') == 'medium' else "🟢")
                print(f"   {priority} {issue.get('title', '')}")

    print("\n" + "=" * 70)
    print("명령어: python pm_dashboard.py [init|set|milestone|issue|status]")
    print("=" * 70 + "\n")

def init_project():
    """프로젝트 초기화"""
    print("\n📋 프로젝트 초기화")
    print("-" * 40)

    data = load_project_data()

    name = input("프로젝트 이름: ").strip()
    if name:
        data['project_name'] = name

    pm = input("PM 이름: ").strip()
    if pm:
        data['pm_name'] = pm

    start = input("시작일 (YYYY-MM-DD): ").strip()
    if start:
        data['start_date'] = start

    end = input("종료 예정일 (YYYY-MM-DD): ").strip()
    if end:
        data['end_date'] = end

    save_project_data(data)
    print("\n✅ 프로젝트 정보가 저장되었습니다.")

def set_current_phase():
    """현재 단계 설정"""
    data = load_project_data()
    print("\n현재 단계 선택:")
    for i, phase in enumerate(PHASES, 1):
        print(f"  {i}. {phase.name}")

    try:
        choice = int(input("\n선택 (1-4): "))
        if 1 <= choice <= 4:
            data['current_phase'] = choice
            save_project_data(data)
            print(f"\n✅ 현재 단계가 '{PHASES[choice-1].name}'으로 설정되었습니다.")
    except ValueError:
        print("올바른 숫자를 입력하세요.")

def add_milestone():
    """마일스톤 추가"""
    data = load_project_data()

    print("\n🎯 마일스톤 추가")
    title = input("마일스톤 제목: ").strip()
    date = input("목표일 (YYYY-MM-DD): ").strip()

    if title:
        data.setdefault('milestones', []).append({
            'title': title,
            'date': date,
            'completed': False,
            'created_at': datetime.now().isoformat()
        })
        save_project_data(data)
        print("\n✅ 마일스톤이 추가되었습니다.")

def add_issue():
    """이슈 추가"""
    data = load_project_data()

    print("\n⚠️  이슈 추가")
    title = input("이슈 제목: ").strip()
    priority = input("우선순위 (high/medium/low): ").strip().lower()

    if title:
        data.setdefault('issues', []).append({
            'title': title,
            'priority': priority if priority in ['high', 'medium', 'low'] else 'medium',
            'resolved': False,
            'created_at': datetime.now().isoformat()
        })
        save_project_data(data)
        print("\n✅ 이슈가 등록되었습니다.")

def main():
    import sys

    if len(sys.argv) < 2:
        show_dashboard()
        return

    command = sys.argv[1].lower()

    if command == 'init':
        init_project()
    elif command == 'set':
        set_current_phase()
    elif command == 'milestone':
        add_milestone()
    elif command == 'issue':
        add_issue()
    elif command == 'status':
        show_dashboard()
    else:
        print(f"알 수 없는 명령어: {command}")
        print("사용법: python pm_dashboard.py [init|set|milestone|issue|status]")

if __name__ == "__main__":
    main()
