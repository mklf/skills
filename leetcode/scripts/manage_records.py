#!/usr/bin/env python3
"""Manage LeetCode practice records for the teaching skill.

This script keeps JSON files in ~/.leetcode_records/:
- leetcode.json: all issued problems
- leetcode_struggle.json: problems where the user asked for help
- leetcode_mastered.json: problems the user has mastered
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path.home() / ".leetcode_records"
ISSUED_PATH = BASE_DIR / "leetcode.json"
STRUGGLE_PATH = BASE_DIR / "leetcode_struggle.json"
MASTERED_PATH = BASE_DIR / "leetcode_mastered.json"


def _empty_payload() -> Dict[str, List[Dict[str, Any]]]:
    return {"problems": []}


def _today() -> str:
    return date.today().isoformat()


def _days_since(added_at: str | None) -> int | None:
    if not added_at:
        return None
    try:
        return (date.today() - datetime.fromisoformat(added_at).date()).days
    except ValueError:
        return None


def _save(path: Path, data: Dict[str, List[Dict[str, Any]]]) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _load(path: Path) -> Dict[str, List[Dict[str, Any]]]:
    if not path.exists():
        return _empty_payload()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _empty_payload()
    if (
        not isinstance(data, dict)
        or "problems" not in data
        or not isinstance(data["problems"], list)
    ):
        return _empty_payload()
    today = _today()
    if any("added_at" not in item for item in data["problems"]):
        for item in data["problems"]:
            item.setdefault("added_at", today)
        _save(path, data)
    return data


def init_files() -> None:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    for path in (ISSUED_PATH, STRUGGLE_PATH, MASTERED_PATH):
        if not path.exists():
            _save(path, _empty_payload())


def _has_problem(path: Path, problem_id: int) -> bool:
    data = _load(path)
    return any(item.get("id") == problem_id for item in data["problems"])


def add_problem(path: Path, problem_id: int, name: str | None = None) -> bool:
    data = _load(path)
    if any(item.get("id") == problem_id for item in data["problems"]):
        return False
    item: Dict[str, Any] = {"id": problem_id, "added_at": _today()}
    if name:
        item["name"] = name
    data["problems"].append(item)
    _save(path, data)
    return True


def remove_problems(path: Path, problem_ids: List[int]) -> List[int]:
    data = _load(path)
    targets = set(problem_ids)
    removed = []
    for item in data["problems"]:
        id_val = item.get("id")
        if isinstance(id_val, int) and id_val in targets:
            removed.append(id_val)
    if removed:
        data["problems"] = [
            item for item in data["problems"] if item.get("id") not in targets
        ]
        _save(path, data)
    return removed


def cmd_exists(args: argparse.Namespace) -> None:
    ids = list(dict.fromkeys(args.id))
    issued, not_issued = [], []
    for problem_id in ids:
        (issued if _has_problem(ISSUED_PATH, problem_id) else not_issued).append(
            problem_id
        )
    print(f"已出过: {'、'.join(str(i) for i in issued) if issued else '无'}")
    print(f"未出过: {'、'.join(str(i) for i in not_issued) if not_issued else '无'}")


def cmd_add_issued(args: argparse.Namespace) -> None:
    created = add_problem(ISSUED_PATH, args.id, args.name)
    print("added" if created else "duplicate")


def cmd_add_struggle(args: argparse.Namespace) -> None:
    created = add_problem(STRUGGLE_PATH, args.id, args.name)
    print("added" if created else "duplicate")


def _report_removed(removed: List[int], requested: List[int]) -> None:
    removed_set = set(removed)
    not_found = [i for i in dict.fromkeys(requested) if i not in removed_set]
    print(f"已删除: {'、'.join(str(i) for i in removed) if removed else '无'}")
    print(f"未找到: {'、'.join(str(i) for i in not_found) if not_found else '无'}")


def cmd_delete_issued(args: argparse.Namespace) -> None:
    _report_removed(remove_problems(ISSUED_PATH, args.id), args.id)


def cmd_delete_struggle(args: argparse.Namespace) -> None:
    _report_removed(remove_problems(STRUGGLE_PATH, args.id), args.id)


def cmd_mark_mastered(args: argparse.Namespace) -> None:
    ids = list(dict.fromkeys(args.id))
    struggle_data = _load(STRUGGLE_PATH)
    struggle_map = {item.get("id"): item for item in struggle_data["problems"]}
    for problem_id in ids:
        remove_problems(STRUGGLE_PATH, [problem_id])
        name = struggle_map.get(problem_id, {}).get("name")
        added = add_problem(MASTERED_PATH, problem_id, name)
        print(f"{problem_id}: {'已标记为掌握' if added else '已在掌握列表'}")


def cmd_review(args: argparse.Namespace) -> None:
    problems = _load(STRUGGLE_PATH)["problems"]
    rows = []
    for item in problems:
        days = _days_since(item.get("added_at"))
        if args.min_days is not None and (days is None or days < args.min_days):
            continue
        rows.append((item.get("id"), item.get("name", ""), item.get("added_at", "未知"), days))

    if not rows:
        print("暂无需要复习的题目")
        return

    rows.sort(key=lambda r: r[3] if r[3] is not None else -1, reverse=True)
    print(f"{'题号':<8} {'题名':<20} {'添加日期':<12} 距今天数")
    print("-" * 52)
    for problem_id, name, added_at, days in rows:
        days_text = f"{days} 天" if days is not None else "未知"
        print(f"{problem_id:<8} {(name[:18] or '-'):<20} {added_at:<12} {days_text}")


def cmd_list_issued(args: argparse.Namespace) -> None:
    problems = _load(ISSUED_PATH)["problems"]
    if not problems:
        print("暂无已出题记录")
        return
    problems_sorted = sorted(problems, key=lambda x: x.get("added_at") or "", reverse=True)
    print(f"{'题号':<8} {'题名':<20} 添加日期")
    print("-" * 44)
    for item in problems_sorted:
        name = item.get("name", "-") or "-"
        print(f"{item.get('id', '?'):<8} {name[:18]:<20} {item.get('added_at', '未知')}")


def cmd_stats(args: argparse.Namespace) -> None:
    issued = _load(ISSUED_PATH)["problems"]
    struggle = _load(STRUGGLE_PATH)["problems"]
    mastered = _load(MASTERED_PATH)["problems"]

    total_issued = len(issued)
    total_struggle = len(struggle)
    total_mastered = len(mastered)
    recent_7 = sum(
        1 for item in issued
        if (_days_since(item.get("added_at")) or 0) <= 7
        and _days_since(item.get("added_at")) is not None
    )
    struggle_rate = (
        f"{total_struggle / total_issued * 100:.0f}%" if total_issued else "N/A"
    )
    mastery_rate = (
        f"{total_mastered / (total_struggle + total_mastered) * 100:.0f}%"
        if (total_struggle + total_mastered) > 0
        else "N/A"
    )
    print(f"总出题数    : {total_issued}")
    print(f"近 7 天出题 : {recent_7}")
    print(f"待复习      : {total_struggle}")
    print(f"已掌握      : {total_mastered}")
    print(f"卡壳率      : {struggle_rate}")
    print(f"掌握率      : {mastery_rate}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage LeetCode skill record files.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_exists = sub.add_parser("exists", help="Check if problem ids are already issued.")
    p_exists.add_argument("--id", type=int, nargs="+", required=True)
    p_exists.set_defaults(func=cmd_exists)

    p_add_issued = sub.add_parser("add-issued", help="Add an issued problem record.")
    p_add_issued.add_argument("--id", type=int, required=True)
    p_add_issued.add_argument("--name", type=str, default=None, help="Problem title")
    p_add_issued.set_defaults(func=cmd_add_issued)

    p_add_struggle = sub.add_parser("add-struggle", help="Add a struggle/help record.")
    p_add_struggle.add_argument("--id", type=int, required=True)
    p_add_struggle.add_argument("--name", type=str, default=None, help="Problem title")
    p_add_struggle.set_defaults(func=cmd_add_struggle)

    p_del_issued = sub.add_parser("delete-issued", help="Delete issued records.")
    p_del_issued.add_argument("--id", type=int, nargs="+", required=True)
    p_del_issued.set_defaults(func=cmd_delete_issued)

    p_del_struggle = sub.add_parser("delete-struggle", help="Delete struggle records.")
    p_del_struggle.add_argument("--id", type=int, nargs="+", required=True)
    p_del_struggle.set_defaults(func=cmd_delete_struggle)

    p_mastered = sub.add_parser(
        "mark-mastered", help="Move problem(s) from struggle to mastered."
    )
    p_mastered.add_argument("--id", type=int, nargs="+", required=True)
    p_mastered.set_defaults(func=cmd_mark_mastered)

    p_review = sub.add_parser("review", help="List struggle problems with days since added.")
    p_review.add_argument(
        "--min-days", type=int, default=None, dest="min_days",
        help="Only show problems waiting at least N days"
    )
    p_review.set_defaults(func=cmd_review)

    sub.add_parser("list-issued", help="List all issued problems.").set_defaults(
        func=cmd_list_issued
    )
    sub.add_parser("stats", help="Show practice statistics.").set_defaults(
        func=cmd_stats
    )

    return parser


def main() -> None:
    init_files()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
