# Tester KuloNiku FR sur Steam Deck

> **Mission :** installer le français, vérifier quelques écrans, puis tester la
> restauration. Comptez environ **10 à 15 minutes**. Aucun compte GitHub ni
> Terminal n’est nécessaire.

## 1. Préparer le jeu

- Mettez SteamOS à jour.
- Installez la démo ou le jeu complet depuis Steam.
- Lancez le jeu une fois sans le patch, atteignez le menu principal, puis
  quittez-le.

## 2. Ouvrir l’installateur

1. Passez en **mode Bureau** : **Steam > Marche/Arrêt > Passer en mode Bureau**.
2. [Téléchargez l’AppImage](https://github.com/BertrandVillien/KuloNiku-FR/releases/download/steam-deck-1.3.0-beta.1/KuloNiku-FR-Steam-Deck-x86_64.AppImage).
3. Dans **Dolphin > Téléchargements**, faites un clic droit sur le fichier.
4. Ouvrez **Propriétés > Permissions** et cochez **Est exécutable**.
5. Double-cliquez sur l’AppImage, puis choisissez **Lancer** si demandé.

## 3. Installer le français

1. Attendez l’état **Prêt à installer le français**.
2. Prenez une première capture de l’application.
3. Cliquez sur **Installer le français** et confirmez.
4. Après le message de réussite, cliquez sur **Revérifier**. L’application doit
   afficher **Installation propre et à jour**.

![Installateur prêt à appliquer le patch](assets/kuloniku-fr-linux-installer.png)

Si le jeu n’est pas trouvé, cliquez sur **Changer…** et choisissez son dossier,
celui qui contient `KuloNiku_Data`.

## 4. Vérifier dans le jeu

1. Fermez l’installateur et revenez en mode Jeu avec **Return to Gaming Mode**.
2. Lancez KuloNiku depuis Steam.
3. Dans les paramètres de langue, choisissez **Français**.
4. Regardez rapidement le menu principal, un tutoriel, une recette et un
   dialogue.
5. Quittez et relancez le jeu : le français doit rester sélectionné.

## 5. Tester la restauration

1. Quittez le jeu et repassez en mode Bureau.
2. Rouvrez l’AppImage et cliquez sur **Restaurer l’original**.
3. Cliquez sur **Revérifier** : l’application doit de nouveau proposer
   **Installer le français**.
4. Lancez brièvement le jeu pour vérifier qu’il fonctionne toujours.
5. Réinstallez ensuite le français et faites un dernier essai.

## Captures demandées

Une seule capture est obligatoire : **la fenêtre de l’installateur**, idéalement
avec l’état **Installation propre et à jour**.

Si possible, prenez aussi une capture après chaque grande étape :

- installateur prêt ;
- installation réussie ;
- menu du jeu en français ;
- restauration réussie ;
- français réinstallé.

### Comment prendre les captures

- **En mode Bureau :** ouvrez le menu des applications, cherchez **Spectacle**,
  puis choisissez **Fenêtre active** ou **Zone rectangulaire**. Enregistrez en
  PNG dans **Images**.
- **En mode Jeu :** appuyez en même temps sur **Steam + R1**. Les captures sont
  visibles dans **Steam > Multimédia**.

Envoyez les images en PNG ou JPG par le même moyen que celui utilisé pour vous
transmettre ce guide (mail, messagerie, dossier partagé…). Aucun compte GitHub
n’est nécessaire. Avec les images, indiquez simplement :

- Steam Deck **LCD ou OLED** ;
- jeu complet ou démo ;
- stockage interne ou microSD ;
- ce qui a fonctionné ou bloqué.

Masquez votre nom de compte et vos chemins personnels. N’envoyez jamais un
fichier du jeu ou une sauvegarde créée par l’installateur.

## En cas de blocage

- **L’AppImage ne s’ouvre pas :** vérifiez que **Est exécutable** est coché.
- **Le jeu n’est pas trouvé :** utilisez **Changer…**.
- **Une erreur apparaît :** prenez une capture et arrêtez le test.
- **Le jeu ne démarre plus :** rouvrez l’AppImage et choisissez
  **Restaurer l’original**.

[Voir la préversion](https://github.com/BertrandVillien/KuloNiku-FR/releases/tag/steam-deck-1.3.0-beta.1)
· [Sélection de la langue française](LANGUAGE_SELECTION.md)
