from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile

import UnityPy

from . import __version__
from .batching import (
    Batch,
    make_batches,
    make_update_batches,
    propagate_dialogue_backups,
    read_csv_rows,
    row_characters,
    translated_keys,
    write_batches,
    write_update_batches,
)
from .i2_asset import LanguageSource, find_i2_object
from .installation import (
    atomic_copy,
    backup_asset,
    detect_asset,
    installation_state,
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
    # UnityPy keeps path-backed files open on Windows. Loading the bytes avoids
    # a sharing violation when the freshly validated patch is copied atomically.
    environment = UnityPy.load(path.read_bytes())
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


def reference_hash(english: str, indonesian: str) -> str:
    """Fingerprint the two reference languages without publishing their text."""
    digest = hashlib.sha256()
    digest.update(english.encode("utf-8"))
    digest.update(b"\0")
    digest.update(indonesian.encode("utf-8"))
    return digest.hexdigest()


def source_profile_hash(source: LanguageSource) -> str:
    """Fingerprint a complete localization source without publishing its text."""
    digest = hashlib.sha256()
    for term in sorted(source.terms, key=lambda item: item.key):
        english = term.translations[0] if term.translations else ""
        indonesian = term.translations[1] if len(term.translations) > 1 else ""
        digest.update(term.key.encode("utf-8"))
        digest.update(b"\0")
        digest.update(reference_hash(english, indonesian).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def source_recognition(source: LanguageSource, translations_path: Path, edition: str) -> str:
    """Return known/unknown for the game text set; unknown never blocks patching."""
    profiles_path = translations_path.with_name("known-sources.json")
    if not profiles_path.exists():
        return "unavailable"
    try:
        profiles = json.loads(profiles_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "unavailable"
    known = profiles.get("editions", {}).get(edition, [])
    hashes = {
        item.get("source_profile_sha256")
        for item in known
        if isinstance(item, dict)
    }
    return "known" if source_profile_hash(source) in hashes else "unknown"


def read_source_hashes(path: Path) -> dict[str, str]:
    hashes = {}
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not {"key", "source_hash"}.issubset(reader.fieldnames):
            raise ValueError("Le profil source doit contenir les colonnes key et source_hash.")
        for row in reader:
            key = (row.get("key") or "").strip()
            value = (row.get("source_hash") or "").strip()
            if key and value:
                hashes[key] = value
    return hashes


def read_compatibility_overrides(path: Path) -> dict[tuple[str, str], str]:
    overrides = {}
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        required = {"key", "source_hash", "fr"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "Les exceptions de compatibilité doivent contenir key, source_hash et fr."
            )
        for row in reader:
            key = (row.get("key") or "").strip()
            source_hash = (row.get("source_hash") or "").strip()
            value = row.get("fr") or ""
            if key and source_hash and value:
                overrides[(key, source_hash)] = value
    return overrides


def resolve_french_for_source(
    source: LanguageSource,
    translations: dict[str, str],
    source_hashes: dict[str, str] | None = None,
    compatibility_overrides: dict[tuple[str, str], str] | None = None,
) -> tuple[dict[str, str], int, int]:
    """Select only translations proven compatible with the installed strings.

    A changed English/Indonesian reference falls back to the installed English
    instead of silently receiving a translation written for another meaning.
    """
    actual_hashes = {
        term.key: reference_hash(
            term.translations[0] if term.translations else "",
            term.translations[1] if len(term.translations) > 1 else "",
        )
        for term in source.terms
    }
    if source_hashes is None:
        resolved = dict(translations)
        rejected = 0
    else:
        resolved = {
            key: value
            for key, value in translations.items()
            if source_hashes.get(key) == actual_hashes.get(key)
        }
        rejected = len(set(translations) & set(actual_hashes)) - len(resolved)

    applied_overrides = 0
    for (key, expected_hash), value in (compatibility_overrides or {}).items():
        if actual_hashes.get(key) == expected_hash:
            resolved[key] = value
            applied_overrides += 1
    return resolved, rejected, applied_overrides


def translation_profile_paths(
    translations_path: Path,
    *,
    edition: str,
    source_hashes: str | None = None,
    compatibility_overrides: str | None = None,
) -> tuple[Path | None, Path | None]:
    hashes_path = (
        Path(source_hashes).resolve()
        if source_hashes
        else translations_path.with_name("source-hashes.csv")
    )
    if not hashes_path.exists():
        if source_hashes:
            raise FileNotFoundError(f"Profil source absent : {hashes_path}")
        hashes_path = None
    overrides_path = None
    if edition == "demo":
        overrides_path = (
            Path(compatibility_overrides).resolve()
            if compatibility_overrides
            else translations_path.with_name("demo-overrides.csv")
        )
        if not overrides_path.exists():
            if compatibility_overrides:
                raise FileNotFoundError(
                    f"Exceptions de compatibilité absentes : {overrides_path}"
                )
            overrides_path = None
    return hashes_path, overrides_path


def load_resolved_french(
    source: LanguageSource,
    translations_path: Path,
    *,
    edition: str,
    source_hashes: str | None = None,
    compatibility_overrides: str | None = None,
) -> tuple[dict[str, str], int, int]:
    hashes_path, overrides_path = translation_profile_paths(
        translations_path,
        edition=edition,
        source_hashes=source_hashes,
        compatibility_overrides=compatibility_overrides,
    )
    hashes = read_source_hashes(hashes_path) if hashes_path else None
    overrides = read_compatibility_overrides(overrides_path) if overrides_path else None
    return resolve_french_for_source(
        source,
        read_french_csv(translations_path),
        hashes,
        overrides,
    )


def translation_bundle_hash(
    translations_path: Path,
    *,
    edition: str,
    source_hashes: str | None = None,
    compatibility_overrides: str | None = None,
) -> str:
    hashes_path, overrides_path = translation_profile_paths(
        translations_path,
        edition=edition,
        source_hashes=source_hashes,
        compatibility_overrides=compatibility_overrides,
    )
    digest = hashlib.sha256()
    for path in (translations_path, hashes_path, overrides_path):
        if path is None:
            continue
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def command_build(args) -> int:
    source_path = Path(args.assets).resolve()
    csv_path = Path(args.translations).resolve()
    output_path = Path(args.output).resolve()
    if output_path.exists() and not args.force:
        raise FileExistsError(f"La destination existe déjà : {output_path}")

    environment, obj, source = load_source(source_path)
    edition = getattr(args, "edition", None) or (
        "demo" if "demo" in str(source_path).lower() else "full"
    )
    translations, rejected, applied_overrides = load_resolved_french(
        source,
        csv_path,
        edition=edition,
        source_hashes=getattr(args, "source_hashes", None),
        compatibility_overrides=getattr(args, "compatibility_overrides", None),
    )
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
        "translation_keys_rejected_source_change": rejected,
        "compatibility_overrides_applied": applied_overrides,
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
    if rejected:
        print(f"Traductions écartées après changement de source : {rejected}")
    if applied_overrides:
        print(f"Exceptions de compatibilité appliquées : {applied_overrides}")
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
    current_hash = sha256(asset.path)
    _, _, installed_source = load_source(asset.path)
    codes = [language.code for language in installed_source.languages]
    if "en" not in codes:
        raise RuntimeError("La langue anglaise de repli est absente.")
    selection = next(
        (
            term
            for term in installed_source.terms
            if term.key == "SETTINGS_LANGUAGESELECTION"
        ),
        None,
    )
    french_in_reused_slot = bool(
        selection
        and "de" in codes
        and selection.translations[codes.index("de")] == "Français"
    )
    french_appended = "fr" in codes
    updating = french_in_reused_slot or french_appended
    source_path = asset.path
    backup_path = None
    manifest_path = None
    manifest = None

    if updating:
        try:
            backup_path, manifest = latest_backup_for(asset.path)
        except FileNotFoundError as error:
            raise RuntimeError(
                "Le français est présent, mais sa sauvegarde originale est introuvable. "
                "Mise à jour refusée pour protéger le jeu."
            ) from error
        manifest_path = backup_path.parent / "manifest.json"
        if manifest.get("patched_sha256") != current_hash:
            raise RuntimeError(
                "Le jeu patché diffère du dernier état vérifié. "
                "Mise à jour automatique refusée pour protéger les fichiers."
            )
        if sha256(backup_path) != manifest.get("original_sha256"):
            raise RuntimeError("La sauvegarde originale ne correspond plus à son manifeste SHA-256.")
        source_path = backup_path

    source_hash = sha256(source_path)
    _, _, parsed = load_source(source_path)
    translations, rejected, applied_overrides = load_resolved_french(
        parsed,
        translations_path,
        edition=asset.edition,
        source_hashes=getattr(args, "source_hashes", None),
        compatibility_overrides=getattr(args, "compatibility_overrides", None),
    )
    game_keys = {term.key for term in parsed.terms}
    matched = len(set(translations) & game_keys)
    if matched == 0:
        raise RuntimeError("Aucune clé française ne correspond à cette version du jeu.")
    print(f"Cible : {asset.path}")
    print(f"Édition : {asset.edition}; plateforme : {asset.platform}")
    print(f"Mode : {'mise à jour directe' if updating else 'première installation'}")
    print(f"SHA-256 source : {source_hash}")
    print(f"Clés françaises reconnues : {matched}/{len(translations)}")
    print(f"Nouvelles clés du jeu en repli anglais : {len(game_keys - set(translations))}")
    if rejected:
        print(f"Traductions écartées après changement de source : {rejected}")
    if applied_overrides:
        print(f"Exceptions de compatibilité {asset.edition} : {applied_overrides}")
    if not args.apply:
        print("Simulation terminée : aucune modification. Relancez avec --apply pour installer.")
        return 0

    if not updating:
        backup_path, manifest_path = backup_asset(asset, sha256)
        manifest = json.loads(manifest_path.read_text())
    assert backup_path is not None
    assert manifest_path is not None
    assert manifest is not None

    try:
        with tempfile.TemporaryDirectory(prefix="kuloniku-fr-") as temporary_dir:
            temporary = Path(temporary_dir)
            output = temporary / "resources.assets"
            rollback = temporary / "resources.assets.before-update"
            shutil.copy2(asset.path, rollback)
            build_args = argparse.Namespace(
                assets=str(source_path), translations=str(translations_path), output=str(output),
                force=False, slot_language="de", edition=asset.edition,
                source_hashes=getattr(args, "source_hashes", None),
                compatibility_overrides=getattr(args, "compatibility_overrides", None),
            )
            command_build(build_args)
            try:
                atomic_copy(output, asset.path)
                resign_macos(asset.path)
                _, _, validation = load_source(asset.path)
                codes = [language.code for language in validation.languages]
                target_index = codes.index("de")
                selection = next(
                    term
                    for term in validation.terms
                    if term.key == "SETTINGS_LANGUAGESELECTION"
                )
                if selection.translations[target_index] != "Français":
                    raise RuntimeError("La validation finale de l’emplacement français a échoué.")
            except Exception:
                atomic_copy(rollback, asset.path)
                resign_macos(asset.path)
                raise
    except Exception:
        raise
    manifest["patched_sha256"] = sha256(asset.path)
    manifest["translation_keys_matched"] = matched
    manifest["patcher_version"] = __version__
    manifest["translation_bundle_sha256"] = translation_bundle_hash(
        translations_path,
        edition=asset.edition,
        source_hashes=getattr(args, "source_hashes", None),
        compatibility_overrides=getattr(args, "compatibility_overrides", None),
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    if updating:
        print(f"Mise à jour terminée. Sauvegarde originale conservée : {backup_path}")
    else:
        print(f"Installation terminée. Sauvegarde : {backup_path}")
    return 0


def status_report(args) -> dict[str, object]:
    """Build a machine-readable installation and translation status report."""
    asset = detect_asset(Path(args.game))
    translations_path = Path(args.translations).resolve()
    current_hash = sha256(asset.path)
    _, _, source = load_source(asset.path)
    recognition = source_recognition(source, translations_path, asset.edition)
    codes = [language.code for language in source.languages]
    selection = next(
        (term for term in source.terms if term.key == "SETTINGS_LANGUAGESELECTION"),
        None,
    )
    french_active = bool(
        selection
        and "de" in codes
        and selection.translations[codes.index("de")] == "Français"
    )
    manifest = None
    try:
        _, manifest = latest_backup_for(asset.path)
    except FileNotFoundError:
        pass
    state = installation_state(current_hash, french_active, manifest)
    bundle_hash = translation_bundle_hash(
        translations_path,
        edition=asset.edition,
        source_hashes=getattr(args, "source_hashes", None),
        compatibility_overrides=getattr(args, "compatibility_overrides", None),
    )
    installed_bundle = manifest.get("translation_bundle_sha256") if manifest else None
    if state == "patched" and installed_bundle == bundle_hash:
        translation_state = "current"
    elif state == "patched" and installed_bundle:
        translation_state = "update_available"
    elif state == "patched":
        # Legacy manifests created before translation bundle hashes existed can
        # still be identified exactly. Rebuild into a temporary file from the
        # verified original backup, then compare without touching the game.
        translation_state = "unknown"
        if manifest:
            try:
                backup_path, _ = latest_backup_for(asset.path)
                if sha256(backup_path) == manifest.get("original_sha256"):
                    with tempfile.TemporaryDirectory(prefix="kuloniku-fr-status-") as temporary_dir:
                        expected = Path(temporary_dir) / "resources.assets"
                        build_args = argparse.Namespace(
                            assets=str(backup_path),
                            translations=str(translations_path),
                            output=str(expected),
                            force=False,
                            slot_language="de",
                            edition=asset.edition,
                            source_hashes=getattr(args, "source_hashes", None),
                            compatibility_overrides=getattr(args, "compatibility_overrides", None),
                        )
                        with contextlib.redirect_stdout(io.StringIO()):
                            command_build(build_args)
                        translation_state = (
                            "current" if sha256(expected) == current_hash else "update_available"
                        )
            except Exception:
                translation_state = "unknown"
    else:
        translation_state = "not_installed"

    return {
        "schema_version": 1,
        "state": state,
        "translation_state": translation_state,
        "backup_available": manifest is not None,
        "edition": asset.edition,
        "platform": asset.platform,
        "source_recognition": recognition,
        "current_sha256": current_hash,
        "installed_bundle_sha256": installed_bundle,
        "available_bundle_sha256": bundle_hash,
        "installed_patcher_version": manifest.get("patcher_version") if manifest else None,
        "current_patcher_version": __version__,
    }


def command_status(args) -> int:
    """Report whether Steam or the local translation changed since patching."""
    report = status_report(args)
    if getattr(args, "json", False):
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0

    labels = {
        "patched": "patch français installé et fichier inchangé",
        "patched_unknown": "français présent, mais état différent du dernier manifeste",
        "restored": "fichier original restauré ; installation du patch disponible",
        "game_updated": "jeu modifié ou mis à jour par Steam ; nouveau patch nécessaire",
        "unpatched": "aucun patch KuloNiku FR reconnu",
    }
    print(f"État : {labels[str(report['state'])]}")
    print(f"Édition : {report['edition']}; plateforme : {report['platform']}")
    if report["source_recognition"] == "unknown":
        print(
            "Version du jeu non encore répertoriée : le patch reste installable ; "
            "les textes nouveaux resteront en anglais jusqu'à leur traduction."
        )
    print(f"SHA-256 actuel : {report['current_sha256']}")

    if report["translation_state"] == "update_available":
        print("Traductions embarquées plus récentes : mise à jour directe disponible.")
    elif report["translation_state"] == "current":
        print("Traductions locales : à jour.")
    elif report["translation_state"] == "unknown":
        print("Version de traduction installée inconnue (ancien manifeste).")
    installed_version = report["installed_patcher_version"]
    if installed_version:
        print(f"Moteur ayant installé le patch : {installed_version}")
    print(f"Moteur actuellement lancé : {__version__}")
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


def command_prepare_update_batches(args) -> int:
    """Prepare only the strings affected by a game-version update."""
    previous_source_path = Path(args.previous_source).resolve()
    source_path = Path(args.source).resolve()
    translations_path = Path(args.translations).resolve()
    source_dir = Path(args.source_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    manifest_path = Path(args.manifest).resolve()
    batches = make_update_batches(
        read_csv_rows(previous_source_path),
        read_csv_rows(source_path),
        read_french_csv(translations_path),
        character_budget=args.character_budget,
    )
    write_update_batches(batches, source_dir, output_dir, manifest_path)
    reviewed_rows = sum(len(batch.rows) for batch in batches)
    print(f"{len(batches)} lots de mise à jour préparés pour {reviewed_rows} clés actives")
    print("Inclus : nouvelles clés sans français et changements anglais/indonésien")
    print(f"Budget maximal : {args.character_budget} caractères de contexte par lot")
    print(f"Manifeste : {manifest_path}")
    return 0


def command_source_hashes(args) -> int:
    """Write the source fingerprints that prevent stale translations."""
    source_rows = read_csv_rows(Path(args.source).resolve())
    translations = read_french_csv(Path(args.translations).resolve())
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=["key", "source_hash"], lineterminator="\n"
        )
        writer.writeheader()
        for row in source_rows:
            if row["key"] not in translations:
                continue
            writer.writerow(
                {
                    "key": row["key"],
                    "source_hash": reference_hash(
                        row.get("english", ""), row.get("indonesian", "")
                    ),
                }
            )
            written += 1
    print(f"{written} empreintes source écrites dans {output}")
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

    overrides_path = Path(args.overrides).resolve()
    override_rows = 0
    if overrides_path.exists():
        for row in read_csv_rows(overrides_path):
            key = row.get("key", "")
            if key not in by_key:
                raise ValueError(f"Clé de correction inconnue : {key}")
            if not row.get("fr") or row.get("status") not in {"reviewed", "provisional"}:
                raise ValueError(f"Correction invalide pour {key}")
            by_key[key] = {
                "key": key,
                "fr": row["fr"],
                "status": row["status"],
                "notes": row.get("notes", ""),
            }
            override_rows += 1

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
    if override_rows:
        print(f"{override_rows} corrections de relecture appliquées")
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
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for item in manifest:
            if item["id"] == "900-dialogue-backups-identiques":
                item["status"] = "done"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"{len(propagated)} dialogues de sauvegarde propagés sans retraduction")
    print(f"{sum(len(batch.rows) for batch in batches[1 if exact_rows else 0:])} lignes à réviser par agents")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kuloniku-fr")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
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
    build_parser.add_argument("--edition", choices=("full", "demo"))
    build_parser.add_argument(
        "--source-hashes",
        help="profil de compatibilité source (source-hashes.csv voisin par défaut)",
    )
    build_parser.add_argument(
        "--compatibility-overrides",
        help="exceptions d'édition (demo-overrides.csv voisin pour la démo)",
    )
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
    install_parser.add_argument(
        "--source-hashes",
        help="profil de compatibilité source (source-hashes.csv voisin par défaut)",
    )
    install_parser.add_argument(
        "--compatibility-overrides",
        help="exceptions d'édition (demo-overrides.csv voisin pour la démo)",
    )
    install_parser.add_argument("--apply", action="store_true", help="effectuer réellement l’installation")
    install_parser.set_defaults(handler=command_install)

    status_parser = subparsers.add_parser(
        "status", help="détecter une mise à jour du jeu ou des traductions"
    )
    status_parser.add_argument("game", help="application, dossier du jeu ou resources.assets")
    status_parser.add_argument("--translations", default="translations/fr.csv")
    status_parser.add_argument("--source-hashes")
    status_parser.add_argument("--compatibility-overrides")
    status_parser.add_argument("--json", action="store_true", help="sortie structurée pour les interfaces")
    status_parser.set_defaults(handler=command_status)

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

    update_batches_parser = subparsers.add_parser(
        "prepare-update-batches",
        help="préparer les nouvelles clés et les changements anglais/indonésien d'une version",
    )
    update_batches_parser.add_argument(
        "--previous-source",
        default="work/source.csv",
        help="CSV extrait de la version précédemment traduite",
    )
    update_batches_parser.add_argument(
        "--source",
        default="work/full/source.csv",
        help="CSV extrait de la nouvelle version du jeu",
    )
    update_batches_parser.add_argument("--translations", default="translations/fr.csv")
    update_batches_parser.add_argument("--source-dir", default="work/update-batches/source")
    update_batches_parser.add_argument("--output-dir", default="translations/update-batches")
    update_batches_parser.add_argument("--manifest", default="work/update-batches/manifest.json")
    update_batches_parser.add_argument("--character-budget", type=int, default=80_000)
    update_batches_parser.set_defaults(handler=command_prepare_update_batches)

    hashes_parser = subparsers.add_parser(
        "source-hashes",
        help="générer les empreintes anglais/indonésien des traductions validées",
    )
    hashes_parser.add_argument("--source", default="work/source.csv")
    hashes_parser.add_argument("--translations", default="translations/fr.csv")
    hashes_parser.add_argument("--output", default="translations/source-hashes.csv")
    hashes_parser.set_defaults(handler=command_source_hashes)

    merge_parser = subparsers.add_parser("merge-batches", help="valider et fusionner les lots terminés")
    merge_parser.add_argument("--source", default="work/source.csv")
    merge_parser.add_argument("--translations", default="translations/fr.csv")
    merge_parser.add_argument("--source-dir", default="work/translation-batches/source")
    merge_parser.add_argument("--output-dir", default="translations/batches")
    merge_parser.add_argument("--overrides", default="translations/review-overrides.csv")
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
