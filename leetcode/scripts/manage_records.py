#!/usr/bin/env python3
"""Manage LeetCode practice records for the teaching skill.

This script keeps two JSON files under the skill directory:
- leetcode.json: all issued problems
- leetcode_struggle.json: problems where the user asked for help
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path.home() / ".leetcode_records"
ISSUED_PATH = BASE_DIR / "leetcode.json"
STRUGGLE_PATH = BASE_DIR / "leetcode_struggle.json"


def _empty_payload() -> Dict[str, List[Dict[str, Any]]]:
    return {"problems": []}


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
    return data


def _save(path: Path, data: Dict[str, List[Dict[str, Any]]]) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def init_files() -> None:
    # Ensure the base directory exists under the user's home
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    for path in (ISSUED_PATH, STRUGGLE_PATH):
        if not path.exists():
            _save(path, _empty_payload())


def _has_problem(path: Path, problem_id: int) -> bool:
    data = _load(path)
    return any(item.get("id") == problem_id for item in data["problems"])


def add_problem(path: Path, problem_id: int) -> bool:
    data = _load(path)
    if any(item.get("id") == problem_id for item in data["problems"]):
        return False

    item = {"id": problem_id}
    data["problems"].append(item)
    _save(path, data)
    return True


def remove_problems(path: Path, problem_ids: List[int]) -> List[int]:
    """Delete the given ids from a record file.

    Returns the list of ids that were actually present and removed.
    """
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
    issued = []
    not_issued = []
    for problem_id in ids:
        exists = _has_problem(ISSUED_PATH, problem_id)
        if exists:
            issued.append(problem_id)
        else:
            not_issued.append(problem_id)

    issued_text = "、".join(str(i) for i in issued) if issued else "无"
    not_issued_text = "、".join(str(i) for i in not_issued) if not_issued else "无"
    print(f"已出过: {issued_text}")
    print(f"未出过: {not_issued_text}")


def cmd_add_issued(args: argparse.Namespace) -> None:
    created = add_problem(ISSUED_PATH, args.id)
    print("added" if created else "duplicate")


def cmd_add_struggle(args: argparse.Namespace) -> None:
    created = add_problem(STRUGGLE_PATH, args.id)
    print("added" if created else "duplicate")


def _report_removed(removed: List[int], requested: List[int]) -> None:
    requested_unique = list(dict.fromkeys(requested))
    removed_set = set(removed)
    not_found = [i for i in requested_unique if i not in removed_set]

    removed_text = "、".join(str(i) for i in removed) if removed else "无"
    not_found_text = "、".join(str(i) for i in not_found) if not_found else "无"
    print(f"已删除: {removed_text}")
    print(f"未找到: {not_found_text}")


def cmd_delete_issued(args: argparse.Namespace) -> None:
    removed = remove_problems(ISSUED_PATH, args.id)
    _report_removed(removed, args.id)


def cmd_delete_struggle(args: argparse.Namespace) -> None:
    removed = remove_problems(STRUGGLE_PATH, args.id)
    _report_removed(removed, args.id)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage LeetCode skill record files.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_exists = sub.add_parser("exists", help="Check if a problem id is already issued.")
    p_exists.add_argument(
        "--id",
        type=int,
        nargs="+",
        required=True,
        help="One or more LeetCode problem ids",
    )
    p_exists.set_defaults(func=cmd_exists)

    p_add_issued = sub.add_parser("add-issued", help="Add an issued problem record.")
    p_add_issued.add_argument(
        "--id", type=int, required=True, help="LeetCode problem id"
    )
    p_add_issued.set_defaults(func=cmd_add_issued)

    p_add_struggle = sub.add_parser("add-struggle", help="Add a struggle/help record.")
    p_add_struggle.add_argument(
        "--id", type=int, required=True, help="LeetCode problem id"
    )
    p_add_struggle.set_defaults(func=cmd_add_struggle)

    p_del_issued = sub.add_parser(
        "delete-issued", help="Delete one or more issued problem records."
    )
    p_del_issued.add_argument(
        "--id",
        type=int,
        nargs="+",
        required=True,
        help="One or more LeetCode problem ids",
    )
    p_del_issued.set_defaults(func=cmd_delete_issued)

    p_del_struggle = sub.add_parser(
        "delete-struggle", help="Delete one or more struggle/help records."
    )
    p_del_struggle.add_argument(
        "--id",
        type=int,
        nargs="+",
        required=True,
        help="One or more LeetCode problem ids",
    )
    p_del_struggle.set_defaults(func=cmd_delete_struggle)

    return parser


def main() -> None:
    init_files()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
