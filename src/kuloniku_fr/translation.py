from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re

from .i2_asset import LanguageSource, Term


TOKEN_PATTERN = re.compile(
    r"\[[^\[\]]+\]|\{[^{}]+\}|<[^<>]+>|%(?:\d+\$)?[-+#0 '.]*\d*(?:\.\d+)?[a-zA-Z]|\\[nrt]"
)


@dataclass(frozen=True)
class TranslationWarning:
    key: str
    kind: str
    message: str


def tokens(value: str) -> Counter[str]:
    return Counter(TOKEN_PATTERN.findall(value))


def source_character_limit(term: Term) -> int:
    return max((len(value) for value in term.translations if value), default=0)


def lint_translation(term: Term, french: str) -> list[TranslationWarning]:
    warnings: list[TranslationWarning] = []
    english = term.translations[0] if term.translations else ""
    expected_tokens = tokens(english)
    actual_tokens = tokens(french)
    if expected_tokens != actual_tokens:
        warnings.append(
            TranslationWarning(
                term.key,
                "tokens",
                f"marqueurs différents : attendu {dict(expected_tokens)}, obtenu {dict(actual_tokens)}",
            )
        )

    limit = source_character_limit(term)
    if limit and len(french) > limit:
        warnings.append(
            TranslationWarning(
                term.key,
                "length",
                f"{len(french)} caractères, maximum observé dans les langues source : {limit}",
            )
        )
    return warnings


def apply_french(
    source: LanguageSource,
    translations: dict[str, str],
    *,
    slot_language: str | None = "de",
) -> tuple[int, int, list[str]]:
    """Injecte le français dans un emplacement reconnu par le menu du jeu.

    Toutes les clés françaises absentes reçoivent la version anglaise de la version
    installée. Une mise à jour du jeu peut donc ajouter de nouvelles clés sans rendre
    le patch inutilisable.

    KuloNiku filtre son menu avec une liste codée séparément. Le nom et le code de
    l'emplacement doivent donc rester inchangés. ``None`` conserve un mode
    expérimental d'ajout, utile pour l'analyse mais non proposé par l'installateur.
    """

    codes = [language.code for language in source.languages]
    if "fr" in codes:
        target_index = codes.index("fr")
        source.languages[target_index].name = "French"
    elif slot_language:
        try:
            target_index = codes.index(slot_language)
        except ValueError as exc:
            raise ValueError(f"Emplacement de langue absent : {slot_language}") from exc
    else:
        from .i2_asset import Language

        target_index = len(source.languages)
        source.languages.append(Language("French", "fr", 0))

    known_keys = {term.key for term in source.terms}
    unknown_keys = sorted(set(translations) - known_keys)
    translated = 0
    fallback = 0
    for term in source.terms:
        english = term.translations[0] if term.translations else ""
        value = translations.get(term.key, english)
        if term.key in translations:
            translated += 1
        else:
            fallback += 1

        while len(term.translations) <= target_index:
            term.translations.append(english)
        term.translations[target_index] = value

        # Une liste tactile vide signifie « fonctionnalité non utilisée » dans
        # cet asset. Ne pas la matérialiser artificiellement.
        if term.touch_translations:
            while len(term.touch_translations) <= target_index:
                term.touch_translations.append(english)
            term.touch_translations[target_index] = value

        # I2 conserve un octet d'état par langue dans cette table.
        if len(term.flags) < len(source.languages):
            term.flags += b"\0" * (len(source.languages) - len(term.flags))

    return translated, fallback, unknown_keys
