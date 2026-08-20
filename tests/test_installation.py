from pathlib import Path

import pytest

from kuloniku_fr import installation
from kuloniku_fr.installation import (
    GameAsset,
    atomic_copy,
    backup_asset,
    detect_asset,
    installation_state,
    require_writable_asset,
    user_data_dir,
)


def test_detect_windows_asset(tmp_path: Path):
    asset = tmp_path / "KuloNiku_Data" / "resources.assets"
    asset.parent.mkdir()
    asset.write_bytes(b"test")

    detected = detect_asset(tmp_path)

    assert detected.path == asset.resolve()
    assert detected.platform == "windows"
    assert detected.edition == "full"


def test_detect_refuses_ambiguous_assets(tmp_path: Path):
    for name in ("A_Data", "B_Data"):
        path = tmp_path / name / "resources.assets"
        path.parent.mkdir()
        path.write_bytes(b"test")

    with pytest.raises(FileNotFoundError):
        detect_asset(tmp_path)


@pytest.mark.parametrize(
    ("current_hash", "french_active", "manifest", "expected"),
    [
        ("patched", True, {"patched_sha256": "patched"}, "patched"),
        ("other", True, {"patched_sha256": "patched"}, "patched_unknown"),
        ("original", False, {"original_sha256": "original"}, "restored"),
        ("steam-update", False, {"original_sha256": "original"}, "game_updated"),
        ("new", False, None, "unpatched"),
    ],
)
def test_installation_state(current_hash, french_active, manifest, expected):
    assert installation_state(current_hash, french_active, manifest) == expected


def test_linux_user_data_uses_xdg(monkeypatch, tmp_path: Path):
    xdg_data = tmp_path / "xdg-data"
    monkeypatch.setattr(installation.platform, "system", lambda: "Linux")
    monkeypatch.setenv("XDG_DATA_HOME", str(xdg_data))

    assert user_data_dir() == xdg_data / "kuloniku-fr"


def test_unwritable_game_file_has_a_clear_error(monkeypatch, tmp_path: Path):
    asset = tmp_path / "resources.assets"
    asset.write_bytes(b"game")
    monkeypatch.setattr(installation.os, "access", lambda path, mode: False)

    with pytest.raises(PermissionError, match="n’est pas accessible en écriture"):
        require_writable_asset(asset)


def test_linux_backup_and_restore_round_trip(monkeypatch, tmp_path: Path):
    from hashlib import sha256

    xdg_data = tmp_path / "xdg-data"
    asset_path = tmp_path / "KuloNiku_Data" / "resources.assets"
    asset_path.parent.mkdir()
    asset_path.write_bytes(b"original")
    monkeypatch.setattr(installation.platform, "system", lambda: "Linux")
    monkeypatch.setenv("XDG_DATA_HOME", str(xdg_data))
    digest = lambda path: sha256(path.read_bytes()).hexdigest()

    backup, manifest = backup_asset(GameAsset(asset_path, "windows", "full"), digest)
    asset_path.write_bytes(b"patched")
    atomic_copy(backup, asset_path)

    assert backup.is_relative_to(xdg_data / "kuloniku-fr" / "backups")
    assert manifest.is_file()
    assert asset_path.read_bytes() == b"original"
    assert digest(asset_path) == digest(backup)
