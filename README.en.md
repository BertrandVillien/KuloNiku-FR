# KuloNiku FR

**Community French patch for _KuloNiku: Bowl Up!_**

[View KuloNiku: Bowl Up! on Steam](https://store.steampowered.com/app/3357960/KuloNiku_Bowl_Up/)
· [Version française](README.md)

![Tests](https://github.com/BertrandVillien/KuloNiku-FR/actions/workflows/ci.yml/badge.svg)
![macOS tested](https://img.shields.io/badge/macOS-tested-2ea44f)
![Windows pending](https://img.shields.io/badge/Windows-real%20test%20pending-f0ad4e)
![Demo and full game](https://img.shields.io/badge/editions-demo%20%7C%20full-6f42c1)

![KuloNiku: Bowl Up! home screen translated into French](docs/assets/kuloniku-fr-home.jpg)

KuloNiku FR brings French to both the demo and the full game. It is free,
unofficial, and does not contain any complete game file.

## Project status

- **macOS:** a prerelease is available and tested on Apple Silicon and Intel;
- **Windows:** the engine is compatible, but the beginner-friendly interface
  still needs to be built and tested;
- **game:** full version `1.1.1` and demo `0.10.5` tested on macOS;
- **updates:** unknown new strings remain in English.

---

## Install the patch

Go to the
[official releases page](https://github.com/BertrandVillien/KuloNiku-FR/releases).
Each release note explains which file to download and how to open it.

On macOS, download the DMG that matches your Mac, then drag **KuloNiku FR** into
**Applications**. The application guides you through installation, updates, and
restoration.

After installation, launch the game from Steam and select **Français** in the
settings.

> The current Windows package is still intended for technical testing. A
> beginner-friendly interface is in preparation.

Want to inspect or modify the code? See the
[source installation guide](docs/INSTALL_FROM_SOURCE.en.md).

### What if macOS blocks the first launch?

Try to open the application once, then go to **System Settings > Privacy &
Security > Open Anyway**. You do not need to disable a Mac security feature or
use the Terminal.

[See Apple’s official instructions](https://support.apple.com/en-gb/102445)

## Easy to undo

Before modifying the game, the application runs a simulation and creates a
verified backup. The **Restore** action returns the original file.

The patch is rebuilt from your own installation: no complete game file is
downloaded or distributed.

[Read the security details](SECURITY.md) ·
[Understand the technical design](docs/DISTRIBUTION.md)

---

## An adaptation, not a word-for-word translation

Each line is compared with the languages shipped with the game, then adapted to
its context and the available screen space. Particular care is given to
Indonesian dishes, character voices, and text that still needs in-game review.

<p>
  <img src="docs/assets/kuloniku-fr-settings.jpg" width="49%" alt="French selected in the language settings">
  <img src="docs/assets/kuloniku-fr-gameplay.jpg" width="49%" alt="A recipe and tutorial translated into French">
</p>

## Contribute

You do not need to know how to code. You can:

- [suggest a French correction](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=translation.yml);
- [report an installation issue](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=installation.yml);
- attach a screenshot to show the context or an overflowing string.

Never attach a game file or a complete extraction. To contribute with Git,
Codex, Claude, or another agent, see the [contribution guide](CONTRIBUTING.md).

## Why this project?

I wanted to discover KuloNiku, but the number of English ingredients, recipes,
and culinary terms was a real barrier to enjoying it. I first looked for a
careful way to translate the demo. The result convinced me to buy the full game
instead of giving up. It also shows how localization can help new players
discover and support a game.

I built this project with Codex around one simple rule: every change should be
understandable, verifiable, and reversible. The patch is not a raw machine
translation. Each line was reviewed against the languages shipped with the game,
its available screen space, and, whenever possible, its scene context.

Indonesian was especially valuable for respecting the studio’s roots, its food,
and the intent of certain dialogues. The French wording aims to feel natural and
fit the interface, while passages that still require in-game confirmation remain
clearly marked as provisional.

## Documentation

The [project documentation](docs/README.md) brings together the FAQ,
compatibility notes, translation quality, and technical information.

---

## Unofficial project

_KuloNiku: Bowl Up!_, its text, artwork, and trademarks belong to their rights
holders, including Gambir Studio and Raw Fury. This project is neither affiliated
with nor endorsed by them. It will be removed or archived upon request or if an
official French localization is released.

## Other community translations

Other communities provide their own KuloNiku translations:

- [unofficial Korean patch](https://github.com/killterm/Localization-KuloNikuBowlUp);
- [Japanese translation tool](https://steamcommunity.com/app/3357960/discussions/0/807974496347632869/).

KuloNiku FR was created independently and did not use any file or translation
from these projects. These links are provided to help players find the community
for their language.
