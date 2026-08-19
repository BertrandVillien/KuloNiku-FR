from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import UnityPy

from .batching import (
    Batch,
    make_batches,
    propagate_dialogue_backups,
    read_csv_rows,
    row_characters,
    translated_keys,
    write_batches,
)
from .i2_asset import LanguageSource, find_i2_object
from .installation import (
    atomic_copy,
    backup_asset,
    detect_asset,
    latest_backup_for,
    resign_macos,
)
from .translation import apply_french, lint_translation, source_character_limit


CSV_FIELDS = [
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_source(path: Path):
    environment = UnityPy.load(str(path))
    obj = find_i2_object(environment)
    raw = obj.get_raw_data()
    source = LanguageSource.parse(raw)
    if source.serialize() != raw:
        raise RuntimeError("Le contrôle de réécriture I2 à l’identique a échoué.")
    return environment, obj, source


def command_inspect(args) -> int:
    path = Path(args.assets).resolve()
    _, _, source = load_source(path)
    print(f"Fichier : {path}")
    print(f"SHA-256 : {sha256(path)}")
    print(f"Termes : {len(source.terms)}")
    print("Langues : " + ", ".join(f"{x.name} ({x.code})" for x in source.languages))
    return 0


def command_extract(args) -> int:
    path = Path(args.assets).resolve()
    destination = Path(args.output).resolve()
    _, _, source = load_source(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        for term in source.terms:
            row = {"key": term.key}
            for index, field in enumerate(CSV_FIELDS[1:]):
                row[field] = term.translations[index] if index < len(term.translations) else ""
            writer.writerow(row)
    print(f"{len(source.terms)} termes extraits vers {destination}")
    return 0


def command_context(args) -> int:
    path = Path(args.assets).resolve()
    destination = Path(args.output).resolve()
    _, _, source = load_source(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    language_fields = [language.code for language in source.languages]
    fields = ["key", "category", "max_source_chars", *language_fields]
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for term in source.terms:
            category = term.key.split("_", 1)[0] if "_" in term.key else "OTHER"
            row = {
                "key": term.key,
                "category": category,
                "max_source_chars": source_character_limit(term),
            }
            for index, code in enumerate(language_fields):
                row[code] = term.translations[index] if index < len(term.translations) else ""
            writer.writerow(row)
    print(f"Contexte de {len(source.terms)} termes extrait vers {destination}")
    print("Ce fichier contient les textes du jeu : gardez-le dans work/ et ne le publiez pas.")
    return 0


def read_french_csv(path: Path) -> dict[str, str]:
    translations = {}
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not {"key", "fr"}.issubset(reader.fieldnames):
            raise ValueError("Le CSV français doit contenir les colonnes key et fr.")
        for row in reader:
            key = (row.get("key") or "").strip()
            value = row.get("fr") or ""
            if key and value:
                translations[key] = value
    return translations


def command_build(args) -> int:
    source_path = Path(args.assets).resolve()
    csv_path = Path(args.translations).resolve()
    output_path = Path(args.output).resolve()
    if output_path.exists() and not args.force:
        raise FileExistsError(f"La destination existe déjà : {output_path}")

    environment, obj, source = load_source(source_path)
    translations = read_french_csv(csv_path)
    warnings = []
    by_key = {term.key: term for term in source.terms}
    for key, value in translations.items():
        if key in by_key:
            warnings.extend(lint_translation(by_key[key], value))
    slot_language = None if getattr(args, "append_language", False) else args.slot_language
    replaced, fallback_count, unknown_keys = apply_french(
        source, translations, slot_language=slot_language
    )
    source_codes = [language.code for language in source.languages]
    target_code = "fr" if "fr" in source_codes else slot_language
    target_index = [language.code for language in source.languages].index(target_code)
    patched_raw = source.serialize()
    reparsed = LanguageSource.parse(patched_raw)
    reparsed_selection = next(
        term for term in reparsed.terms if term.key == "SETTINGS_LANGUAGESELECTION"
    )
    if reparsed_selection.translations[target_index] != "Français":
        raise RuntimeError("Le contrôle du contenu français a échoué.")

    obj.set_raw_data(patched_raw)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(environment.file.save())

    # Validation indépendante du fichier final.
    _, _, validation = load_source(output_path)
    validation_selection = next(
        term for term in validation.terms if term.key == "SETTINGS_LANGUAGESELECTION"
    )
    if validation_selection.translations[target_index] != "Français":
        raise RuntimeError("Le fichier final ne contient pas la langue française.")

    metadata = {
        "source_sha256": sha256(source_path),
        "patched_sha256": sha256(output_path),
        "terms_total": len(source.terms),
        "terms_translated": replaced,
        "terms_fallback_english": fallback_count,
        "translation_keys_unknown": unknown_keys,
        "mode": f"slot:{slot_language}" if slot_language else "append-experimental",
        "warnings": [warning.__dict__ for warning in warnings],
    }
    metadata_path = output_path.with_suffix(output_path.suffix + ".json")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    print(f"Patch construit : {output_path}")
    print(f"Traductions françaises : {replaced}/{len(source.terms)}")
    print(f"Repli anglais : {fallback_count}")
    if unknown_keys:
        print(f"Clés françaises absentes de cette version : {len(unknown_keys)}")
    if warnings:
        print(f"Avertissements de traduction : {len(warnings)} (voir le JSON)")
    return 0


def command_lint(args) -> int:
    _, _, source = load_source(Path(args.assets).resolve())
    translations = read_french_csv(Path(args.translations).resolve())
    by_key = {term.key: term for term in source.terms}
    warnings = []
    for key, value in translations.items():
        if key in by_key:
            warnings.extend(lint_translation(by_key[key], value))
    unknown = sorted(set(translations) - set(by_key))
    for warning in warnings:
        print(f"{warning.key}: {warning.kind}: {warning.message}")
    for key in unknown:
        print(f"{key}: unknown: clé absente de cette version")
    print(f"{len(translations)} traductions, {len(warnings)} avertissements, {len(unknown)} clés absentes")
    return 1 if args.strict and (warnings or unknown) else 0


def command_install(args) -> int:
    asset = detect_asset(Path(args.game))
    translations_path = Path(args.translations).resolve()
    source_hash = sha256(asset.path)
    _, _, parsed = load_source(asset.path)
    codes = [language.code for language in parsed.languages]
    if "en" not in codes:
        raise RuntimeError("La langue anglaise de repli est absente.")
    if "fr" in codes:
        raise RuntimeError("Cette installation contient l’ancien essai fr ajouté. Restaurez-la avant de repatcher.")
    if "de" in codes:
        selection = next(
            (term for term in parsed.terms if term.key == "SETTINGS_LANGUAGESELECTION"),
            None,
        )
        if selection and selection.translations[codes.index("de")] == "Français":
            raise RuntimeError("Le patch français est déjà installé. Restaurez-le avant de repatcher.")
    translations = read_french_csv(translations_path)
    game_keys = {term.key for term in parsed.terms}
    matched = len(set(translations) & game_keys)
    if matched == 0:
        raise RuntimeError("Aucune clé française ne correspond à cette version du jeu.")
    print(f"Cible : {asset.path}")
    print(f"Édition : {asset.edition}; plateforme : {asset.platform}")
    print(f"SHA-256 actuel : {source_hash}")
    print(f"Clés françaises reconnues : {matched}/{len(translations)}")
    print(f"Nouvelles clés du jeu en repli anglais : {len(game_keys - set(translations))}")
    if not args.apply:
        print("Simulation terminée : aucune modification. Relancez avec --apply pour installer.")
        return 0

    backup_path, manifest_path = backup_asset(asset, sha256)
    try:
        with tempfile.TemporaryDirectory(prefix="kuloniku-fr-") as temporary_dir:
            output = Path(temporary_dir) / "resources.assets"
            build_args = argparse.Namespace(
                assets=str(asset.path), translations=str(translations_path), output=str(output),
                force=False, slot_language="de",
            )
            command_build(build_args)
            atomic_copy(output, asset.path)
        resign_macos(asset.path)
        _, _, validation = load_source(asset.path)
        codes = [language.code for language in validation.languages]
        target_index = codes.index("de")
        selection = next(
            term for term in validation.terms if term.key == "SETTINGS_LANGUAGESELECTION"
        )
        if selection.translations[target_index] != "Français":
            raise RuntimeError("La validation finale de l’emplacement français a échoué.")
    except Exception:
        atomic_copy(backup_path, asset.path)
        resign_macos(asset.path)
        raise
    manifest = json.loads(manifest_path.read_text())
    manifest["patched_sha256"] = sha256(asset.path)
    manifest["translation_keys_matched"] = matched
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"Installation terminée. Sauvegarde : {backup_path}")
    return 0


def command_restore(args) -> int:
    asset = detect_asset(Path(args.game))
    backup_path, manifest = latest_backup_for(asset.path)
    if sha256(backup_path) != manifest["original_sha256"]:
        raise RuntimeError("La sauvegarde ne correspond pas à son manifeste SHA-256.")
    if not args.apply:
        print(f"Restauration disponible : {backup_path}")
        print("Simulation terminée : aucune modification. Relancez avec --apply pour restaurer.")
        return 0
    atomic_copy(backup_path, asset.path)
    resign_macos(asset.path)
    if sha256(asset.path) != manifest["original_sha256"]:
        raise RuntimeError("La vérification finale de restauration a échoué.")
    print(f"Fichier original restauré : {asset.path}")
    return 0


def command_make_batches(args) -> int:
    source_path = Path(args.source).resolve()
    translations_path = Path(args.translations).resolve()
    source_dir = Path(args.source_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    manifest_path = Path(args.manifest).resolve()
    batches = make_batches(
        read_csv_rows(source_path),
        translated_keys(translations_path),
        character_budget=args.character_budget,
    )
    write_batches(batches, source_dir, output_dir, manifest_path)
    print(f"{len(batches)} lots préparés pour {sum(len(batch.rows) for batch in batches)} clés actives")
    print(f"Budget maximal : {args.character_budget} caractères multilingues par lot")
    print(f"Manifeste : {manifest_path}")
    return 0


def command_merge_batches(args) -> int:
    translations_path = Path(args.translations).resolve()
    source_dir = Path(args.source_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    base_rows = read_csv_rows(translations_path)
    by_key = {row["key"]: row for row in base_rows}
    merged_files = 0
    merged_rows = 0
    for output_path in sorted(output_dir.glob("*.csv")):
        source_path = source_dir / output_path.name
        if not source_path.exists():
            raise FileNotFoundError(f"Source de lot absente : {source_path}")
        expected = [row["key"] for row in read_csv_rows(source_path)]
        rows = read_csv_rows(output_path)
        if [row.get("key") for row in rows] != expected:
            raise ValueError(f"Clés ou ordre incorrects dans {output_path}")
        if not rows or not {"key", "fr", "status", "notes"}.issubset(rows[0]):
            raise ValueError(f"Colonnes de traduction invalides dans {output_path}")
        for row in rows:
            if not row.get("fr"):
                raise ValueError(f"Traduction vide pour {row.get('key')} dans {output_path}")
            if row.get("status") not in {"reviewed", "provisional"}:
                raise ValueError(f"Statut invalide pour {row.get('key')} dans {output_path}")
            by_key[row["key"]] = {
                "key": row["key"],
                "fr": row["fr"],
                "status": row["status"],
                "notes": row.get("notes", ""),
            }
            merged_rows += 1
        merged_files += 1

    original_order = [row["key"] for row in read_csv_rows(Path(args.source).resolve())]
    order_index = {key: index for index, key in enumerate(original_order)}
    ordered = sorted(by_key.values(), key=lambda row: order_index.get(row["key"], len(order_index)))
    with translations_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["key", "fr", "status", "notes"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(ordered)
    print(f"{merged_rows} lignes fusionnées depuis {merged_files} lots")
    print(f"Total français : {len(ordered)}")
    return 0


def command_prepare_backups(args) -> int:
    source_path = Path(args.source).resolve()
    translations_path = Path(args.translations).resolve()
    source_dir = Path(args.source_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    manifest_path = Path(args.manifest).resolve()
    source_rows = read_csv_rows(source_path)
    translations = read_french_csv(translations_path)
    propagated, unresolved = propagate_dialogue_backups(source_rows, translations)

    by_key = {row["key"]: row for row in source_rows}
    batches: list[Batch] = []
    exact_rows = [by_key[key] for key in propagated]
    if exact_rows:
        batches.append(
            Batch(
                "900-dialogue-backups-identiques",
                "dialogue-backups-exact",
                exact_rows,
                sum(row_characters(row) for row in exact_rows),
            )
        )

    sequence = 901
    current: list[dict[str, str]] = []
    current_chars = 0
    for row in unresolved:
        if not any(row.get(field, "") for field in CSV_FIELDS[1:]):
            continue
        size = row_characters(row)
        if current and current_chars + size > args.character_budget:
            batches.append(
                Batch(
                    f"{sequence:03d}-dialogue-backups-a-reviser",
                    "dialogue-backups-review",
                    current,
                    current_chars,
                )
            )
            sequence += 1
            current = []
            current_chars = 0
        current.append(row)
        current_chars += size
    if current:
        batches.append(
            Batch(
                f"{sequence:03d}-dialogue-backups-a-reviser",
                "dialogue-backups-review",
                current,
                current_chars,
            )
        )

    write_batches(batches, source_dir, output_dir, manifest_path)
    if exact_rows:
        output_path = output_dir / "900-dialogue-backups-identiques.csv"
        with output_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=["key", "fr", "status", "notes"],
                lineterminator="\n",
            )
            writer.writeheader()
            for key, french in propagated.items():
                writer.writerow(
                    {
                        "key": key,
                        "fr": french,
                        "status": "reviewed",
                        "notes": "Propagé depuis le dialogue principal anglais identique.",
                    }
                )
    print(f"{len(propagated)} dialogues de sauvegarde propagés sans retraduction")
    print(f"{sum(len(batch.rows) for batch in batches[1 if exact_rows else 0:])} lignes à réviser par agents")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kuloniku-fr")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="inspecter resources.assets")
    inspect_parser.add_argument("assets")
    inspect_parser.set_defaults(handler=command_inspect)

    extract_parser = subparsers.add_parser("extract", help="extraire les langues en CSV")
    extract_parser.add_argument("assets")
    extract_parser.add_argument("output")
    extract_parser.set_defaults(handler=command_extract)

    context_parser = subparsers.add_parser("context", help="extraire toutes les langues et métriques de contexte")
    context_parser.add_argument("assets")
    context_parser.add_argument("output")
    context_parser.set_defaults(handler=command_context)

    build_parser = subparsers.add_parser("build", help="construire un resources.assets français")
    build_parser.add_argument("assets")
    build_parser.add_argument("translations")
    build_parser.add_argument("output")
    build_parser.add_argument(
        "--slot-language",
        default="de",
        help="emplacement reconnu par le menu à réutiliser (de par défaut)",
    )
    build_parser.add_argument(
        "--append-language",
        action="store_true",
        help="mode expérimental : ajouter fr, actuellement masqué par le menu du jeu",
    )
    build_parser.add_argument("--force", action="store_true")
    build_parser.set_defaults(handler=command_build)

    lint_parser = subparsers.add_parser("lint", help="contrôler marqueurs et longueurs")
    lint_parser.add_argument("assets")
    lint_parser.add_argument("translations")
    lint_parser.add_argument("--strict", action="store_true")
    lint_parser.set_defaults(handler=command_lint)

    install_parser = subparsers.add_parser("install", help="installer avec sauvegarde automatique")
    install_parser.add_argument("game", help="application, dossier du jeu ou resources.assets")
    install_parser.add_argument("--translations", default="translations/fr.csv")
    install_parser.add_argument("--apply", action="store_true", help="effectuer réellement l’installation")
    install_parser.set_defaults(handler=command_install)

    restore_parser = subparsers.add_parser("restore", help="restaurer la dernière sauvegarde")
    restore_parser.add_argument("game", help="application, dossier du jeu ou resources.assets")
    restore_parser.add_argument("--apply", action="store_true", help="effectuer réellement la restauration")
    restore_parser.set_defaults(handler=command_restore)

    batches_parser = subparsers.add_parser("make-batches", help="préparer des lots compacts pour les agents")
    batches_parser.add_argument("--source", default="work/source.csv")
    batches_parser.add_argument("--translations", default="translations/fr.csv")
    batches_parser.add_argument("--source-dir", default="work/translation-batches/source")
    batches_parser.add_argument("--output-dir", default="translations/batches")
    batches_parser.add_argument("--manifest", default="work/translation-batches/manifest.json")
    batches_parser.add_argument("--character-budget", type=int, default=80_000)
    batches_parser.set_defaults(handler=command_make_batches)

    merge_parser = subparsers.add_parser("merge-batches", help="valider et fusionner les lots terminés")
    merge_parser.add_argument("--source", default="work/source.csv")
    merge_parser.add_argument("--translations", default="translations/fr.csv")
    merge_parser.add_argument("--source-dir", default="work/translation-batches/source")
    merge_parser.add_argument("--output-dir", default="translations/batches")
    merge_parser.set_defaults(handler=command_merge_batches)

    backups_parser = subparsers.add_parser(
        "prepare-backups",
        help="propager les dialogues de sauvegarde identiques et préparer les exceptions",
    )
    backups_parser.add_argument("--source", default="work/source.csv")
    backups_parser.add_argument("--translations", default="translations/fr.csv")
    backups_parser.add_argument("--source-dir", default="work/translation-backups/source")
    backups_parser.add_argument("--output-dir", default="translations/backup-batches")
    backups_parser.add_argument("--manifest", default="work/translation-backups/manifest.json")
    backups_parser.add_argument("--character-budget", type=int, default=80_000)
    backups_parser.set_defaults(handler=command_prepare_backups)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except Exception as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
