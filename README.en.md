# KuloNiku FR

**Community French patch for _KuloNiku: Bowl Up!_**

[View or buy KuloNiku: Bowl Up! on Steam](https://store.steampowered.com/app/3357960/KuloNiku_Bowl_Up/)

[Version française](README.md)

![Tests](https://github.com/BertrandVillien/KuloNiku-FR/actions/workflows/ci.yml/badge.svg)
![macOS tested](https://img.shields.io/badge/macOS-tested-2ea44f)
![Windows pending](https://img.shields.io/badge/Windows-real%20test%20pending-f0ad4e)
![Demo and full game](https://img.shields.io/badge/editions-demo%20%7C%20full-6f42c1)

![KuloNiku: Bowl Up! home screen translated into French](docs/assets/kuloniku-fr-home.jpg)

KuloNiku FR brings a community-made French localization to both the demo and
the full game. It is free, unofficial, and intended as a temporary solution
until an official French localization becomes available.

## Why I made this patch

I wanted to discover KuloNiku, but the number of English ingredient names and
culinary terms was a real barrier to enjoying it. I first looked for a safe way
to translate the demo. Once that worked, I bought the full game instead of
giving up, which also shows how localization can help French-speaking players
discover and support the game.

I built the project with Codex and kept every operation reversible: text
extraction, language comparison, simulation, backup, then injection. Because
the current menu cannot display an extra language, the patch temporarily
reuses the German slot and keeps English as the safe fallback. Restoring the
game immediately makes German available again.

The French adaptation was reviewed line by line using all eight languages in
the game, technical keys, and available scene context. Indonesian was
especially helpful for respecting the studio’s background and clarifying some
dishes; difficult terms received additional research. Wording also stays as
close as possible to the lengths already supported by the game to reduce layout
issues.

## Project status

- French translation of every textual entry currently used by the game;
- full game `1.1.1` and demo `0.10.5` tested on macOS;
- patching engine compatible with macOS and Windows, with a real Windows test still needed;
- unknown new strings remain in English after an update;
- no game data or complete game file is distributed.

## Simple installation — coming soon

Standalone **macOS** and **Windows** installers are being validated. This will
be the recommended method: download the appropriate package from the
[Releases](https://github.com/BertrandVillien/KuloNiku-FR/releases) page, run
the installer, review the displayed simulation, then confirm.

The first release has not been published yet. Until then, the following method
lets you test the patch from source.

### First launch on macOS

The application is locally signed by GitHub Actions but is not notarized by
Apple. It works on Apple Silicon and Intel Macs without a paid developer
membership. Download it only from the project’s
[official releases](https://github.com/BertrandVillien/KuloNiku-FR/releases).

If macOS blocks the first launch:

1. try to open **KuloNiku FR** once;
2. open **System Settings > Privacy & Security**;
3. scroll to the KuloNiku FR message, then click **Open Anyway**;
4. confirm **Open**. macOS remembers this choice for the application.

This is the procedure documented by
[Apple](https://support.apple.com/en-gb/102445). You do not need to disable
Gatekeeper or enter a Terminal command.

The installer automatically finds Steam, prioritizes the full game over the
demo, and presents a simple status. The technical log stays collapsed. A French
update is offered only when the exact translation fingerprint differs. Future
translation bundles can be downloaded and verified without reinstalling the
application, unless they require a newer patching engine; the GitHub check will
become active with the first release.

## Installation from source

This method requires [Python](https://www.python.org/) and
[uv](https://docs.astral.sh/uv/). It will remain available for people who want
to inspect or modify the code.

1. Close the game.
2. Install dependencies:

   ```sh
   uv sync
   ```

3. Run the simulation first; it makes no changes:

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

## Why installation remains safe

- mandatory simulation before writing;
- SHA-256-verified local backup;
- reconstruction from your own installation;
- atomic replacement and straightforward restoration;
- English and Indonesian text checks before each injection;
- English fallback when an update changes or adds a string.

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

## Contributing without knowing how to code

Open the
[Suggest a French correction](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=translation.yml)
form directly to:

- suggest better wording;
- attach a screenshot and explain the context;
- report text that is too long or an installation issue.

You must be signed in to a free GitHub account to view the form. The technical
key is optional. Once the form is complete, click **Submit new issue**: your
proposal will appear in the project’s issues and can be discussed. For an
installation issue, use
[Report an installation issue](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=installation.yml)
instead.

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

_KuloNiku: Bowl Up!_, its text, visuals, and trademarks belong to their
respective rights holders, including Gambir Studio and Raw Fury. This project is
not affiliated with or endorsed by them. It distributes no complete game file
and will be removed or archived upon request or when an official French
localization becomes available.
