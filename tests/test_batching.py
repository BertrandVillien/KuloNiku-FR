from argparse import Namespace
import csv

from kuloniku_fr.batching import SOURCE_FIELDS, make_batches, propagate_dialogue_backups
from kuloniku_fr.cli import command_prepare_backups


def row(key: str, english: str) -> dict[str, str]:
    return {
        "key": key,
        "english": english,
        "indonesian": english,
        "spanish": english,
        "thai": english,
        "chinese_simplified": english,
        "chinese_traditional": english,
        "german": english,
        "portuguese": english,
    }


def test_make_batches_excludes_done_empty_and_backup_rows():
    rows = [
        row("INGREDIENT_A", "A"),
        row("Dialogue/HERO_1", "Hello"),
        row("Dialogue (Backup)/HERO_1", "Hello"),
        row("EMPTY", ""),
    ]
    for field in rows[-1]:
        if field != "key":
            rows[-1][field] = ""

    batches = make_batches(rows, {"INGREDIENT_A"}, character_budget=100)

    assert [[item["key"] for item in batch.rows] for batch in batches] == [
        ["Dialogue/HERO_1"]
    ]


def test_propagate_only_exact_english_backup_pairs():
    rows = [
        row("Dialogue/HERO_1", "Hello"),
        row("Dialogue (Backup)/HERO_1", "Hello"),
        row("Dialogue/HERO_2", "New text"),
        row("Dialogue (Backup)/HERO_2", "Old text"),
    ]

    propagated, unresolved = propagate_dialogue_backups(
        rows, {"Dialogue/HERO_1": "Bonjour", "Dialogue/HERO_2": "Nouveau texte"}
    )

    assert propagated == {"Dialogue (Backup)/HERO_1": "Bonjour"}
    assert [item["key"] for item in unresolved] == ["Dialogue (Backup)/HERO_2"]


def test_prepare_backups_writes_exact_copy_and_review_batch(tmp_path):
    rows = [
        row("Dialogue/HERO_1", "Hello"),
        row("Dialogue (Backup)/HERO_1", "Hello"),
        row("Dialogue/HERO_2", "New text"),
        row("Dialogue (Backup)/HERO_2", "Old text"),
    ]
    source = tmp_path / "source.csv"
    with source.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=SOURCE_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    translations = tmp_path / "fr.csv"
    translations.write_text(
        "key,fr,status,notes\nDialogue/HERO_1,Bonjour,reviewed,\n"
        "Dialogue/HERO_2,Nouveau texte,reviewed,\n",
        encoding="utf-8",
    )
    source_dir = tmp_path / "backup-source"
    output_dir = tmp_path / "backup-output"
    manifest = tmp_path / "manifest.json"

    result = command_prepare_backups(
        Namespace(
            source=str(source),
            translations=str(translations),
            source_dir=str(source_dir),
            output_dir=str(output_dir),
            manifest=str(manifest),
            character_budget=80_000,
        )
    )

    assert result == 0
    assert (output_dir / "900-dialogue-backups-identiques.csv").read_text(
        encoding="utf-8"
    ).splitlines()[1].startswith("Dialogue (Backup)/HERO_1,Bonjour,reviewed,")
    assert (source_dir / "901-dialogue-backups-a-reviser.csv").exists()
