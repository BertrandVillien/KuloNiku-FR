import hashlib
from pathlib import Path
from zipfile import ZipFile

from kuloniku_fr.windows_launcher import (
    LauncherPaths,
    available_update_kind,
    available_updates,
    decode_engine_output,
    engine_environment,
    extract_translation_package,
    installed_game_candidates,
    latest_release_from_payload,
    parse_steam_library_paths,
    version_tuple,
)


def test_engine_environment_forces_utf8_for_redirected_windows_output():
    environment = engine_environment()

    assert environment["PYTHONUTF8"] == "1"
    assert environment["PYTHONIOENCODING"] == "utf-8"


def test_decode_engine_output_supports_utf8_and_windows_console_encoding():
    assert decode_engine_output("Édition : complète".encode("utf-8")) == "Édition : complète"
    assert decode_engine_output("Édition : complète".encode("cp1252")) == "Édition : complète"


def test_update_manifest_distinguishes_engine_and_translation_updates():
    manifest = {
        "version": "0.2.0",
        "translation_bundles": {"full": "remote"},
    }
    assert version_tuple("v0.2.0-beta.1") == (0, 2, 0, 1, 1)
    assert available_update_kind(
        manifest,
        edition="full",
        bundled_translation_hash="local",
        current_version="0.1.0",
    ) == "engine"

    manifest["version"] = "0.1.0"
    assert available_update_kind(
        manifest,
        edition="full",
        bundled_translation_hash="local",
        current_version="0.1.0",
    ) == "translations"

    manifest["translation_bundles"]["full"] = "local"
    assert available_update_kind(
        manifest,
        edition="full",
        bundled_translation_hash="local",
        current_version="0.1.0",
    ) is None


def test_prerelease_versions_are_compared_in_publication_order():
    assert version_tuple("0.3.0-beta.2") > version_tuple("0.3.0-beta.1")
    assert version_tuple("0.3.0-rc.1") > version_tuple("0.3.0-beta.9")
    assert version_tuple("0.3.0") > version_tuple("0.3.0-rc.9")
    assert version_tuple("0.3.0b1") == version_tuple("0.3.0-beta.1")


def test_installer_and_translation_updates_are_independent():
    manifest = {
        "version": "0.3.0",
        "translation_bundles": {"full": "remote"},
        "translation_package": {
            "minimum_patcher_version": "0.2.0",
            "bundles": {"full": "remote"},
        },
    }
    assert available_updates(
        manifest,
        edition="full",
        bundled_translation_hash="local",
        current_version="0.2.0",
    ) == (True, "download")

    manifest["translation_package"]["minimum_patcher_version"] = "0.3.0"
    assert available_updates(
        manifest,
        edition="full",
        bundled_translation_hash="local",
        current_version="0.2.0",
    ) == (True, "installer_required")


def test_translation_package_is_verified_and_extracted_safely(tmp_path: Path):
    archive = tmp_path / "translations.zip"
    contents = {
        "fr.csv": b"key,fr\nHELLO,Bonjour\n",
        "source-hashes.csv": b"key,source_hash\nHELLO,hash\n",
        "demo-overrides.csv": b"key,source_hash,fr\n",
        "known-sources.json": b"{}\n",
        "NOTICE.md": b"Notice\n",
    }
    with ZipFile(archive, "w") as bundle:
        for name, data in contents.items():
            bundle.writestr(name, data)
    expected_hash = hashlib.sha256(archive.read_bytes()).hexdigest()

    french = extract_translation_package(archive, tmp_path / "cache", expected_hash)

    assert french.read_bytes() == contents["fr.csv"]
    assert {path.name for path in french.parent.iterdir()} == set(contents)


def test_latest_release_endpoint_payload_is_a_release_list():
    release = {
        "html_url": "https://github.com/example/project/releases/tag/v0.2.0",
        "assets": [{"name": "update-manifest.json"}],
    }

    assert latest_release_from_payload([release]) == release
    assert latest_release_from_payload([]) is None
    assert latest_release_from_payload(release) is None


def make_game(folder: Path) -> Path:
    assets = folder / f"{folder.name}_Data" / "resources.assets"
    assets.parent.mkdir(parents=True)
    assets.write_bytes(b"not-a-real-game-file")
    return folder


def test_parse_steam_library_paths_supports_escaped_windows_paths():
    text = r'''
    "libraryfolders"
    {
        "0" { "path" "C:\\Program Files (x86)\\Steam" }
        "1" { "path" "D:\\Jeux\\SteamLibrary" }
    }
    '''

    assert parse_steam_library_paths(text) == [
        Path(r"C:\Program Files (x86)\Steam"),
        Path(r"D:\Jeux\SteamLibrary"),
    ]


def test_installed_game_candidates_prefers_full_game_and_uses_manifest(tmp_path: Path):
    steamapps = tmp_path / "steamapps"
    common = steamapps / "common"
    full = make_game(common / "Bowl Up")
    demo = make_game(common / "KuloNiku Demo")
    (steamapps / "appmanifest_3357960.acf").write_text(
        '"AppState" { "installdir" "Bowl Up" }', encoding="utf-8"
    )

    assert installed_game_candidates([tmp_path]) == [full.resolve(), demo.resolve()]


def test_launcher_paths_requires_engine_and_translations(tmp_path: Path):
    paths = LauncherPaths(tmp_path)
    assert len(paths.validate()) == 2

    paths.resources.mkdir()
    paths.engine.write_bytes(b"exe")
    paths.translations.parent.mkdir()
    paths.translations.write_text("key,fr\n", encoding="utf-8")
    assert paths.validate() == []
