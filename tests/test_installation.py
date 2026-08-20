from pathlib import Path

import pytest

from kuloniku_fr.installation import detect_asset, installation_state


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
