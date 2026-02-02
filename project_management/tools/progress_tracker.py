#!/usr/bin/env python3
"""
프로젝트 진행 상황 추적 도구
R&D 프로젝트의 진행 현황을 추적하고 보고서를 생성하는 CLI 도구
"""

import os
import re
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "tools" / ".progress_history.json"
PROJECT_DATA = PROJECT_ROOT / "tools" / ".project_data.json"

PHASES = {
    '1': {'folder': '01_planning', 'name': '기획 단계', 'weight': 0.20},
    '2': {'folder': '02_preparation', 'name': '준비 단계', 'weight': 0.20},
    '3': {'folder': '03_execution', 'name': '수행 단계', 'weight': 0.40},
    '4': {'folder': '04_operation', 'name': '운영·확산 단계', 'weight': 0.20},
}

def load_history() -> List[Dict]:
    """진행 이력 로드"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history: List[Dict]):
    """진행 이력 저장"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_project_data() -> Dict:
    """프로젝트 데이터 로드"""
    if PROJECT_DATA.exists():
        with open(PROJECT_DATA, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def get_phase_progress(phase_num: str) -> Dict:
    """단계별 진행률 계산"""
    info = PHASES.get(phase_num)
    if not info:
        return {'completed': 0, 'total': 0, 'percentage': 0}

    checklist_path = PROJECT_ROOT / info['folder'] / "CHECKLIST.md"
    if not checklist_path.exists():
        return {'completed': 0, 'total': 0, 'percentage': 0}

    with open(checklist_path, 'r', encoding='utf-8') as f:
        content = f.read()

    checked = len(re.findall(r'- \[x\]', content, re.IGNORECASE))
    unchecked = len(re.findall(r'- \[ \]', content))
    total = checked + unchecked

    return {
        'completed': checked,
        'total': total,
        'percentage': (checked / total * 100) if total > 0 else 0
    }

def get_overall_progress() -> Dict:
    """전체 가중 진행률 계산"""
    weighted_sum = 0
    phases_data = {}

    for phase_num, info in PHASES.items():
        progress = get_phase_progress(phase_num)
        phases_data[phase_num] = progress
        weighted_sum += progress['percentage'] * info['weight']

    return {
        'overall_percentage': weighted_sum,
        'phases': phases_data
    }

def record_snapshot():
    """현재 진행 상황 스냅샷 기록"""
    history = load_history()
    progress = get_overall_progress()

    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'overall': progress['overall_percentage'],
        'phases': {k: v['percentage'] for k, v in progress['phases'].items()}
    }

    history.append(snapshot)
    save_history(history)

    print(f"✅ 진행 상황이 기록되었습니다. (전체: {progress['overall_percentage']:.1f}%)")

def show_progress():
    """현재 진행 상황 표시"""
    progress = get_overall_progress()
    project = load_project_data()

    print("\n" + "=" * 70)
    print("        프로젝트 진행 현황")
    print("=" * 70)

    if project.get('project_name'):
        print(f"\n📋 {project['project_name']}")

    # 전체 진행률
    overall = progress['overall_percentage']
    bar_width = 40
    filled = int(bar_width * overall / 100)
    bar = "█" * filled + "░" * (bar_width - filled)

    print(f"\n📊 전체 진행률 (가중치 적용)")
    print(f"   [{bar}] {overall:.1f}%")

    # 단계별 진행률
    print("\n" + "-" * 70)
    print("📈 단계별 진행률")
    print("-" * 70)

    for phase_num, info in PHASES.items():
        phase_data = progress['phases'][phase_num]
        pct = phase_data['percentage']
        completed = phase_data['completed']
        total = phase_data['total']

        bar_width = 25
        filled = int(bar_width * pct / 100)
        bar = "█" * filled + "░" * (bar_width - filled)

        weight_str = f"(가중치: {info['weight']*100:.0f}%)"
        print(f"\n   {info['name']} {weight_str}")
        print(f"   [{bar}] {pct:.1f}% ({completed}/{total})")

    print("\n" + "=" * 70 + "\n")

