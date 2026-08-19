from kuloniku_fr.batching import make_batches, propagate_dialogue_backups


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
