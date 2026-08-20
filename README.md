# KuloNiku FR

**Patch français communautaire pour _KuloNiku: Bowl Up!_**

[Voir ou acheter KuloNiku: Bowl Up! sur Steam](https://store.steampowered.com/app/3357960/KuloNiku_Bowl_Up/)

[English version](README.en.md)

![Tests](https://github.com/BertrandVillien/KuloNiku-FR/actions/workflows/ci.yml/badge.svg)
![macOS testé](https://img.shields.io/badge/macOS-test%C3%A9-2ea44f)
![Windows à valider](https://img.shields.io/badge/Windows-%C3%A0%20valider-f0ad4e)
![Démo et jeu complet](https://img.shields.io/badge/%C3%A9ditions-d%C3%A9mo%20%7C%20complet-6f42c1)

![Accueil de KuloNiku: Bowl Up! traduit en français](docs/assets/kuloniku-fr-home.jpg)

KuloNiku FR permet de jouer en français à la démo et au jeu complet. Le projet
est gratuit, non officiel et construit par la communauté dans l’attente d’une
éventuelle localisation française officielle.

## État du projet

- traduction de toutes les entrées textuelles utilisées par le jeu ;
- version complète `1.1.1` et démo `0.10.5` testées sur macOS ;
- moteur compatible macOS et Windows, test réel Windows encore nécessaire ;
- nouvelles phrases inconnues laissées en anglais après une mise à jour ;
- aucune donnée ou fichier complet du jeu distribué.

> Le patch utilise actuellement l’emplacement allemand du menu. Restaurer le
> jeu rend immédiatement l’allemand disponible.

## Installation simple — bientôt disponible

Des installateurs autonomes pour **macOS** et **Windows** sont en cours de
validation. Ce sera la méthode recommandée : télécharger le paquet adapté depuis
la page [Releases](https://github.com/BertrandVillien/KuloNiku-FR/releases),
lancer l’installateur, vérifier la simulation affichée, puis confirmer.

La première release n’est pas encore publiée. En attendant, la méthode suivante
permet de tester le patch depuis les sources.

## Installation depuis les sources

Cette méthode nécessite [Python](https://www.python.org/) et
[uv](https://docs.astral.sh/uv/). Elle restera disponible pour les personnes qui
souhaitent examiner ou modifier le code.

1. Fermez le jeu.
2. Installez les dépendances :

   ```sh
   uv sync
   ```

3. Lancez d’abord la simulation, qui ne modifie rien :

   ```sh
   uv run kuloniku-fr install "/chemin/vers/KuloNiku.app"
   ```

4. Si le diagnostic est correct, installez le patch :

   ```sh
   uv run kuloniku-fr install "/chemin/vers/KuloNiku.app" --apply
   ```

5. Relancez le jeu depuis Steam et choisissez **Français** dans les paramètres.

Sous Windows, indiquez le dossier contenant `KuloNiku_Data` à la place de
l’application macOS.

Pour restaurer la sauvegarde vérifiée créée automatiquement :

```sh
uv run kuloniku-fr restore "/chemin/vers/KuloNiku.app" --apply
```

## Pourquoi l’installation reste sûre

- simulation obligatoire avant écriture ;
- sauvegarde locale vérifiée par SHA-256 ;
- reconstruction depuis votre propre installation ;
- remplacement atomique et restauration simple ;
- contrôle des textes anglais et indonésien avant chaque injection ;
- repli anglais lorsqu’une mise à jour change ou ajoute une phrase.

## Une adaptation, pas une traduction mot à mot

Chaque ligne est étudiée avec les huit langues fournies par le jeu, sa clé
technique, le contexte de la scène et la place disponible à l’écran. L’anglais
reste la référence pour les faits et les règles ; l’indonésien éclaire la
culture, les plats et l’intention du studio. Les noms culinaires sont adaptés à
l’usage français plutôt que traduits par approximation.

<p>
  <img src="docs/assets/kuloniku-fr-settings.jpg" width="49%" alt="Langue française sélectionnée dans les paramètres">
  <img src="docs/assets/kuloniku-fr-gameplay.jpg" width="49%" alt="Recette et tutoriel traduits en français">
</p>

## Participer sans savoir programmer

Ouvrez directement le formulaire
[Proposer une correction française](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=translation.yml)
pour :

- proposer une meilleure formulation ;
- joindre une capture et expliquer le contexte ;
- signaler un texte trop long ou un problème d’installation.

La clé technique est facultative. Une fois le formulaire rempli, cliquez sur
**Submit new issue** : la proposition apparaîtra dans les tickets du projet et
pourra être discutée. Pour un problème d’installation, utilisez plutôt
[Signaler un problème d’installation](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=installation.yml).

Ne joignez jamais un fichier du jeu ou une extraction complète. Consultez
[CONTRIBUTING.md](CONTRIBUTING.md) pour contribuer avec Git ou avec un agent
comme Codex, Claude ou un autre outil.

Les autres communautés peuvent forker le moteur pour préparer leur propre
langue, sous réserve des droits du jeu et des traductions concernées.

## Documentation

- [Questions fréquentes](docs/FAQ.md)
- [Compatibilité et mises à jour](docs/UPDATES.md)
- [Qualité de la traduction](docs/QUALITY.md)
- [Terminologie française](docs/TERMINOLOGY.md)
- [Sécurité](SECURITY.md)
- [Cadre juridique et attribution](docs/LEGAL.md)

## Projet non officiel

_KuloNiku: Bowl Up!_, ses textes, visuels et marques appartiennent à leurs
ayants droit, notamment Gambir Studio et Raw Fury. Ce projet n’est ni affilié ni
approuvé par eux. Il ne distribue aucun fichier complet du jeu et sera retiré ou
archivé à leur demande ou si une traduction française officielle paraît.
