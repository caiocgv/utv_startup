#!/usr/bin/env python3
"""
tools/engdb/generate_diagrams.py

Runner script: generates all Mermaid diagrams under docs/_generated/.

Usage:
    python tools/engdb/generate_diagrams.py [--repo-root REPO_ROOT]

If --repo-root is not specified, the script resolves the repository root as
the directory three levels above this file (tools/engdb/ → tools/ → repo/).
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

# Allow running as a standalone script without installing the package.
_TOOLS_DIR = Path(__file__).resolve().parent.parent  # tools/
if str(_TOOLS_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR.parent))

from tools.engdb.diagrams import GENERATED_DIR, generate_all


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate Mermaid diagrams from engineering database metadata."
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Path to the repository root. Defaults to auto-detected root.",
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[2]
    out_dir = repo_root / GENERATED_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    diagrams = generate_all(str(repo_root), today)

    changed: list[str] = []
    for filename, content in sorted(diagrams.items()):
        out_path = out_dir / filename
        existing = out_path.read_text(encoding="utf-8") if out_path.exists() else None
        if existing != content:
            out_path.write_text(content, encoding="utf-8")
            changed.append(filename)
            print(f"  [updated] {GENERATED_DIR}/{filename}")
        else:
            print(f"  [no change] {GENERATED_DIR}/{filename}")

    if changed:
        print(f"\n✅ {len(changed)} diagram(s) updated.")
    else:
        print("\n✅ All diagrams are up to date.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
