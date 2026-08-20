import hashlib
from pathlib import Path
from zipfile import ZipFile

from kuloniku_fr.windows_launcher import (
    LauncherPaths,
    available_update_kind,
    available_updates,
    decode_engine_output,
    default_review_workspace_output,
    engine_environment,
    extract_translation_package,
    installed_game_candidates,
    is_prerelease_version,
    latest_release_from_payload,
    parse_steam_library_paths,
    prepare_review_test_arguments,
    review_context_directory,
    review_workspace_arguments,
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
    assert is_prerelease_version("0.3.0-beta.1") is True
    assert is_prerelease_version("0.3.0-rc.1") is True
    assert is_prerelease_version("0.3.0") is False


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
        "review-overrides.csv": b"key,fr\n",
        "TERMINOLOGY.md": b"# Glossaire\n",
        "AGENT_BRIEF.md": b"# Contexte\n",
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
    stable_release = {
        "html_url": "https://github.com/example/project/releases/tag/v0.2.0",
        "assets": [{"name": "update-manifest.json"}],
        "prerelease": False,
    }
    beta_release = {
        "html_url": "https://github.com/example/project/releases/tag/v0.3.0-beta.1",
        "assets": [{"name": "update-manifest.json"}],
        "prerelease": True,
    }

    assert latest_release_from_payload(
        [beta_release, stable_release], include_prereleases=True
    ) == beta_release
    assert latest_release_from_payload(
        [beta_release, stable_release], include_prereleases=False
    ) == stable_release
    assert latest_release_from_payload([], include_prereleases=False) is None
    assert latest_release_from_payload(stable_release, include_prereleases=False) is None


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


def test_launcher_paths_requires_engine_translations_and_review_context(tmp_path: Path):
    paths = LauncherPaths(tmp_path)
    assert len(paths.validate()) == 5

    paths.resources.mkdir()
    paths.engine.write_bytes(b"exe")
    paths.translations.parent.mkdir()
    paths.translations.write_text("key,fr\n", encoding="utf-8")
    for name in ("review-overrides.csv", "TERMINOLOGY.md", "AGENT_BRIEF.md"):
        (paths.review_context / name).write_text("test\n", encoding="utf-8")
    assert paths.validate() == []


def test_review_workspace_uses_updated_context_or_bundled_fallback(tmp_path: Path):
    bundled = tmp_path / "bundled" / "fr.csv"
    active = tmp_path / "active" / "fr.csv"
    bundled.parent.mkdir()
    active.parent.mkdir()

    assert review_context_directory(active, bundled) == bundled.parent

    for name in ("review-overrides.csv", "TERMINOLOGY.md", "AGENT_BRIEF.md"):
        (active.parent / name).write_text("test\n", encoding="utf-8")
    assert review_context_directory(active, bundled) == active.parent


def test_review_workspace_arguments_are_explicit_and_output_is_local(
    monkeypatch, tmp_path: Path
):
    local_app_data = tmp_path / "Local"
    monkeypatch.setenv("LOCALAPPDATA", str(local_app_data))
    output = default_review_workspace_output()
    context = tmp_path / "context"

    arguments = review_workspace_arguments(
        Path("engine.exe"),
        Path("game"),
        Path("fr.csv"),
        context,
        output,
    )

    assert output == local_app_data / "KuloNiku FR" / "review-workspace" / "index.html"
    assert arguments[1] == "review-workspace"
    assert arguments[-2:] == ["--output", str(output)]
    assert str(context / "review-overrides.csv") in arguments


def test_review_test_arguments_prepare_a_local_file(monkeypatch, tmp_path: Path):
    local_app_data = tmp_path / "Local"
    monkeypatch.setenv("LOCALAPPDATA", str(local_app_data))
    from kuloniku_fr.windows_launcher import default_review_test_output

    output = default_review_test_output()
    arguments = prepare_review_test_arguments(
        Path("engine.exe"),
        Path("game"),
        Path("propositions.csv"),
        Path("fr.csv"),
        output,
    )

    assert arguments[1] == "prepare-review-test"
    assert arguments[-2:] == ["--output", str(output)]
    assert output == local_app_data / "KuloNiku FR" / "review-test" / "fr.csv"
