# KuloNiku FR

**Patch français communautaire pour _KuloNiku: Bowl Up!_**

[Voir KuloNiku: Bowl Up! sur Steam](https://store.steampowered.com/app/3357960/KuloNiku_Bowl_Up/)
· [English version](README.en.md)

![Tests](https://github.com/BertrandVillien/KuloNiku-FR/actions/workflows/ci.yml/badge.svg)
![macOS testé](https://img.shields.io/badge/macOS-test%C3%A9-2ea44f)
![Windows testé](https://img.shields.io/badge/Windows-test%C3%A9-2ea44f)

![Accueil de KuloNiku: Bowl Up! traduit en français](docs/assets/kuloniku-fr-home.jpg)

KuloNiku FR permet de jouer en français à la démo et au jeu complet. Le projet
est gratuit, non officiel et ne contient aucun fichier complet du jeu.

## État du projet

- **macOS :** préversion disponible et testée sur Apple Silicon et Intel ;
- **Windows :** interface graphique testée avec le jeu complet ;
- **jeu :** version complète `1.1.1` testée sur macOS et Windows, démo `0.10.5`
  testée sur macOS ;
- **mises à jour :** les nouvelles phrases inconnues restent en anglais.

---

## Installer le patch

Rendez-vous sur la page des
[releases officielles](https://github.com/BertrandVillien/KuloNiku-FR/releases).
La note de chaque version indique clairement quel fichier télécharger et comment
l’ouvrir.

Sur Windows, téléchargez l’archive **Windows x64**, décompressez-la entièrement,
puis ouvrez **Installer KuloNiku FR.exe**. L’application détecte Steam et vous
guide pour installer, mettre à jour ou restaurer le patch. L’exécutable n’est
pas encore signé numériquement : Windows SmartScreen peut demander une
confirmation. Ne désactivez jamais votre antivirus pour l’ouvrir.

Sur macOS, téléchargez le DMG adapté à votre Mac, puis glissez **KuloNiku FR**
dans **Applications**. L’application propose les mêmes opérations.

Après l’installation, lancez le jeu depuis Steam et choisissez **Français** dans
les paramètres.

Vous souhaitez examiner ou modifier le code ? Consultez
[l’installation depuis les sources](docs/INSTALL_FROM_SOURCE.md).

### Et si macOS bloque la première ouverture ?

Essayez d’ouvrir l’application une fois, puis allez dans **Réglages Système >
Confidentialité et sécurité > Ouvrir quand même**. Il n’est pas nécessaire de
désactiver une protection du Mac ni d’utiliser le Terminal.

[Voir la procédure officielle d’Apple](https://support.apple.com/fr-fr/102445)

## Une installation facile à annuler

Avant de modifier le jeu, l’application effectue une simulation et crée une
sauvegarde vérifiée. Le bouton **Restaurer** permet de revenir au fichier
d’origine.

Le patch est reconstruit à partir de votre propre installation : aucun fichier
complet du jeu n’est téléchargé ou distribué.

[Lire les détails de sécurité](SECURITY.md) ·
[Comprendre le fonctionnement technique](docs/DISTRIBUTION.md)

---

## Une adaptation, pas une traduction mot à mot

Chaque ligne est comparée aux langues fournies avec le jeu, puis adaptée au
contexte et à la place disponible à l’écran. Une attention particulière est
portée aux plats indonésiens et aux voix des personnages. Toutes les traductions
sont arbitrées ; certains dépassements de longueur restent à contrôler
visuellement en jeu.

<p>
  <img src="docs/assets/kuloniku-fr-settings.jpg" width="49%" alt="Langue française sélectionnée dans les paramètres">
  <img src="docs/assets/kuloniku-fr-gameplay.jpg" width="49%" alt="Recette et tutoriel traduits en français">
</p>

## Participer

Pas besoin de savoir programmer. Vous pouvez :

- [proposer une correction française](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=translation.yml) ;
- [signaler un problème d’installation](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=installation.yml) ;
- joindre une capture pour montrer le contexte ou un texte trop long.

Ne joignez jamais un fichier du jeu ou une extraction complète. Pour contribuer
avec Git, Codex, Claude ou un autre agent, consultez le
[guide de contribution](CONTRIBUTING.md).

## Pourquoi ce projet ?

Je voulais découvrir KuloNiku, mais la quantité d’ingrédients, de recettes et de
termes culinaires en anglais freinait réellement mon expérience. J’ai commencé
par chercher une manière prudente de traduire la démo. Le résultat m’a convaincu
d’acheter le jeu complet au lieu d’abandonner. Cela montre aussi combien une
localisation peut aider de nouveaux joueurs à découvrir et soutenir un jeu.

J’ai construit ce projet avec Codex en gardant une règle simple : pouvoir
comprendre, vérifier et annuler chaque modification. Le patch ne se contente pas
d’injecter une traduction automatique. Chaque ligne a été reprise avec les
langues fournies par le jeu, sa place à l’écran et, lorsque c’était possible, le
contexte de la scène.

L’indonésien a été particulièrement précieux pour respecter l’origine du studio,
les plats et l’intention de certains dialogues. Les formulations françaises
cherchent à rester naturelles et assez courtes pour l’interface.

## Documentation

La [documentation du projet](docs/README.md) rassemble la FAQ, la compatibilité,
la qualité de la traduction et les informations techniques.

---

## Projet non officiel

_KuloNiku: Bowl Up!_, ses textes, visuels et marques appartiennent à leurs ayants
droit, notamment Gambir Studio et Raw Fury. Ce projet n’est ni affilié ni
approuvé par eux. Il sera retiré ou archivé à leur demande ou si une traduction
française officielle paraît.

## Autres traductions communautaires

D’autres communautés proposent leur propre traduction de KuloNiku :

- [patch coréen non officiel](https://github.com/killterm/Localization-KuloNikuBowlUp) ;
- [outil de traduction japonaise](https://steamcommunity.com/app/3357960/discussions/0/807974496347632869/) ;
- [traduction russe assistée par IA](https://boosty.to/ketsuneko/posts/5acd1b69-3ade-4a08-9319-95373059a4a6), proposée selon les conditions de son auteur.

KuloNiku FR a été réalisé indépendamment et n’a utilisé aucun fichier ni aucune
traduction provenant de ces projets. Ces liens sont proposés pour aider les
joueurs à trouver la communauté correspondant à leur langue.
