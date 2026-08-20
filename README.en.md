# KuloNiku FR

**Community French patch for _KuloNiku: Bowls Up!_**

[Version française](README.md)

![Tests](https://github.com/BertrandVillien/KuloNiku-FR/actions/workflows/ci.yml/badge.svg)
![macOS tested](https://img.shields.io/badge/macOS-tested-2ea44f)
![Windows pending](https://img.shields.io/badge/Windows-real%20test%20pending-f0ad4e)
![Demo and full game](https://img.shields.io/badge/editions-demo%20%7C%20full-6f42c1)

![KuloNiku: Bowls Up! home screen translated into French](docs/assets/kuloniku-fr-home.jpg)

KuloNiku FR brings a community-made French localization to both the demo and
the full game. It is free, unofficial, and intended as a temporary solution
until an official French localization becomes available.

## Project status

- French translation of every textual entry currently used by the game;
- full game `1.1.1` and demo `0.10.5` tested on macOS;
- macOS and Windows patching engine, with a real Windows test still pending;
- unknown strings safely fall back to English after game updates;
- no complete game file or extracted multilingual table is distributed.

> The patch currently reuses the German language slot. Restoring the game makes
> German available again immediately.

## Current installation method

Standalone installers are being prepared. Installing from source currently
requires [Python](https://www.python.org/) and
[uv](https://docs.astral.sh/uv/).

1. Close the game.
2. Install dependencies:

   ```sh
   uv sync
   ```

3. Run the read-only simulation first:

   ```sh
   uv run kuloniku-fr install "/path/to/KuloNiku.app"
   ```

4. If the diagnosis is correct, install the patch:

   ```sh
   uv run kuloniku-fr install "/path/to/KuloNiku.app" --apply
   ```

5. Launch the game from Steam and select **Français** in the settings.

On Windows, provide the folder containing `KuloNiku_Data` instead of the macOS
application.

To restore the verified backup created automatically:

```sh
uv run kuloniku-fr restore "/path/to/KuloNiku.app" --apply
```

## Safety model

- mandatory dry run before writing;
- local SHA-256-verified backup;
- reconstruction from the player’s own installation;
- atomic replacement and straightforward rollback;
- English and Indonesian source checks before each injection;
- English fallback whenever an update changes or adds a string.

## An adaptation, not a word-for-word translation

Every line is reviewed against all eight languages shipped with the game, its
technical key, scene context, and available interface space. English is the
reference for facts and rules, while Indonesian helps preserve cultural,
culinary, and studio intent. Traditional dishes follow established French usage
instead of approximate literal translations.

<p>
  <img src="docs/assets/kuloniku-fr-settings.jpg" width="49%" alt="French selected in the language settings">
  <img src="docs/assets/kuloniku-fr-gameplay.jpg" width="49%" alt="A recipe and tutorial translated into French">
</p>

## Contributing without coding

GitHub forms let players propose improved wording, attach a contextual
screenshot, report text that does not fit, or describe an installation issue.
The technical key is optional.

Never attach a game file or a complete extraction. See
[CONTRIBUTING.md](CONTRIBUTING.md) to contribute through Git or with an agent
such as Codex, Claude, or another tool.

Other language communities may fork the patching engine, subject to the rights
that apply to the game and their translations.

## Documentation

- [FAQ in French](docs/FAQ.md)
- [Compatibility and updates](docs/UPDATES.md)
- [Translation quality](docs/QUALITY.md)
- [French terminology](docs/TERMINOLOGY.md)
- [Security policy](SECURITY.md)
- [Legal context and attribution](docs/LEGAL.md)

## Unofficial project

_KuloNiku: Bowls Up!_, its text, visuals, and trademarks belong to their
respective rights holders, including Gambir Studio and Raw Fury. This project is
not affiliated with or endorsed by them. It distributes no complete game file
and will be removed or archived upon request or when an official French
localization becomes available.
