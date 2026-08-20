# Install and test KuloNiku FR on Steam Deck

> **Beta awaiting validation on real Steam Deck hardware.** The current
> AppImage passed automated checks and a complete Linux VM test with Steam and
> Proton. It is not part of a stable release yet.

## Download the beta

- [Download KuloNiku-FR-Steam-Deck-x86_64.AppImage directly](https://github.com/BertrandVillien/KuloNiku-FR/releases/download/steam-deck-1.3.0-beta.1/KuloNiku-FR-Steam-Deck-x86_64.AppImage).
- [Download its SHA-256 checksum file](https://github.com/BertrandVillien/KuloNiku-FR/releases/download/steam-deck-1.3.0-beta.1/KuloNiku-FR-Steam-Deck-x86_64.AppImage.sha256).
- [View the prerelease notes](https://github.com/BertrandVillien/KuloNiku-FR/releases/tag/steam-deck-1.3.0-beta.1).
- [View the successful workflow run](https://github.com/BertrandVillien/KuloNiku-FR/actions/runs/32386961308).

The prerelease is public and the direct downloads do not require a GitHub
account.

- AppImage SHA-256:
  `dc1454bc235652265f7b0336c2d26683312da511c55f6977c78ac5d2773baa8d`

## Before patching

1. Use the Stable SteamOS channel and install its updates.
2. Install a legitimate copy of the demo or full game from Steam, either on
   internal storage or on a Steam Deck-formatted microSD card.
3. Let Steam finish downloading the game and its Proton components.
4. Launch the **unpatched game** once, reach its main menu, and quit normally.
5. Record the Deck model, SteamOS version, game edition, and storage location.

Do not add Steam launch options. `PROTON_USE_WINED3D=1 %command%` was only a
VirtualBox workaround and must not be used on Steam Deck hardware.

## Install French

1. Select **Steam > Power > Switch to Desktop**.
2. Open Firefox and use the direct download link above. No GitHub account is
   required.
3. Open **Downloads** in Dolphin.
4. Right-click the AppImage, open **Properties > Permissions**, and
   enable **Is executable**.
5. Double-click the AppImage and choose **Launch** if Dolphin asks.
6. Wait for the automatic detection and simulation to finish.
7. Confirm that the correct Steam edition is detected and that the status says
   **Prêt à installer le français**.
8. Select **Installer le français** and confirm. A SHA-256-verified backup is
   created before the local game file is replaced.
9. After success, select **Revérifier** and confirm that the installation is
   clean and current.

![Linux installer ready to apply the patch](assets/kuloniku-fr-linux-installer.png)

If automatic detection fails, use **Changer…** and select the game directory
that contains `KuloNiku_Data`. Do not select `resources.assets` itself.

## Test in game

1. Close the AppImage and return to Gaming Mode.
2. Launch KuloNiku normally from Steam.
3. Select **Français** in the language settings.
4. Check the main menu, settings, one tutorial, one recipe, and one dialogue.
5. Quit and relaunch the game to confirm that the language remains selected.

The patch does not run in the background and does not change Proton, so it
should not reduce performance on actual hardware. Severe VM slowdown came from
VirtualBox software rendering.

## Test restore and reinstall

1. Quit the game and switch back to Desktop Mode.
2. Reopen the AppImage and wait for verification.
3. Select **Restaurer l’original** and confirm.
4. Select **Revérifier**; installation should be offered again.
5. Launch the restored game briefly and confirm that it still works.
6. Quit, reinstall French with the AppImage, and verify French in game again.

Keep the AppImage during beta testing so the patch can be checked, updated, or
restored.

Do not use `sudo`, `pacman`, Protontricks, or Wine, and do not disable SteamOS
read-only mode. Never attach game files, patch backups, Steam credentials, or
crash reports containing personal data to an issue.

[Report a Steam Deck issue](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=installation.yml)
· [Official Steam Deck Desktop Mode FAQ](https://help.steampowered.com/en/faqs/view/671A-4453-E8D2-323C)
· [Official SteamOS and Proton overview](https://www.steamdeck.com/en/software)
