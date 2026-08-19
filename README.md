# KuloNiku FR

Projet communautaire de traduction française de **KuloNiku: Bowl Up!**.

## État actuel

- Prototype validé techniquement sur la démo macOS `0.10.5`.
- Extraction confirmée de la table Unity `I2Languages` : 12 211 clés, 8 langues.
- Le constructeur ajoute le français comme nouvelle langue et utilise l’anglais
  de la version installée pour chaque entrée encore non traduite.
- Aucun fichier original du jeu ne doit être versionné ou distribué dans ce dépôt.

## Principes

1. Les traductions françaises vivent dans `translations/fr.csv`.
2. Chaque traduction est relue à partir de toutes les langues disponibles et du
   contexte donné par sa clé.
3. Les fichiers Unity produits restent des artefacts locaux ou de publication,
   jamais des sources Git.
4. Toute installation doit proposer une sauvegarde et une restauration simples.

## Essai utilisateur sûr

Fermer le jeu, puis commencer par une simulation :

```sh
uv sync
uv run kuloniku-fr install "/chemin/vers/KuloNiku.app"
```

Si le diagnostic est bon, appliquer le patch :

```sh
uv run kuloniku-fr install "/chemin/vers/KuloNiku.app" --apply
```

Restaurer la dernière sauvegarde vérifiée :

```sh
uv run kuloniku-fr restore "/chemin/vers/KuloNiku.app" --apply
```

Sur Windows, donner le dossier qui contient `KuloNiku_Data`. Le même outil
détecte automatiquement macOS/Windows et Démo/Complet.

## Commandes de développement

```sh
uv sync
uv run kuloniku-fr inspect /chemin/vers/resources.assets
uv run kuloniku-fr extract /chemin/vers/resources.assets work/source.csv
uv run kuloniku-fr context /chemin/vers/resources.assets work/context.csv
uv run kuloniku-fr lint /chemin/vers/resources.assets translations/fr.csv
uv run kuloniku-fr build /chemin/vers/resources.assets translations/fr.csv work/resources.assets
```

`context` produit un tableau de travail avec toutes les langues et la longueur
maximale observée. Il reste dans `work/` car il contient les textes originaux du
jeu. Le dépôt public ne distribue que les traductions françaises et les outils.

## Compatibilité avec les mises à jour

Le patch est reconstruit depuis le `resources.assets` installé : il n’impose pas
un fichier provenant d’une ancienne version. Une version inconnue est acceptée
si sa table I2 est valide, contient l’anglais et reconnaît au moins une clé
française. Les nouvelles clés restent en anglais et les clés françaises devenues
absentes sont signalées.

Projet communautaire non officiel, sans affiliation avec Gambir Studio.

Les futures releases autonomes seront construites pour macOS et Windows avec
deux lanceurs simples : installer et restaurer. Leur état de validation est suivi
dans `docs/ROADMAP.md`.
