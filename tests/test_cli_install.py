from argparse import Namespace
import json
from pathlib import Path

from kuloniku_fr import cli
from kuloniku_fr.installation import GameAsset


class Language:
    def __init__(self, code: str):
        self.code = code


class Term:
    def __init__(self, key: str, translations: list[str]):
        self.key = key
        self.translations = translations


class Source:
    def __init__(self, french: bool):
        self.languages = [Language("en"), Language("id"), Language("de")]
        self.terms = [
            Term(
                "SETTINGS_LANGUAGESELECTION",
                ["English", "Indonesia", "Français" if french else "Deutsch"],
            )
        ]


def test_install_updates_directly_from_verified_original(monkeypatch, tmp_path: Path):
    asset_path = tmp_path / "KuloNiku_Data" / "resources.assets"
    asset_path.parent.mkdir()
    asset_path.write_bytes(b"patched-old")

    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()
    backup_path = backup_dir / "resources.assets"
    backup_path.write_bytes(b"original")
    manifest_path = backup_dir / "manifest.json"
    manifest = {
        "original_sha256": cli.sha256(backup_path),
        "patched_sha256": cli.sha256(asset_path),
    }
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    monkeypatch.setattr(
        cli,
        "detect_asset",
        lambda game: GameAsset(asset_path, "windows", "full"),
    )
    monkeypatch.setattr(cli, "latest_backup_for", lambda target: (backup_path, manifest))
    monkeypatch.setattr(
        cli,
        "load_source",
        lambda path: (None, None, Source(french=Path(path).read_bytes() != b"original")),
    )
    monkeypatch.setattr(
        cli,
        "load_resolved_french",
        lambda *args, **kwargs: ({"SETTINGS_LANGUAGESELECTION": "Français"}, 0, 0),
    )

    def fake_build(args):
        Path(args.output).write_bytes(b"patched-new")
        return 0

    monkeypatch.setattr(cli, "command_build", fake_build)
    monkeypatch.setattr(cli, "resign_macos", lambda path: None)
    monkeypatch.setattr(cli, "translation_bundle_hash", lambda *args, **kwargs: "bundle")

    result = cli.command_install(
        Namespace(
            game=str(tmp_path),
            translations=str(tmp_path / "fr.csv"),
            source_hashes=None,
            compatibility_overrides=None,
            apply=True,
        )
    )

    assert result == 0
    assert asset_path.read_bytes() == b"patched-new"
    assert backup_path.read_bytes() == b"original"
    updated_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert updated_manifest["original_sha256"] == cli.sha256(backup_path)
    assert updated_manifest["patched_sha256"] == cli.sha256(asset_path)
    assert updated_manifest["translation_bundle_sha256"] == "bundle"


def test_status_reports_current_translation_and_backup(monkeypatch, tmp_path: Path):
    asset_path = tmp_path / "KuloNiku_Data" / "resources.assets"
    asset_path.parent.mkdir()
    asset_path.write_bytes(b"patched")
    translations = tmp_path / "fr.csv"
    translations.write_text("key,fr\n", encoding="utf-8")
    manifest = {
        "patched_sha256": cli.sha256(asset_path),
        "translation_bundle_sha256": "bundle-current",
        "patcher_version": "0.1.0",
    }

    monkeypatch.setattr(
        cli,
        "detect_asset",
        lambda game: GameAsset(asset_path, "windows", "full"),
    )
    monkeypatch.setattr(cli, "load_source", lambda path: (None, None, Source(french=True)))
    monkeypatch.setattr(
        cli,
        "latest_backup_for",
        lambda target: (tmp_path / "backup" / "resources.assets", manifest),
    )
    monkeypatch.setattr(
        cli,
        "translation_bundle_hash",
        lambda *args, **kwargs: "bundle-current",
    )

    report = cli.status_report(
        Namespace(
            game=str(tmp_path),
            translations=str(translations),
            source_hashes=None,
            compatibility_overrides=None,
        )
    )

    assert report["state"] == "patched"
    assert report["translation_state"] == "current"
    assert report["backup_available"] is True
    assert report["schema_version"] == 1
    assert report["source_recognition"] == "unavailable"


def test_source_recognition_marks_unlisted_game_without_blocking(tmp_path: Path):
    translations = tmp_path / "fr.csv"
    translations.write_text("key,fr\n", encoding="utf-8")
    (tmp_path / "known-sources.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "editions": {
                    "full": [
                        {
                            "game_version": "older",
                            "source_profile_sha256": "not-the-current-profile",
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )

    assert cli.source_recognition(Source(french=False), translations, "full") == "unknown"


def test_status_detects_a_real_steam_replacement_from_the_asset_hash(monkeypatch, tmp_path: Path):
    asset_path = tmp_path / "KuloNiku_Data" / "resources.assets"
    asset_path.parent.mkdir()
    asset_path.write_bytes(b"new-steam-version")
    translations = tmp_path / "fr.csv"
    translations.write_text("key,fr\n", encoding="utf-8")
    manifest = {
        "original_sha256": "old-original",
        "patched_sha256": "old-patched",
        "translation_bundle_sha256": "bundle-current",
    }

    monkeypatch.setattr(
        cli,
        "detect_asset",
        lambda game: GameAsset(asset_path, "windows", "full"),
    )
    monkeypatch.setattr(cli, "load_source", lambda path: (None, None, Source(french=False)))
    monkeypatch.setattr(
        cli,
        "latest_backup_for",
        lambda target: (tmp_path / "backup" / "resources.assets", manifest),
    )
    monkeypatch.setattr(cli, "translation_bundle_hash", lambda *args, **kwargs: "bundle-current")

    report = cli.status_report(
        Namespace(
            game=str(tmp_path),
            translations=str(translations),
            source_hashes=None,
            compatibility_overrides=None,
        )
    )

    assert report["state"] == "game_updated"
    assert report["translation_state"] == "not_installed"
