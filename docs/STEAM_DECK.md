# Installer KuloNiku FR sur Steam Deck

> **Bêta à valider sur un véritable Steam Deck.** L’AppImage actuelle sert aux
> essais et n’est pas encore incluse dans une release stable.

1. Passez en **mode Bureau**.
2. Téléchargez `KuloNiku-FR-Steam-Deck-x86_64.AppImage` depuis l’artefact de la
   dernière [fabrication Steam Deck](https://github.com/BertrandVillien/KuloNiku-FR/actions/workflows/package-steam-deck.yml).
3. Faites un clic droit sur le fichier, puis ouvrez **Propriétés > Permissions**
   et cochez **Est exécutable**.
4. Ouvrez l’AppImage et choisissez **Installer le français**.
5. Revenez en mode Jeu, lancez KuloNiku et choisissez **Français** dans les
   paramètres.

L’application détecte le stockage interne, les bibliothèques Steam et la carte
microSD. Si nécessaire, **Changer…** permet de choisir manuellement le dossier
qui contient `KuloNiku_Data`.

Pendant la bêta, GitHub place automatiquement l’artefact dans une archive de
téléchargement : extrayez-la une seule fois pour obtenir l’AppImage. La future
release stable proposera directement le fichier AppImage.

N’utilisez pas `sudo`, `pacman`, Protontricks, Wine et ne désactivez pas le mode
lecture seule de SteamOS. L’AppImage ne demande aucune installation système.

[Guide officiel AppImage](https://docs.appimage.org/introduction/quickstart.html)
· [FAQ officielle du mode Bureau Steam Deck](https://help.steampowered.com/es/faqs/view/671A-4453-E8D2-323C)

## Valider la bêta

Un test complet sur un vrai Deck doit confirmer :

- l’ouverture sans Terminal ;
- la détection sur stockage interne ou microSD ;
- l’installation, puis le choix du français dans le jeu ;
- la détection correcte après fermeture et réouverture de l’application ;
- la restauration de l’original, suivie d’une vérification Steam réussie.

Une VM Manjaro KDE x86-64 peut servir à contrôler l’interface et une installation
de test : UTM sur Mac Apple Silicon, ou VMware/VirtualBox sur PC. Elle sera plus
lente sur un Mac ARM, mais suffit pour ce parcours. Un PC AMD peut aussi utiliser
SteamOS sur un disque de test dédié, jamais sur le disque principal.

Ces simulations ne remplacent pas la validation matérielle recommandée par
Valve.

[Signaler un problème Steam Deck](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=installation.yml)
· [Recommandations Valve](https://partner.steamgames.com/doc/steamhardware/steamdeck/faq)
· [Installer SteamOS](https://help.steampowered.com/en/faqs/view/65B4-2AA3-5F37-4227)
