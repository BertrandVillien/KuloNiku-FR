import json

import pytest

from kuloniku_fr.i2_asset import Language, LanguageSource, Pointer, Term
from kuloniku_fr.review_workspace import build_review_payload, write_review_workspace


def make_source(*, patched: bool = False) -> LanguageSource:
    selection_de = "Français" if patched else "Deutsch"
    terms = [
        Term(
            "SETTINGS_LANGUAGESELECTION",
            0,
            ["Language", "Bahasa", selection_de],
            b"",
            [],
        ),
        Term(
            "Dialogue/STELLA_HELLO_1",
            0,
            ["Welcome, rookie!", "Selamat datang!", "Willkommen!"],
            b"",
            [],
        ),
        Term(
            "Dialogue/STELLA_HELLO_2",
            0,
            ["Ready to cook?", "Siap memasak?", "Bereit?"],
            b"",
            [],
        ),
    ]
    return LanguageSource(
        game_object=Pointer(0, 0),
        enabled=1,
        script=Pointer(0, 0),
        name="I2Languages",
        agrees_scene=0,
        agrees_plugins=0,
        google_live_sync_up_to_date=0,
        terms=terms,
        case_insensitive_terms=0,
        missing_translation_mode=0,
        app_name_term="",
        languages=[
            Language("English", "en", 0),
            Language("Indonesian", "id", 0),
            Language("German", "de", 0),
        ],
        ignore_device_language=0,
        allow_unloading_languages=0,
        google_web_service_url="",
        google_spreadsheet_key="",
        google_spreadsheet_name="",
        google_last_updated_version="",
        google_update_frequency=0,
        google_editor_check_frequency=0,
        google_update_synchronization=0,
        google_update_delay=0.0,
        assets=[],
    )


BRIEF = """# Brief

## Univers et ton

Un jeu chaleureux de cuisine et de gestion.

## Voix récurrentes

- **Stella** : rivale théâtrale et mordante.

## Contraintes

Préserver les variables.
"""


def test_review_payload_joins_french_notes_lore_and_groups():
    payload = build_review_payload(
        make_source(),
        {
            "Dialogue/STELLA_HELLO_1": {
                "fr": "Bienvenue, débutant !",
                "status": "reviewed",
                "notes": "Ton mordant.",
            }
        },
        {
            "Dialogue/STELLA_HELLO_1": {
                "fr": "Bienvenue, débutant !",
                "status": "reviewed",
                "notes": "Vu en jeu.",
            }
        },
        terminology_markdown="# Terminologie\n\nMeatball : boulette.",
        agent_brief_markdown=BRIEF,
        edition="full",
        asset_sha256="abc",
    )

    row = payload["rows"][1]
    assert payload["languages"] == [
        {"code": "en", "name": "Anglais"},
        {"code": "id", "name": "Indonésien"},
        {"code": "de", "name": "Allemand"},
    ]
    assert row["fr"] == "Bienvenue, débutant !"
    assert row["missing_fr"] is False
    assert payload["metadata"]["missing_french"] == 2
    assert row["languages"]["id"] == "Selamat datang!"
    assert row["group"] == "dialogue-stella"
    assert row["macro"] == "dialogue"
    assert row["characters"] == ["Stella"]
    assert row["translation_notes"] == "Ton mordant.\nVu en jeu."
    assert payload["references"]["universe"].startswith("Un jeu chaleureux")


def test_review_payload_rejects_an_already_patched_source():
    with pytest.raises(ValueError, match="Restaurez"):
        build_review_payload(
            make_source(patched=True),
            {},
            {},
            terminology_markdown="",
            agent_brief_markdown=BRIEF,
            edition="full",
            asset_sha256="abc",
        )


def test_workspace_is_self_contained_and_escapes_script_end(tmp_path):
    payload = build_review_payload(
        make_source(),
        {
            "Dialogue/STELLA_HELLO_1": {
                "fr": "Ne pas écrire </script> ici",
                "status": "reviewed",
                "notes": "",
            }
        },
        {},
        terminology_markdown="",
        agent_brief_markdown=BRIEF,
        edition="full",
        asset_sha256="abc",
    )
    output = write_review_workspace(payload, tmp_path / "review" / "index.html")
    html = output.read_text(encoding="utf-8")

    assert "100 % hors ligne" in html
    assert "sélectionnez seulement ceux" in html
    assert "Exporter ma sélection" in html
    assert "Traductions manquantes" in html
    assert "Projet GitHub" in html
    assert "function renderList" in html
    assert "showCountFilter" in html
    assert "review.yml" in html
    assert "progressBar" not in html
    assert "function renderMarkdown" in html
    assert "function renderGameText" in html
    assert "game-variable" in html
    assert "game-color-alert" in html
    assert "defaultExpandedLanguages=['en','de','es','pt','id']" in html
    assert "kuloniku-review-ui-v1" in html
    assert "Afficher le texte brut" in html
    assert "function renderLanguage" in html
    assert "function renderHiddenLanguages" in html
    assert ".game-color .game-variable" in html
    assert "Icône monnaie" in html
    assert "Effacer les filtres" in html
    assert "clearFilters" in html
    assert "connect-src 'none'" in html
    assert "Ne pas écrire <\\/script> ici" in html
    embedded = html.split('<script id="reviewData" type="application/json">', 1)[1]
    embedded = embedded.split("</script>", 1)[0].replace("<\\/", "</")
    assert json.loads(embedded)["metadata"]["rows"] == 3
