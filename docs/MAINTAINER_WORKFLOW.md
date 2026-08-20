# Cycle de maintenance

Ce document s’adresse aux mainteneurs du dépôt. Il regroupe les opérations
internes qui ne sont pas nécessaires pour proposer une correction ordinaire.

## Préparer un lot de traduction

1. Extraire la version installée vers `work/context.csv` avec la commande
   `context`. Les langues et le budget de caractères y sont côte à côte.
2. Sélectionner un lot cohérent de clés : ingrédients, interface, tutoriel, etc.
3. Consulter `TERMINOLOGY.md` pour les choix déjà harmonisés.
4. Confier le lot borné à un agent en suivant `AGENT_WORKFLOW.md`.
5. Comparer la longueur française à `max_source_chars`. Documenter dans `notes`
   tout dépassement nécessaire.
6. Marquer chaque entrée `reviewed` ou `provisional`.
7. Exécuter les contrôles, construire un fichier de test et vérifier l’affichage
   en jeu.

## Dialogues dupliqués

Une même réplique peut exister sous une clé principale et plusieurs clés de
secours.

1. Corriger la clé principale dans `translations/review-overrides.csv`.
2. Exécuter `prepare-backups` pour propager les copies dont le texte source est
   strictement identique.
3. Faire relire séparément les variantes réellement différentes.
4. Fusionner, puis contrôler les variables et les balises.

## Lots assistés par agent

- Un agent reçoit uniquement le brief, son petit lot source et le nom de son
  fichier de sortie.
- Deux agents peuvent travailler en parallèle seulement sur des fichiers
  distincts dans `translations/batches/`.
- Le mainteneur vérifie le nombre de lignes, l’ordre, les clés, les marqueurs,
  les longueurs et les statuts avant la fusion.
- Les corrections transversales validées restent dans
  `translations/review-overrides.csv` afin d’être réappliquées après les lots.
- Les noms de plats traditionnels exigent une vérification de l’usage français.

## Contrôle final

- conserver exactement les clés, variables, balises et retours à la ligne ;
- vérifier les dépassements de longueur ;
- conserver les fichiers Unity sous `work/` ou `outputs/` ;
- ne jamais versionner un original ou un fichier reconstruit du jeu ;
- tester la simulation, la sauvegarde, l’installation et la restauration avant
  toute distribution.
