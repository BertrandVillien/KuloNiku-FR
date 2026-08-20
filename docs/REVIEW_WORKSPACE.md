# Proposer des corrections ciblées

L’espace de relecture permet d’explorer la traduction française avec les huit
langues du jeu, les clés voisines, les catégories, les longueurs, les notes, le
glossaire et les informations de lore. Il n’est pas nécessaire de tout relire :
sélectionnez simplement les passages sur lesquels vous souhaitez intervenir.

Il est créé hors ligne depuis votre propre installation de KuloNiku. Les textes
sources restent sur votre ordinateur et ne sont jamais ajoutés au dépôt.

## Créer l’espace de relecture

Installez d’abord les outils du projet en suivant le guide
[Installation depuis les sources](INSTALL_FROM_SOURCE.md), puis placez-vous à
la racine du dépôt.

Si KuloNiku FR est déjà installé, l’outil utilise automatiquement sa sauvegarde
originale vérifiée, sans modifier le jeu. En l’absence de sauvegarde, restaurez
d’abord l’original avec l’application.

```bash
uv run kuloniku-fr review-workspace "CHEMIN_DU_JEU" --open
```

`CHEMIN_DU_JEU` peut désigner l’application macOS, le dossier Windows du jeu ou
directement son fichier `resources.assets`.

L’outil crée `work/review-workspace/index.html` et l’ouvre dans votre
navigateur. Cette page fonctionne sans connexion et ne contacte aucun serveur.

## Explorer et sélectionner

Chaque clé présente :

- le français actuel et les huit langues officielles ;
- sa catégorie, son groupe et sa longueur de référence ;
- les clés voisines du même ensemble ;
- les décisions déjà documentées ;
- le lore des personnages détectés et le glossaire du projet.

Les couleurs, retours à la ligne, passages en gras et variables du jeu sont
interprétés dans les textes affichés. Le champ de proposition française reste
volontairement brut afin de conserver exactement ses balises et variables avant
l’export.

Les langues latines et l’indonésien sont dépliés par défaut. Les autres sont
regroupées dans une liste compacte sous la grille et peuvent être ouvertes
individuellement. Le navigateur mémorise automatiquement les langues affichées.
Sur ordinateur, survolez une langue pour voir son texte brut ; sur tout écran,
utilisez **Afficher le texte brut** pour basculer entre les deux lectures.

L’outil compare automatiquement les clés du jeu installé avec le fichier
français. Les traductions absentes, notamment après une mise à jour du jeu,
sont signalées dès l’ouverture.

Utilisez la vue **Liste** pour parcourir rapidement les textes, puis cliquez sur
une clé pour ouvrir sa fiche détaillée.

Les compteurs **sélectionnés** et **propositions** servent aussi de raccourcis :
cliquez dessus pour afficher directement leur fiche lorsqu’il n’y en a qu’une,
ou leur liste filtrée lorsqu’il y en a plusieurs.

Ajoutez seulement les passages utiles à votre sélection : **Proposer une
correction**, **Signaler une ambiguïté** ou **À vérifier en jeu**. Votre
sélection est enregistrée dans le navigateur.

Utilisez **Exporter ma sélection** pour conserver une copie JSON réimportable.
Le fichier reste lié à la version exacte des textes du jeu : une sélection
ancienne ne peut pas être importée par erreur dans une autre version.

## Transmettre la relecture

**Exporter les propositions** produit un CSV limité aux formulations françaises
modifiées. Les propositions sont marquées comme provisoires afin qu’elles
soient encore contrôlées avant intégration.

Après l’export, utilisez **Copier le résumé pour GitHub**, puis **Ouvrir une
issue GitHub**. Le formulaire dédié accepte le CSV des propositions et,
facultativement, le JSON de sélection.

Transmettez :

1. le fichier de sélection JSON, sans les textes sources ;
2. le CSV des propositions françaises ;
3. quelques captures du jeu pour les problèmes visuels ou narratifs.

Ne transmettez jamais `index.html`, un fichier du jeu, `work/context.csv` ou une
autre extraction multilingue.
