from __future__ import annotations

from dataclasses import dataclass
import struct


class I2FormatError(ValueError):
    """Le contenu I2 Localization ne correspond pas au format attendu."""


class Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.position = 0

    def _require(self, size: int) -> None:
        if size < 0 or self.position + size > len(self.data):
            raise I2FormatError(
                f"Lecture invalide à l’octet {self.position} (taille {size})."
            )

    def align4(self) -> None:
        self.position = (self.position + 3) & ~3

    def int32(self) -> int:
        self._require(4)
        value = struct.unpack_from("<i", self.data, self.position)[0]
        self.position += 4
        return value

    def int64(self) -> int:
        self._require(8)
        value = struct.unpack_from("<q", self.data, self.position)[0]
        self.position += 8
        return value

    def float32(self) -> float:
        self._require(4)
        value = struct.unpack_from("<f", self.data, self.position)[0]
        self.position += 4
        return value

    def uint8_aligned(self) -> int:
        self._require(1)
        value = self.data[self.position]
        self.position += 1
        self.align4()
        return value

    def string(self) -> str:
        size = self.int32()
        self._require(size)
        raw = self.data[self.position : self.position + size]
        self.position += size
        self.align4()
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise I2FormatError("Chaîne I2 non UTF-8.") from exc

    def strings(self) -> list[str]:
        count = self.int32()
        if not 0 <= count <= 100_000:
            raise I2FormatError(f"Nombre de chaînes invraisemblable : {count}.")
        return [self.string() for _ in range(count)]

    def byte_array(self) -> bytes:
        size = self.int32()
        self._require(size)
        value = self.data[self.position : self.position + size]
        self.position += size
        self.align4()
        return value


class Writer:
    def __init__(self):
        self.data = bytearray()

    def align4(self) -> None:
        self.data.extend(b"\0" * ((-len(self.data)) % 4))

    def int32(self, value: int) -> None:
        self.data.extend(struct.pack("<i", value))

    def int64(self, value: int) -> None:
        self.data.extend(struct.pack("<q", value))

    def float32(self, value: float) -> None:
        self.data.extend(struct.pack("<f", value))

    def uint8_aligned(self, value: int) -> None:
        self.data.append(value)
        self.align4()

    def string(self, value: str) -> None:
        raw = value.encode("utf-8")
        self.int32(len(raw))
        self.data.extend(raw)
        self.align4()

    def strings(self, values: list[str]) -> None:
        self.int32(len(values))
        for value in values:
            self.string(value)

    def byte_array(self, value: bytes) -> None:
        self.int32(len(value))
        self.data.extend(value)
        self.align4()


@dataclass
class Pointer:
    file_id: int
    path_id: int


@dataclass
class Term:
    key: str
    term_type: int
    translations: list[str]
    flags: bytes
    touch_translations: list[str]


@dataclass
class Language:
    name: str
    code: str
    flags: int


