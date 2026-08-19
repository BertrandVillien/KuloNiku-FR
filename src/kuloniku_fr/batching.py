from __future__ import annotations

import csv
from dataclasses import dataclass
import json
from pathlib import Path
import re


SOURCE_FIELDS = [
    "key",
    "english",
    "indonesian",
    "spanish",
    "thai",
    "chinese_simplified",
    "chinese_traditional",
    "german",
    "portuguese",
]


@dataclass
class Batch:
    identifier: str
    group: str
    rows: list[dict[str, str]]
    characters: int


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def translated_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {row["key"] for row in read_csv_rows(path) if row.get("fr")}


def row_characters(row: dict[str, str]) -> int:
    return sum(len(row.get(field, "")) for field in SOURCE_FIELDS)


def semantic_group(key: str) -> str:
    if key.startswith("Dialogue/"):
        remainder = key.removeprefix("Dialogue/")
        return "dialogue-" + remainder.split("_", 1)[0].lower()
    prefix = key.split("_", 1)[0].split("/", 1)[0]
    return "system-" + re.sub(r"[^a-z0-9]+", "-", prefix.lower()).strip("-")


CULINARY_PREFIXES = {
    "action", "boiling", "container", "cooking", "crafting", "dish", "drink",
    "food", "frying", "ingredient", "ingredientset", "ingredienttype", "recipe",
    "seasoning", "sidedish", "skewer", "taste", "tool", "tools", "utensil",
}
WORLD_PREFIXES = {
    "character", "contest", "decoration", "festival", "friendship", "hangout",
    "journal", "location", "mail", "night", "quest", "relationship", "shop",
}


def macro_group(group: str) -> str:
    if group.startswith("dialogue-"):
        return "dialogue"
    prefix = group.removeprefix("system-")
    if prefix in CULINARY_PREFIXES:
        return "culinary"
    if prefix in WORLD_PREFIXES:
        return "world"
    return "interface-gameplay"


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value[:48] or "misc"


def make_batches(
    source_rows: list[dict[str, str]],
    done_keys: set[str],
    *,
    character_budget: int = 60_000,
) -> list[Batch]:
    pending = [
        row
        for row in source_rows
        if row["key"] not in done_keys
        and not row["key"].startswith("Dialogue (Backup)/")
        and any(row.get(field, "") for field in SOURCE_FIELDS[1:])
    ]
    grouped: dict[str, list[dict[str, str]]] = {}
    order: list[str] = []
    for row in pending:
        group = semantic_group(row["key"])
        if group not in grouped:
            grouped[group] = []
            order.append(group)
        grouped[group].append(row)

    batches: list[Batch] = []
    sequence = 1
    current_rows: list[dict[str, str]] = []
    current_groups: list[str] = []
    current_chars = 0
    current_macro = ""

    def flush() -> None:
        nonlocal sequence, current_rows, current_groups, current_chars
        if not current_rows:
            return
        label = current_groups[0]
        if current_groups[-1] != label:
            label = f"{label}-to-{current_groups[-1]}"
        identifier = f"{sequence:03d}-{slug(current_macro)}-{slug(label)}"
        batches.append(Batch(identifier, ",".join(current_groups), current_rows, current_chars))
        sequence += 1
        current_rows = []
        current_groups = []
        current_chars = 0

    ordered_groups = [
        group
        for macro_name in ("culinary", "interface-gameplay", "world", "dialogue")
        for group in order
        if macro_group(group) == macro_name
    ]
    for group in ordered_groups:
        macro = macro_group(group)
        if current_rows and macro != current_macro:
            flush()
        current_macro = macro
        for row in grouped[group]:
            size = row_characters(row)
            if current_rows and current_chars + size > character_budget:
                flush()
            if not current_groups or current_groups[-1] != group:
                current_groups.append(group)
            current_rows.append(row)
            current_chars += size
        # A coherent group may exceed the budget only by one unusually long row.
        if current_chars >= character_budget:
            flush()
    flush()
    return batches


def write_batches(
    batches: list[Batch], source_dir: Path, output_dir: Path, manifest_path: Path
) -> None:
    source_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for batch in batches:
        source_path = source_dir / f"{batch.identifier}.csv"
        output_path = output_dir / f"{batch.identifier}.csv"
        with source_path.open("w", newline="", encoding="utf-8") as stream:
            fields = [*SOURCE_FIELDS, "max_source_chars"]
            writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            for row in batch.rows:
                item = {field: row.get(field, "") for field in SOURCE_FIELDS}
                item["max_source_chars"] = max(
                    (len(row.get(field, "")) for field in SOURCE_FIELDS[1:] if row.get(field, "")),
                    default=0,
                )
                writer.writerow(item)
        manifest.append(
            {
                "id": batch.identifier,
                "group": batch.group,
                "rows": len(batch.rows),
                "characters": batch.characters,
                "source": str(source_path),
                "output": str(output_path),
                "status": "done" if output_path.exists() else "pending",
            }
        )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def propagate_dialogue_backups(
    source_rows: list[dict[str, str]], translations: dict[str, str]
) -> tuple[dict[str, str], list[dict[str, str]]]:
    by_key = {row["key"]: row for row in source_rows}
    propagated: dict[str, str] = {}
    unresolved: list[dict[str, str]] = []
    for row in source_rows:
        key = row["key"]
        if not key.startswith("Dialogue (Backup)/"):
            continue
        primary_key = "Dialogue/" + key.removeprefix("Dialogue (Backup)/")
        primary = by_key.get(primary_key)
        if (
            primary
            and primary.get("english") == row.get("english")
            and primary_key in translations
        ):
            propagated[key] = translations[primary_key]
        else:
            unresolved.append(row)
    return propagated, unresolved
