# Proposer des corrections ciblées

L’espace de relecture permet d’explorer la traduction française avec les huit
langues du jeu, les clés voisines, les catégories, les longueurs, les notes, le
glossaire et les informations de lore. Il n’est pas nécessaire de tout relire :
sélectionnez simplement les passages sur lesquels vous souhaitez intervenir.

Il est créé hors ligne depuis votre propre installation de KuloNiku. Les textes
sources restent sur votre ordinateur et ne sont jamais ajoutés au dépôt.

![Espace de relecture KuloNiku FR avec filtres, comparaison des langues et outils d’export](assets/kuloniku-fr-review-workspace.png)

## Créer l’espace de relecture

### Depuis l’application — recommandé

1. Ouvrez **KuloNiku FR** sur Windows ou macOS.
2. Laissez l’application détecter le jeu, ou sélectionnez-le avec **Changer…**.
3. Ouvrez **Options avancées**, puis cliquez sur **Réviser et corriger les traductions**.

L’espace est généré puis ouvert dans votre navigateur. Le jeu n’est pas modifié
et aucun texte n’est envoyé sur Internet.

Si KuloNiku FR est déjà installé, l’outil utilise automatiquement sa sauvegarde
originale vérifiée, sans modifier le jeu. En l’absence de sauvegarde, restaurez
d’abord l’original avec l’application.

### Depuis la ligne de commande

Pour travailler depuis le dépôt, installez les outils du projet en suivant le
guide [Installation depuis les sources](INSTALL_FROM_SOURCE.md), puis lancez à
la racine du dépôt :

```bash
uv run kuloniku-fr review-workspace "CHEMIN_DU_JEU" --open
```

`CHEMIN_DU_JEU` peut désigner l’application macOS, le dossier Windows du jeu ou
directement son fichier `resources.assets`.

Cette méthode crée `work/review-workspace/index.html`. Depuis l’application, le
fichier est placé dans les données locales de KuloNiku FR. Dans les deux cas, la
page fonctionne sans connexion et ne contacte aucun serveur.

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

## Tester les corrections dans le jeu

1. Dans l’espace de relecture, utilisez **Exporter les propositions**.
2. Revenez dans l’application KuloNiku FR.
3. Ouvrez **Options avancées**, cliquez sur **Importer mon fichier de correction** et choisissez
   `kuloniku-fr-propositions.csv`.
4. Confirmez après la simulation, puis lancez le jeu depuis Steam.

L’application vérifie que les propositions correspondent exactement à cette
version du jeu et que leurs variables et balises sont intactes. Elle prépare
ensuite une traduction locale de test, sans modifier les fichiers intégrés à
l’application.

Après le contrôle en jeu, vous pouvez tester un nouvel export, restaurer
l’original ou réinstaller la traduction publique. La sauvegarde originale reste
vérifiée pendant tout le parcours.

### Méthode manuelle depuis les sources

```bash
uv run kuloniku-fr prepare-review-test "CHEMIN_DU_JEU" kuloniku-fr-propositions.csv
uv run kuloniku-fr install "CHEMIN_DU_JEU" --translations work/review-test/fr.csv
uv run kuloniku-fr install "CHEMIN_DU_JEU" --translations work/review-test/fr.csv --apply
```

La deuxième commande est la simulation. N’utilisez `--apply` qu’après sa
réussite.

## Transmettre la relecture

**Exporter les propositions** produit un CSV limité aux formulations françaises
modifiées. Les propositions sont marquées comme provisoires afin qu’elles
soient encore contrôlées avant intégration.

Indiquez dans votre résumé les passages réellement vérifiés en jeu.

Après l’export, utilisez **Copier le résumé pour GitHub**, puis **Ouvrir une
issue GitHub**. Le formulaire dédié accepte le CSV des propositions et,
facultativement, le JSON de sélection.

Transmettez :

1. le fichier de sélection JSON, sans les textes sources ;
2. le CSV des propositions françaises ;
3. quelques captures du jeu pour les problèmes visuels ou narratifs.

Ne transmettez jamais `index.html`, un fichier du jeu, `work/context.csv` ou une
autre extraction multilingue.