def show_trend():
    """진행 추세 표시"""
    history = load_history()

    if len(history) < 2:
        print("\n⚠️  추세 분석을 위해 최소 2개의 기록이 필요합니다.")
        print("   'python progress_tracker.py record' 명령으로 기록을 추가하세요.\n")
        return

    print("\n" + "=" * 70)
    print("        진행 추세 분석")
    print("=" * 70)

    # 최근 10개 기록
    recent = history[-10:]

    print("\n📈 최근 진행 기록")
    print("-" * 70)

    prev_overall = None
    for record in recent:
        dt = datetime.fromisoformat(record['timestamp'])
        overall = record['overall']

        if prev_overall is not None:
            diff = overall - prev_overall
            trend = f"(+{diff:.1f}%)" if diff > 0 else f"({diff:.1f}%)" if diff < 0 else "(변화없음)"
        else:
            trend = ""

        print(f"   {dt.strftime('%Y-%m-%d %H:%M')} : {overall:5.1f}% {trend}")
        prev_overall = overall

    # 주간 변화 분석
    if len(history) >= 2:
        first = history[0]
        last = history[-1]

        first_dt = datetime.fromisoformat(first['timestamp'])
        last_dt = datetime.fromisoformat(last['timestamp'])
        days = (last_dt - first_dt).days or 1

        total_progress = last['overall'] - first['overall']
        daily_rate = total_progress / days

        print("\n" + "-" * 70)
        print("📊 진행 분석")
        print("-" * 70)
        print(f"   총 기록 기간: {days}일")
        print(f"   총 진행률 변화: {total_progress:+.1f}%")
        print(f"   일일 평균 진행: {daily_rate:+.2f}%")

        # 완료 예측
        remaining = 100 - last['overall']
        if daily_rate > 0:
            estimated_days = remaining / daily_rate
            estimated_date = last_dt + timedelta(days=estimated_days)
            print(f"\n   🎯 예상 완료일: {estimated_date.strftime('%Y-%m-%d')} (현재 속도 유지 시)")

    print("\n" + "=" * 70 + "\n")

def generate_report():
    """진행 보고서 생성"""
    progress = get_overall_progress()
    project = load_project_data()
    history = load_history()

    report_date = datetime.now().strftime('%Y-%m-%d')
    report_path = PROJECT_ROOT / f"progress_report_{report_date}.md"

    content = f"""# 프로젝트 진행 보고서

**생성일시**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**프로젝트**: {project.get('project_name', 'R&D 프로젝트')}
**PM**: {project.get('pm_name', '-')}

---

## 전체 진행 현황

| 항목 | 값 |
|------|-----|
| 전체 진행률 | {progress['overall_percentage']:.1f}% |

## 단계별 진행률

| 단계 | 진행률 | 완료/전체 | 가중치 |
|------|--------|----------|--------|
"""

    for phase_num, info in PHASES.items():
        phase_data = progress['phases'][phase_num]
        content += f"| {info['name']} | {phase_data['percentage']:.1f}% | {phase_data['completed']}/{phase_data['total']} | {info['weight']*100:.0f}% |\n"

    # 이슈 섹션
    if project.get('issues'):
        active_issues = [i for i in project['issues'] if not i.get('resolved')]
        if active_issues:
            content += "\n## 활성 이슈\n\n"
            for issue in active_issues:
                priority_icon = "🔴" if issue.get('priority') == 'high' else ("🟡" if issue.get('priority') == 'medium' else "🟢")
                content += f"- {priority_icon} {issue.get('title', '')}\n"

    # 마일스톤 섹션
    if project.get('milestones'):
        content += "\n## 마일스톤 현황\n\n"
        for ms in project['milestones']:
            status = "✅" if ms.get('completed') else "⏳"
            content += f"- {status} [{ms.get('date', 'TBD')}] {ms.get('title', '')}\n"

    content += f"""
---

*이 보고서는 progress_tracker.py에 의해 자동 생성되었습니다.*
"""

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ 보고서가 생성되었습니다: {report_path}\n")

def main():
    if len(sys.argv) < 2:
        show_progress()
        return

    cmd = sys.argv[1].lower()

    if cmd == 'status' or cmd == 's':
        show_progress()
    elif cmd == 'record' or cmd == 'r':
        record_snapshot()
    elif cmd == 'trend' or cmd == 't':
        show_trend()
    elif cmd == 'report':
        generate_report()
    elif cmd == 'help':
        print("""
진행 상황 추적 도구 사용법:

  python progress_tracker.py              현재 진행 상황 표시
  python progress_tracker.py status       현재 진행 상황 표시
  python progress_tracker.py record       현재 상황 스냅샷 기록
  python progress_tracker.py trend        진행 추세 분석
  python progress_tracker.py report       진행 보고서 생성 (Markdown)
        """)
    else:
        print("알 수 없는 명령어입니다. 'help' 명령어를 사용하세요.")

if __name__ == "__main__":
    main()
