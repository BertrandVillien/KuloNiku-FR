from pathlib import Path

from kuloniku_fr.windows_launcher import (
    LauncherPaths,
    available_update_kind,
    decode_engine_output,
    engine_environment,
    installed_game_candidates,
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
    assert version_tuple("v0.2.0-beta.1") == (0, 2, 0)
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

    paths.engine.write_bytes(b"exe")
    paths.translations.parent.mkdir()
    paths.translations.write_text("key,fr\n", encoding="utf-8")
    assert paths.validate() == []
