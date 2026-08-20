# Test KuloNiku FR on Steam Deck

> **Mission:** install French, check a few screens, then test restoration. Allow
> about **10 to 15 minutes**. No GitHub account or Terminal is required.

## 1. Prepare the game

- Update SteamOS.
- Install the demo or full game from Steam.
- Launch the unpatched game once, reach the main menu, and quit.

## 2. Open the installer

1. Select **Steam > Power > Switch to Desktop**.
2. [Download the AppImage](https://github.com/BertrandVillien/KuloNiku-FR/releases/download/steam-deck-1.3.0-beta.1/KuloNiku-FR-Steam-Deck-x86_64.AppImage).
3. In **Dolphin > Downloads**, right-click the file.
4. Open **Properties > Permissions** and enable **Is executable**.
5. Double-click the AppImage and choose **Launch** if asked.

## 3. Install French

1. Wait for **Prêt à installer le français**.
2. [Take the first screenshot of the application](#requested-screenshots).
3. Select **Installer le français** and confirm.
4. After success, select **Revérifier**. The application should display
   **Installation propre et à jour**.

![Installer ready to apply the patch](assets/kuloniku-fr-linux-installer.png)

If the game is not found, select **Changer…** and choose the game directory that
contains `KuloNiku_Data`.

## 4. Check the game

1. Close the installer and select **Return to Gaming Mode**.
2. Launch KuloNiku from Steam.
3. Select **Français** in the language settings.
4. Check the main menu, one tutorial, one recipe, and one dialogue.
5. Quit and relaunch the game. French should remain selected.

## 5. Test restoration

1. Quit the game and return to Desktop Mode.
2. Reopen the AppImage and select **Restaurer l’original**.
3. Select **Revérifier**. Installation should be offered again.
4. Launch the game briefly and confirm that it still works.
5. Reinstall French and run one final check.

## Requested screenshots

One screenshot is required: **the installer window**, preferably showing
**Installation propre et à jour**.

If possible, also capture each main step:

- installer ready;
- installation successful;
- game menu in French;
- restoration successful;
- French reinstalled.

### Taking screenshots

- **Desktop Mode:** open the application menu, search for **Spectacle**, then
  select **Active Window** or **Rectangular Region**. Save the PNG in
  **Pictures**.
- **Gaming Mode:** press **Steam + R1** together. Screenshots appear under
  **Steam > Media**.

Send the PNG or JPG images through the same channel used to share this guide
(email, messaging app, shared folder, and so on). No GitHub account is needed.
Include the Deck model, game edition, storage location, and what worked or
failed.

Hide account names and personal paths. Never send game files or backups made by
the installer.

## If something goes wrong

- **The AppImage does not open:** confirm that **Is executable** is enabled.
- **The game is not found:** use **Changer…**.
- **An error appears:** take a screenshot and stop the test.
- **The game no longer starts:** reopen the AppImage and select
  **Restaurer l’original**.

[View the prerelease](https://github.com/BertrandVillien/KuloNiku-FR/releases/tag/steam-deck-1.3.0-beta.1)
· [French language selection](LANGUAGE_SELECTION.md)
