# Install KuloNiku FR on Steam Deck

> **Beta awaiting validation on a real Steam Deck.** The current AppImage is a
> test artifact and is not included in a stable release yet.

1. Switch to **Desktop Mode**.
2. Download `KuloNiku-FR-Steam-Deck-x86_64.AppImage` from the latest
   [Steam Deck build](https://github.com/BertrandVillien/KuloNiku-FR/actions/workflows/package-steam-deck.yml).
3. Right-click the file, open **Properties > Permissions**, and enable
   **Is executable**.
4. Open the AppImage and choose **Installer le français**.
5. Return to Gaming Mode, launch KuloNiku, and select **Français** in settings.

The application detects internal storage, Steam libraries, and microSD cards.
If needed, **Changer…** lets you select the folder containing `KuloNiku_Data`.

During beta testing, GitHub automatically wraps the artifact in a download
archive. Extract it once to get the AppImage. The future stable release will
provide the AppImage file directly.

Do not use `sudo`, `pacman`, Protontricks, Wine, or disable SteamOS read-only
mode. The AppImage requires no system installation.

[Official AppImage guide](https://docs.appimage.org/introduction/quickstart.html)
· [Official Steam Deck Desktop Mode FAQ](https://help.steampowered.com/es/faqs/view/671A-4453-E8D2-323C)

After testing on real hardware, report any issue through the
[installation form](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=installation.yml).
