"""Refuse common private or proprietary artifacts in tracked Git files."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys


FORBIDDEN_NAMES = {
    "resources.assets",
    "resources.assets.resS",
}
FORBIDDEN_PARTS = {
    ".codex",
    ".agents",
    "work",
    "outputs",
}
FORBIDDEN_SUFFIXES = {
    ".jsonl",
    ".log",
    ".spec",
}
PRIVATE_TEXT = (
    re.compile(rb"/Users/[A-Za-z0-9._-]+/"),
    re.compile(rb"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+\\"),
)


def tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [root / item.decode() for item in result.stdout.split(b"\0") if item]


def audit(root: Path) -> list[str]:
    problems: list[str] = []
    for path in tracked_files(root):
        relative = path.relative_to(root)
        if path.name in FORBIDDEN_NAMES:
            problems.append(f"fichier du jeu suivi : {relative}")
        if FORBIDDEN_PARTS.intersection(relative.parts):
            problems.append(f"répertoire privé suivi : {relative}")
        if path.suffix in FORBIDDEN_SUFFIXES:
            problems.append(f"artefact local suivi : {relative}")
        if not path.is_file() or path.stat().st_size > 5_000_000:
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        if any(pattern.search(data) for pattern in PRIVATE_TEXT):
            problems.append(f"chemin utilisateur trouvé : {relative}")
    return problems


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    problems = audit(root)
    if problems:
        print("Audit public refusé :", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1
    print("Audit public réussi : aucun artefact privé ou fichier du jeu suivi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