@dataclass
class LanguageSource:
    game_object: Pointer
    enabled: int
    script: Pointer
    name: str
    agrees_scene: int
    agrees_plugins: int
    google_live_sync_up_to_date: int
    terms: list[Term]
    case_insensitive_terms: int
    missing_translation_mode: int
    app_name_term: str
    languages: list[Language]
    ignore_device_language: int
    allow_unloading_languages: int
    google_web_service_url: str
    google_spreadsheet_key: str
    google_spreadsheet_name: str
    google_last_updated_version: str
    google_update_frequency: int
    google_editor_check_frequency: int
    google_update_synchronization: int
    google_update_delay: float
    assets: list[Pointer]

    @classmethod
    def parse(cls, data: bytes) -> "LanguageSource":
        reader = Reader(data)
        game_object = Pointer(reader.int32(), reader.int64())
        enabled = reader.uint8_aligned()
        script = Pointer(reader.int32(), reader.int64())
        name = reader.string()
        agrees_scene = reader.uint8_aligned()
        agrees_plugins = reader.uint8_aligned()
        google_live_sync_up_to_date = reader.uint8_aligned()

        term_count = reader.int32()
        if not 0 <= term_count <= 100_000:
            raise I2FormatError(f"Nombre de termes invraisemblable : {term_count}.")
        terms = []
        for _ in range(term_count):
            terms.append(
                Term(
                    key=reader.string(),
                    term_type=reader.int32(),
                    translations=reader.strings(),
                    flags=reader.byte_array(),
                    touch_translations=reader.strings(),
                )
            )

        case_insensitive_terms = reader.uint8_aligned()
        missing_translation_mode = reader.int32()
        app_name_term = reader.string()

        language_count = reader.int32()
        languages = [
            Language(reader.string(), reader.string(), reader.uint8_aligned())
            for _ in range(language_count)
        ]

        ignore_device_language = reader.uint8_aligned()
        allow_unloading_languages = reader.int32()
        google_web_service_url = reader.string()
        google_spreadsheet_key = reader.string()
        google_spreadsheet_name = reader.string()
        google_last_updated_version = reader.string()
        google_update_frequency = reader.int32()
        google_editor_check_frequency = reader.int32()
        google_update_synchronization = reader.int32()
        google_update_delay = reader.float32()

        asset_count = reader.int32()
        assets = [Pointer(reader.int32(), reader.int64()) for _ in range(asset_count)]
        if reader.position != len(data):
            raise I2FormatError(
                f"{len(data) - reader.position} octets inattendus en fin d’objet I2."
            )

        return cls(
            game_object,
            enabled,
            script,
            name,
            agrees_scene,
            agrees_plugins,
            google_live_sync_up_to_date,
            terms,
            case_insensitive_terms,
            missing_translation_mode,
            app_name_term,
            languages,
            ignore_device_language,
            allow_unloading_languages,
            google_web_service_url,
            google_spreadsheet_key,
            google_spreadsheet_name,
            google_last_updated_version,
            google_update_frequency,
            google_editor_check_frequency,
            google_update_synchronization,
            google_update_delay,
            assets,
        )

    def serialize(self) -> bytes:
        writer = Writer()
        writer.int32(self.game_object.file_id)
        writer.int64(self.game_object.path_id)
        writer.uint8_aligned(self.enabled)
        writer.int32(self.script.file_id)
        writer.int64(self.script.path_id)
        writer.string(self.name)
        writer.uint8_aligned(self.agrees_scene)
        writer.uint8_aligned(self.agrees_plugins)
        writer.uint8_aligned(self.google_live_sync_up_to_date)

        writer.int32(len(self.terms))
        for term in self.terms:
            writer.string(term.key)
            writer.int32(term.term_type)
            writer.strings(term.translations)
            writer.byte_array(term.flags)
            writer.strings(term.touch_translations)

        writer.uint8_aligned(self.case_insensitive_terms)
        writer.int32(self.missing_translation_mode)
        writer.string(self.app_name_term)
        writer.int32(len(self.languages))
        for language in self.languages:
            writer.string(language.name)
            writer.string(language.code)
            writer.uint8_aligned(language.flags)

        writer.uint8_aligned(self.ignore_device_language)
        writer.int32(self.allow_unloading_languages)
        writer.string(self.google_web_service_url)
        writer.string(self.google_spreadsheet_key)
        writer.string(self.google_spreadsheet_name)
        writer.string(self.google_last_updated_version)
        writer.int32(self.google_update_frequency)
        writer.int32(self.google_editor_check_frequency)
        writer.int32(self.google_update_synchronization)
        writer.float32(self.google_update_delay)
        writer.int32(len(self.assets))
        for asset in self.assets:
            writer.int32(asset.file_id)
            writer.int64(asset.path_id)
        return bytes(writer.data)


def find_i2_object(environment):
    matches = []
    for obj in environment.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        try:
            if obj.peek_name() == "I2Languages":
                matches.append(obj)
        except (ValueError, AttributeError, FileNotFoundError):
            continue
    if len(matches) != 1:
        raise I2FormatError(
            f"Un objet I2Languages était attendu, {len(matches)} trouvé(s)."
        )
    return matches[0]
