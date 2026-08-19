from pathlib import Path

import pytest

from kuloniku_fr.installation import detect_asset


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
