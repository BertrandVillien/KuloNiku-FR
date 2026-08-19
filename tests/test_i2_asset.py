from pathlib import Path

import pytest

from kuloniku_fr.i2_asset import LanguageSource
from kuloniku_fr.translation import apply_french, lint_translation


LAB_ASSET = Path("work/lab/game/resources.assets")


@pytest.mark.skipif(not LAB_ASSET.exists(), reason="copie de laboratoire absente")
def test_round_trip_real_i2_object():
    import UnityPy

    environment = UnityPy.load(str(LAB_ASSET))
    obj = next(obj for obj in environment.objects if obj.path_id == 3606)
    raw = obj.get_raw_data()
    source = LanguageSource.parse(raw)

    assert len(source.terms) == 12_211
    assert [language.code for language in source.languages] == [
        "en",
        "id",
        "es",
        "th",
        "zh-CN",
        "zh-TW",
        "de",
        "pt",
    ]
    assert source.serialize() == raw


@pytest.mark.skipif(not LAB_ASSET.exists(), reason="copie de laboratoire absente")
def test_append_french_keeps_languages_and_falls_back_to_english():
    import UnityPy

    environment = UnityPy.load(str(LAB_ASSET))
    obj = next(obj for obj in environment.objects if obj.path_id == 3606)
    source = LanguageSource.parse(obj.get_raw_data())
    original_codes = [language.code for language in source.languages]

    translated, fallback, unknown = apply_french(
        source, {"ACTION_SERVE": "Servir"}, slot_language=None
    )

    assert [language.code for language in source.languages] == [*original_codes, "fr"]
    assert translated == 1
    assert fallback == len(source.terms) - 1
    assert unknown == []
    serve = next(term for term in source.terms if term.key == "ACTION_SERVE")
    assert serve.translations[-1] == "Servir"
    assert serve.touch_translations == []
    other = next(term for term in source.terms if term.key != "ACTION_SERVE")
    assert other.translations[-1] == other.translations[0]
    reparsed = LanguageSource.parse(source.serialize())
    assert reparsed.languages[-1].code == "fr"


@pytest.mark.skipif(not LAB_ASSET.exists(), reason="copie de laboratoire absente")
def test_french_slot_keeps_supported_language_metadata():
    import UnityPy

    environment = UnityPy.load(str(LAB_ASSET))
    obj = next(obj for obj in environment.objects if obj.path_id == 3606)
    source = LanguageSource.parse(obj.get_raw_data())
    original_languages = [
        (language.name, language.code) for language in source.languages
    ]

    apply_french(
        source,
        {"SETTINGS_LANGUAGESELECTION": "Français", "ACTION_SERVE": "Servir"},
        slot_language="de",
    )

    assert [
        (language.name, language.code) for language in source.languages
    ] == original_languages
    german_index = [language.code for language in source.languages].index("de")
    selection = next(
        term for term in source.terms if term.key == "SETTINGS_LANGUAGESELECTION"
    )
    serve = next(term for term in source.terms if term.key == "ACTION_SERVE")
    assert selection.translations[german_index] == "Français"
    assert serve.translations[german_index] == "Servir"


@pytest.mark.skipif(not LAB_ASSET.exists(), reason="copie de laboratoire absente")
def test_lint_detects_length_and_preserves_tokens():
    import UnityPy

    environment = UnityPy.load(str(LAB_ASSET))
    obj = next(obj for obj in environment.objects if obj.path_id == 3606)
    source = LanguageSource.parse(obj.get_raw_data())
    term = next(term for term in source.terms if term.key == "ACTION_SERVE")
    warnings = lint_translation(term, "Une traduction volontairement beaucoup trop longue")
    assert any(warning.kind == "length" for warning in warnings)
