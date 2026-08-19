# KuloNiku FR

Projet communautaire de traduction française de **KuloNiku: Bowl Up!**.

## État actuel

- Prototype validé techniquement sur la démo macOS `0.10.5`.
- Extraction confirmée de la table Unity `I2Languages` : 12 211 clés, 8 langues.
- Le menu du jeu n’accepte que huit emplacements codés. Le patch conserve
  techniquement l’emplacement allemand (`de`), l’affiche comme « Français » et
  y injecte le français. L’anglais de la version installée sert de repli.
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

La langue allemande redevient disponible dès la restauration du fichier
original. Cette contrainte pourra disparaître si le studio ouvre officiellement
le menu à de nouveaux codes de langue.

Les futures releases autonomes seront construites pour macOS et Windows avec
deux lanceurs simples : installer et restaurer. Leur état de validation est suivi
dans `docs/ROADMAP.md`.

## Traduction complète par lots

Le générateur exclut les textes déjà traduits et les sauvegardes de dialogues,
puis crée des lots thématiques limités par un budget de caractères :

```sh
uv run kuloniku-fr make-batches --character-budget 80000
```

Chaque sous-agent reçoit seulement `translations/AGENT_BRIEF.md` et un CSV sous
`work/translation-batches/source/`. Il écrit dans un fichier distinct sous
`translations/batches/`, ce qui permet deux traductions parallèles sans conflit.

Après validation des sorties :

```sh
uv run kuloniku-fr merge-batches
uv run kuloniku-fr lint work/lab/game/resources.assets translations/fr.csv
```

Les sauvegardes de dialogues identiques seront propagées depuis leur dialogue
principal; seules les variantes réelles feront l’objet de lots supplémentaires.
