# KuloNiku FR

**Mod / patch français communautaire pour _KuloNiku: Bowl Up!_**

[Voir ou acheter KuloNiku: Bowl Up! sur Steam](https://store.steampowered.com/app/3357960/KuloNiku_Bowl_Up/)

[English version](README.en.md)

![Tests](https://github.com/BertrandVillien/KuloNiku-FR/actions/workflows/ci.yml/badge.svg)
![macOS testé](https://img.shields.io/badge/macOS-test%C3%A9-2ea44f)
![Windows à valider](https://img.shields.io/badge/Windows-%C3%A0%20valider-f0ad4e)
![Démo et jeu complet](https://img.shields.io/badge/%C3%A9ditions-d%C3%A9mo%20%7C%20complet-6f42c1)

![Accueil de KuloNiku: Bowl Up! traduit en français](docs/assets/kuloniku-fr-home.jpg)

KuloNiku FR est un mod de traduction qui permet de jouer en français à la démo
et au jeu complet. Le projet est gratuit, non officiel et construit par la
communauté dans l’attente d’une éventuelle localisation française officielle.

## Pourquoi j’ai créé ce patch

Je voulais découvrir KuloNiku, mais la quantité d’ingrédients et de termes
culinaires en anglais freinait réellement mon expérience. J’ai d’abord cherché
un moyen sûr de traduire la démo. Le résultat m’a convaincu d’acheter le jeu
complet au lieu d’abandonner, ce qui illustre aussi l’intérêt d’une localisation
pour faire connaître le jeu aux francophones.

J’ai construit le projet avec Codex, en gardant chaque opération réversible :
extraction des textes, comparaison des langues, simulation, sauvegarde puis
injection. Le menu ne pouvant pas afficher une langue supplémentaire, le patch
remplace temporairement l’allemand et conserve l’anglais comme solution de
repli. Restaurer le jeu rend immédiatement l’allemand disponible.

L’adaptation française a été travaillée ligne par ligne avec les huit langues
du jeu, les clés techniques et le contexte disponible. L’indonésien a été
particulièrement utile pour respecter l’origine du studio et préciser certains
plats ; les termes délicats ont fait l’objet de recherches complémentaires.
Les formulations restent aussi proches que possible des longueurs déjà prévues
par le jeu afin de limiter les problèmes d’affichage.

## État du projet

- traduction de toutes les entrées textuelles utilisées par le jeu ;
- version complète `1.1.1` et démo `0.10.5` testées sur macOS ;
- moteur compatible macOS et Windows, test réel Windows encore nécessaire ;
- nouvelles phrases inconnues laissées en anglais après une mise à jour ;
- aucune donnée ou fichier complet du jeu distribué.

## Installation simple — bientôt disponible

Des installateurs autonomes pour **Windows** et **macOS** sont en cours de
validation. Ce sera la méthode recommandée : télécharger le paquet adapté depuis
la page [Releases](https://github.com/BertrandVillien/KuloNiku-FR/releases),
lancer l’installateur, vérifier la simulation affichée, puis confirmer.

La première release n’est pas encore publiée. En attendant, la méthode suivante
permet de tester le mod depuis les sources.

### Windows — validation en cours

Windows est traité en priorité dans la documentation, car il concerne la
majorité des joueurs. Un paquet technique est déjà construit automatiquement,
mais il n’est pas encore assez simple pour un novice : une vraie interface
graphique Windows reste à produire puis à tester sur un PC. Elle devra trouver
Steam et KuloNiku toute seule, privilégier le jeu complet à la démo et proposer
installation, mise à jour et restauration sans ligne de commande.

### Première ouverture sur macOS

L’application est signée localement par GitHub Actions, mais pas notariée par
Apple. Elle fonctionne sur les Mac Apple Silicon et Intel sans abonnement
développeur. Téléchargez-la uniquement depuis les
[releases officielles du projet](https://github.com/BertrandVillien/KuloNiku-FR/releases).

Si macOS refuse la première ouverture :

1. essayez d’ouvrir **KuloNiku FR** une fois ;
2. ouvrez **Réglages Système > Confidentialité et sécurité** ;
3. descendez jusqu’au message concernant KuloNiku FR, puis cliquez sur
   **Ouvrir quand même** ;
4. confirmez **Ouvrir**. Ce choix est mémorisé pour l’application.

Cette procédure est celle documentée par
[Apple](https://support.apple.com/fr-fr/102445). Il n’est pas nécessaire de
désactiver Gatekeeper ni de saisir une commande dans le Terminal.

L’installateur trouve automatiquement Steam, privilégie le jeu complet à la
démo et affiche un état simple. Le journal technique reste replié. Il ne propose
une mise à jour française que si l’empreinte des traductions est réellement
différente. Les futurs lots de traduction pourront être téléchargés et vérifiés
sans réinstaller l’application, sauf lorsqu’ils exigent une version plus récente
du moteur ; la vérification de GitHub sera active dès la première release.

## Installation depuis les sources

Cette méthode nécessite [Python](https://www.python.org/) et
[uv](https://docs.astral.sh/uv/). Elle restera disponible pour les personnes qui
souhaitent examiner ou modifier le code.

1. Fermez le jeu.
2. Installez les dépendances :

   ```sh
   uv sync
   ```

3. Lancez d’abord la simulation, qui ne modifie rien.

   Sous Windows :

   ```powershell
   uv run kuloniku-fr install "C:\Program Files (x86)\Steam\steamapps\common\KuloNiku"
   ```

   Sous macOS :

   ```sh
   uv run kuloniku-fr install "/chemin/vers/KuloNiku.app"
   ```

4. Si le diagnostic est correct, installez le mod en ajoutant `--apply` à la
   même commande. Exemple macOS :

   ```sh
   uv run kuloniku-fr install "/chemin/vers/KuloNiku.app" --apply
   ```

5. Relancez le jeu depuis Steam et choisissez **Français** dans les paramètres.

Sous Windows, le chemin fourni doit être le dossier contenant
`KuloNiku_Data`.

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

Il faut être connecté à un compte GitHub gratuit pour afficher le formulaire.
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
