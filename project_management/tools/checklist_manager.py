#!/usr/bin/env python3
"""
체크리스트 관리 도구
R&D 프로젝트의 각 단계별 체크리스트를 관리하는 CLI 도구
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict

PROJECT_ROOT = Path(__file__).parent.parent

PHASES = {
    '1': ('01_planning', '기획 단계'),
    '2': ('02_preparation', '준비 단계'),
    '3': ('03_execution', '수행 단계'),
    '4': ('04_operation', '운영·확산 단계'),
}

def get_checklist_path(phase_num: str) -> Path:
    """체크리스트 파일 경로 반환"""
    if phase_num not in PHASES:
        return None
    folder, _ = PHASES[phase_num]
    return PROJECT_ROOT / folder / "CHECKLIST.md"

def parse_tasks(content: str) -> List[Dict]:
    """체크리스트에서 태스크 추출"""
    tasks = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        # 체크박스 패턴 매칭
        match = re.match(r'^(\s*)- \[([ xX])\] (.+)$', line)
        if match:
            indent, status, text = match.groups()
            tasks.append({
                'line_num': i,
                'indent': len(indent),
                'completed': status.lower() == 'x',
                'text': text.strip(),
                'original': line
            })

    return tasks

def display_tasks(tasks: List[Dict], show_completed: bool = True):
    """태스크 목록 표시"""
    for i, task in enumerate(tasks, 1):
        if not show_completed and task['completed']:
            continue

        status = "✅" if task['completed'] else "⬜"
        indent = "  " * (task['indent'] // 2)
        print(f"  {i:2d}. {indent}{status} {task['text']}")

def show_status():
    """전체 상태 표시"""
    print("\n" + "=" * 60)
    print("        체크리스트 현황")
    print("=" * 60 + "\n")

    total_completed = 0
    total_tasks = 0

    for phase_num, (folder, name) in PHASES.items():
        path = get_checklist_path(phase_num)
        if not path.exists():
            print(f"  {phase_num}. {name}: 파일 없음")
            continue

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        tasks = parse_tasks(content)
        completed = sum(1 for t in tasks if t['completed'])
        total = len(tasks)

        total_completed += completed
        total_tasks += total

        pct = (completed / total * 100) if total > 0 else 0
        bar_width = 20
        filled = int(bar_width * pct / 100)
        bar = "█" * filled + "░" * (bar_width - filled)

        print(f"  {phase_num}. {name}")
        print(f"     [{bar}] {pct:.1f}% ({completed}/{total})")
        print()

    print("-" * 60)
    overall_pct = (total_completed / total_tasks * 100) if total_tasks > 0 else 0
    print(f"  전체 진행률: {overall_pct:.1f}% ({total_completed}/{total_tasks})")
    print("=" * 60 + "\n")

def show_phase(phase_num: str, pending_only: bool = False):
    """특정 단계 태스크 표시"""
    if phase_num not in PHASES:
        print(f"올바른 단계 번호를 입력하세요 (1-4)")
        return

    folder, name = PHASES[phase_num]
    path = get_checklist_path(phase_num)

    if not path.exists():
        print(f"체크리스트 파일이 없습니다: {path}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    tasks = parse_tasks(content)

    print(f"\n{'=' * 60}")
    print(f"  {name} 체크리스트")
    print(f"{'=' * 60}\n")

    if pending_only:
        print("  [미완료 항목만 표시]\n")

    display_tasks(tasks, show_completed=not pending_only)

    completed = sum(1 for t in tasks if t['completed'])
    print(f"\n  진행률: {completed}/{len(tasks)} ({completed/len(tasks)*100:.1f}%)\n")

def toggle_task(phase_num: str, task_num: int):
    """태스크 완료 상태 토글"""
    path = get_checklist_path(phase_num)
    if not path or not path.exists():
        print("체크리스트 파일을 찾을 수 없습니다.")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    tasks = parse_tasks(content)

    if task_num < 1 or task_num > len(tasks):
        print(f"올바른 태스크 번호를 입력하세요 (1-{len(tasks)})")
        return

    task = tasks[task_num - 1]
    lines = content.split('\n')

    # 상태 토글
    if task['completed']:
        new_line = lines[task['line_num']].replace('[x]', '[ ]').replace('[X]', '[ ]')
        new_status = "미완료"
    else:
        new_line = lines[task['line_num']].replace('[ ]', '[x]')
        new_status = "완료"

    lines[task['line_num']] = new_line

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n✅ '{task['text']}' → {new_status}")

def batch_complete(phase_num: str, task_nums: List[int]):
    """여러 태스크 일괄 완료"""
    path = get_checklist_path(phase_num)
    if not path or not path.exists():
        print("체크리스트 파일을 찾을 수 없습니다.")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    tasks = parse_tasks(content)
    lines = content.split('\n')

    completed_items = []
    for num in task_nums:
        if 1 <= num <= len(tasks):
            task = tasks[num - 1]
            if not task['completed']:
                lines[task['line_num']] = lines[task['line_num']].replace('[ ]', '[x]')
                completed_items.append(task['text'])

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n✅ {len(completed_items)}개 항목 완료 처리:")
    for item in completed_items:
        print(f"   - {item}")

def interactive_mode():
    """대화형 모드"""
    print("\n" + "=" * 60)
    print("        체크리스트 관리 (대화형 모드)")
    print("=" * 60)
    print("\n명령어:")
    print("  s       - 전체 상태 보기")
    print("  1-4     - 해당 단계 보기")
    print("  1p, 2p  - 해당 단계 미완료만 보기")
    print("  1.5     - 1단계 5번 항목 토글")
    print("  1.3-7   - 1단계 3~7번 일괄 완료")
    print("  q       - 종료")
    print("-" * 60 + "\n")

    while True:
        try:
            cmd = input(">>> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if not cmd:
            continue

        if cmd == 'q':
            break
        elif cmd == 's':
            show_status()
        elif cmd in ['1', '2', '3', '4']:
            show_phase(cmd)
        elif cmd in ['1p', '2p', '3p', '4p']:
            show_phase(cmd[0], pending_only=True)
        elif '.' in cmd:
            parts = cmd.split('.')
            if len(parts) == 2:
                phase = parts[0]
                if '-' in parts[1]:
                    # 범위 지정 (예: 1.3-7)
                    start, end = parts[1].split('-')
                    try:
                        nums = list(range(int(start), int(end) + 1))
                        batch_complete(phase, nums)
                    except ValueError:
                        print("올바른 형식: 단계.시작-끝 (예: 1.3-7)")
                else:
                    # 단일 항목 (예: 1.5)
                    try:
                        toggle_task(phase, int(parts[1]))
                    except ValueError:
                        print("올바른 형식: 단계.번호 (예: 1.5)")
        else:
            print("알 수 없는 명령어입니다.")

def main():
    if len(sys.argv) < 2:
        show_status()
        return

    cmd = sys.argv[1].lower()

    if cmd == 'status':
        show_status()
    elif cmd == 'interactive' or cmd == 'i':
        interactive_mode()
    elif cmd in ['1', '2', '3', '4']:
        pending = len(sys.argv) > 2 and sys.argv[2] == '--pending'
        show_phase(cmd, pending_only=pending)
    elif cmd == 'toggle' and len(sys.argv) >= 4:
        toggle_task(sys.argv[2], int(sys.argv[3]))
    elif cmd == 'help':
        print("""
체크리스트 관리 도구 사용법:

  python checklist_manager.py                  전체 상태 보기
  python checklist_manager.py status           전체 상태 보기
  python checklist_manager.py 1                1단계 체크리스트 보기
  python checklist_manager.py 1 --pending      1단계 미완료 항목만 보기
  python checklist_manager.py toggle 1 5       1단계 5번 항목 토글
  python checklist_manager.py i                대화형 모드
        """)
    else:
        print("알 수 없는 명령어입니다. 'help' 명령어를 사용하세요.")

if __name__ == "__main__":
    main()
