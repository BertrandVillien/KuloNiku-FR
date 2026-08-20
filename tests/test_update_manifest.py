import importlib.util
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from kuloniku_fr import TRANSLATION_PACKAGE_MINIMUM_PATCHER_VERSION
from kuloniku_fr.cli import translation_bundle_hash


def test_translation_bundle_hash_is_identical_with_windows_line_endings(tmp_path: Path):
    unix = tmp_path / "unix"
    windows = tmp_path / "windows"
    unix.mkdir()
    windows.mkdir()
    for name, content in {
        "fr.csv": b"key,fr\nHELLO,Bonjour\n",
        "source-hashes.csv": b"key,source_hash\nHELLO,hash\n",
    }.items():
        (unix / name).write_bytes(content)
        (windows / name).write_bytes(content.replace(b"\n", b"\r\n"))

    assert translation_bundle_hash(
        unix / "fr.csv", edition="full"
    ) == translation_bundle_hash(windows / "fr.csv", edition="full")


def test_translation_release_is_standalone_and_declares_its_required_engine(
    monkeypatch, tmp_path: Path
):
    translations = tmp_path / "translations"
    translations.mkdir()
    (translations / "fr.csv").write_text("key,fr\nHELLO,Bonjour\n", encoding="utf-8")
    (translations / "source-hashes.csv").write_text(
        "key,source_hash\nHELLO,hash\n", encoding="utf-8"
    )
    (translations / "demo-overrides.csv").write_text(
        "key,source_hash,fr\n", encoding="utf-8"
    )
    (translations / "known-sources.json").write_text(
        '{"schema_version": 1, "editions": {}}\n', encoding="utf-8"
    )
    (translations / "NOTICE.md").write_text("Notice\n", encoding="utf-8")

    script = Path(__file__).parents[1] / "packaging" / "create_update_manifest.py"
    spec = importlib.util.spec_from_file_location("create_update_manifest", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.__version__ = "1.0.0"
    monkeypatch.chdir(tmp_path)
    module.main()

    manifest = json.loads((tmp_path / "package" / "update-manifest.json").read_text())
    package = manifest["translation_package"]
    assert manifest["schema"] == 2
    assert manifest["version"] == "1.0.0"
    assert package["minimum_patcher_version"] == TRANSLATION_PACKAGE_MINIMUM_PATCHER_VERSION
    assert package["minimum_patcher_version"] != manifest["version"]
    assert package["bundles"] == manifest["translation_bundles"]
    archive_path = tmp_path / "package" / package["asset"]
    assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == package["sha256"]
    first_archive = archive_path.read_bytes()
    module.main()
    assert archive_path.read_bytes() == first_archive
    with ZipFile(archive_path) as archive:
        assert set(archive.namelist()) == {
            "fr.csv",
            "source-hashes.csv",
            "demo-overrides.csv",
            "known-sources.json",
            "NOTICE.md",
        }
