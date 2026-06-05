#!/usr/bin/env python3
"""Package a skill directory into a zip file.

Usage:
  python package_skill.py <skill_dir>
  python package_skill.py <skill_dir> --output /path/to/out.zip
"""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package a skill directory into a zip archive."
    )
    parser.add_argument(
        "skill_dir",
        type=Path,
        help="Path to the skill directory (must contain SKILL.md).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Optional output zip path. Default: <repo_root>/<skill_name>.zip",
    )
    return parser.parse_args()


def validate_skill_dir(skill_dir: Path) -> Path:
    resolved = skill_dir.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Skill directory not found: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Not a directory: {resolved}")
    if not (resolved / "SKILL.md").exists():
        raise ValueError(f"Invalid skill directory (missing SKILL.md): {resolved}")
    return resolved


def should_skip(path: Path) -> bool:
    name = path.name
    if name == ".DS_Store":
        return True
    if name == "__pycache__":
        return True
    return False


def package_skill(skill_dir: Path, output_zip: Path) -> Path:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    root_name = skill_dir.name

    with ZipFile(output_zip, mode="w", compression=ZIP_DEFLATED) as zf:
        for path in sorted(skill_dir.rglob("*")):
            if should_skip(path):
                continue
            if path.is_file():
                rel_inside_skill = path.relative_to(skill_dir)
                arcname = Path(root_name) / rel_inside_skill
                zf.write(path, arcname.as_posix())

    return output_zip


def main() -> None:
    args = parse_args()
    skill_dir = validate_skill_dir(args.skill_dir)

    if args.output is None:
        output_zip = Path.cwd() / f"{skill_dir.name}.zip"
    else:
        output_zip = args.output.expanduser().resolve()

    result = package_skill(skill_dir, output_zip)
    print(f"打包完成: {result}")


if __name__ == "__main__":
    main()
