# Installer et tester KuloNiku FR sur Steam Deck

> **Bêta à valider sur un véritable Steam Deck.** L’AppImage actuelle a passé
> les tests automatiques et un essai complet en VM Linux avec Steam et Proton.
> Elle n’est pas encore incluse dans une release stable.

## Télécharger la bêta

La préversion est publique et ne demande pas de compte GitHub :

- [télécharger directement KuloNiku-FR-Steam-Deck-x86_64.AppImage](https://github.com/BertrandVillien/KuloNiku-FR/releases/download/steam-deck-1.3.0-beta.1/KuloNiku-FR-Steam-Deck-x86_64.AppImage) ;
- [télécharger son fichier de contrôle SHA-256](https://github.com/BertrandVillien/KuloNiku-FR/releases/download/steam-deck-1.3.0-beta.1/KuloNiku-FR-Steam-Deck-x86_64.AppImage.sha256) ;
- [consulter la préversion et ses notes](https://github.com/BertrandVillien/KuloNiku-FR/releases/tag/steam-deck-1.3.0-beta.1) ;
- [consulter la fabrication et ses contrôles](https://github.com/BertrandVillien/KuloNiku-FR/actions/runs/32386961308).

SHA-256 de `KuloNiku-FR-Steam-Deck-x86_64.AppImage` :
  `dc1454bc235652265f7b0336c2d26683312da511c55f6977c78ac5d2773baa8d`

La vérification de l’empreinte est facultative pour le parcours sans Terminal.
Un testeur qui souhaite la faire peut placer les deux téléchargements dans le
même dossier, ouvrir Konsole dans ce dossier et
lancer `sha256sum -c KuloNiku-FR-Steam-Deck-x86_64.AppImage.sha256`.

## Avant d’installer le patch

1. Utilisez le canal **Stable** de SteamOS et installez ses mises à jour.
2. Installez légalement la démo ou le jeu complet depuis Steam, sur le stockage
   interne ou sur une microSD formatée par le Steam Deck.
3. Attendez la fin complète du téléchargement et des mises à jour Proton.
4. Lancez une première fois le jeu **sans le patch**, atteignez le menu principal,
   puis quittez-le normalement. Cette étape permet de distinguer un problème du
   jeu ou de Proton d’un problème du patch.
5. Notez le modèle du Deck (LCD ou OLED), la version de SteamOS, l’édition testée
   (démo ou jeu complet) et l’emplacement du jeu (interne ou microSD).

N’ajoutez aucune option de lancement Steam. En particulier,
`PROTON_USE_WINED3D=1 %command%` était uniquement un contournement graphique pour
la VM VirtualBox et ne doit pas être utilisé sur un Steam Deck.

## Installer le français

1. Appuyez sur **Steam > Marche/Arrêt > Passer en mode Bureau**.
2. Ouvrez Firefox et utilisez le lien de téléchargement direct indiqué plus
   haut. Aucun compte GitHub n’est nécessaire.
3. Dans Dolphin, ouvrez **Téléchargements**.
4. Faites un clic droit sur l’AppImage, ouvrez **Propriétés >
   Permissions** et cochez **Est exécutable**.
5. Double-cliquez sur l’AppImage. Si Dolphin demande une confirmation, choisissez
   **Lancer**.
6. L’application recherche le jeu et lance automatiquement une simulation. Ne
   cliquez sur rien tant que **Vérification du jeu…** est affiché.
7. Vérifiez que l’écran indique **Jeu complet détecté · Steam** ou
   **Démo détectée · Steam**, puis **Prêt à installer le français**.
8. Cliquez sur **Installer le français** et confirmez. L’application crée et
   vérifie une sauvegarde SHA-256 avant de remplacer le fichier local.
9. Attendez le message de réussite, puis cliquez sur **Revérifier**. L’état doit
   indiquer que l’installation est propre et à jour.

![Installateur Linux prêt à appliquer le patch](assets/kuloniku-fr-linux-installer.png)

L’application détecte les bibliothèques du stockage interne et de la microSD.
Si elle ne trouve rien, utilisez **Changer…** et choisissez le dossier du jeu qui
contient `KuloNiku_Data`. Ne sélectionnez pas directement `resources.assets`.

## Vérifier dans le jeu

1. Fermez l’AppImage.
2. Revenez en mode Jeu avec **Return to Gaming Mode**.
3. Lancez KuloNiku normalement depuis sa fiche Steam.
4. Dans les paramètres de langue, choisissez **Français**. Le patch réutilise
   l’emplacement interne de l’allemand : voir
   [Sélection de la langue française](LANGUAGE_SELECTION.md).
5. Contrôlez au minimum le menu principal, les paramètres, un tutoriel, une
   recette et un dialogue.
6. Quittez puis relancez le jeu pour vérifier que la langue reste sélectionnée.

Le patch ne reste pas actif en arrière-plan et ne modifie pas Proton. Sur le
matériel réel, il ne doit donc provoquer aucune baisse de performances. Les
fortes lenteurs observées en VM venaient du rendu graphique logiciel de
VirtualBox.

## Tester la restauration et la réinstallation

Ce contrôle est obligatoire pour valider la bêta :

1. Quittez complètement le jeu et repassez en mode Bureau.
2. Rouvrez la même AppImage et attendez sa vérification.
3. Cliquez sur **Restaurer l’original**, puis confirmez. Une simulation de la
   restauration est effectuée avant l’écriture et la sauvegarde est revérifiée.
4. Cliquez sur **Revérifier**. L’application doit de nouveau proposer
   **Installer le français**.
5. Relancez brièvement le jeu et confirmez que l’état d’origine est fonctionnel.
6. Quittez le jeu, rouvrez l’AppImage et réinstallez le français.
7. Relancez enfin le jeu et confirmez que **Français** est de nouveau disponible.

Conservez l’AppImage pendant toute la bêta : elle permet de revérifier, mettre à
jour ou restaurer le patch. Une vérification des fichiers depuis Steam restaure
également les fichiers officiels, mais elle ne remplace pas le test du bouton de
restauration intégré.

## Si quelque chose ne fonctionne pas

- **L’AppImage ne s’ouvre pas :** vérifiez que **Est exécutable** est coché.
- **Le jeu n’est pas détecté :** vérifiez qu’il est entièrement installé, puis
  utilisez **Changer…** pour sélectionner le dossier contenant
  `KuloNiku_Data`.
- **La simulation échoue :** n’insistez pas et ne modifiez aucun fichier à la
  main. Ouvrez **Options avancées > Journal de logs** et joignez une capture du
  message.
- **Le jeu ne démarre plus :** restaurez l’original avec l’AppImage. Indiquez
  aussi si le jeu non patché avait réussi le contrôle préalable.
- **Le téléchargement échoue :** ouvrez la page de la préversion et utilisez
  l’asset qui se termine par `.AppImage`. Ne téléchargez pas une copie depuis un
  site tiers.

N’utilisez pas `sudo`, `pacman`, Protontricks ou Wine et ne désactivez pas le
mode lecture seule de SteamOS. L’AppImage ne demande aucune installation système.

## Compte rendu attendu

Le rapport doit préciser :

- Steam Deck LCD ou OLED, version de SteamOS et canal utilisé ;
- jeu complet ou démo, stockage interne ou microSD ;
- détection automatique ou sélection avec **Changer…** ;
- résultat de l’installation, du test en jeu, de la restauration et de la
  réinstallation ;
- éventuels textes trop longs, restés en anglais ou incorrects, avec captures.

Ne joignez jamais `resources.assets`, un autre fichier du jeu, une sauvegarde du
patch, un rapport de crash contenant des données personnelles ou vos
identifiants Steam.

[Signaler un problème Steam Deck](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=installation.yml)
· [FAQ officielle du mode Bureau Steam Deck](https://help.steampowered.com/en/faqs/view/671A-4453-E8D2-323C)
· [Informations officielles sur SteamOS et Proton](https://www.steamdeck.com/fr/software)
