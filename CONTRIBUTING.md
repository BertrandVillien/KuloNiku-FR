# Contribuer à la traduction

La source de travail publique est `translations/fr.csv`. Les traductions
originales du jeu sont extraites localement dans `work/` et ne sont pas
versionnées.

## Sans savoir programmer

Le moyen le plus simple est d’ouvrir le formulaire GitHub « Proposer une
correction française ». Il suffit d’indiquer le texte vu, le contexte et une
proposition. Une capture est recommandée pour montrer la place disponible et
le personnage qui parle. La clé technique est facultative.

Ne joignez jamais `resources.assets`, un fichier du jeu ou une extraction
complète. Une capture limitée à l’écran concerné et une courte citation sont
suffisantes.

## Cycle d’un lot

1. Extraire la version installée vers `work/context.csv` avec la commande
   `context` : toutes les langues et le budget de caractères y sont côte à côte.
2. Sélectionner un lot cohérent de clés : ingrédients, interface, tutoriel, etc.
   Consulter aussi `docs/TERMINOLOGY.md` pour les choix déjà harmonisés.
3. Faire traduire ce lot par un sous-agent en lui fournissant les huit langues.
4. Utiliser la clé, les langues et le contexte en jeu pour lever les ambiguïtés.
5. Comparer la longueur française à `max_source_chars`. Dépasser seulement si
   une formulation plus courte perdrait le sens, puis l’expliquer dans `notes`.
6. Marquer chaque entrée :
   - `reviewed` : traduction suffisamment sûre ;
   - `provisional` : validation visuelle ou narrative encore nécessaire.
7. Exécuter `lint`, construire un fichier de test et vérifier l’affichage en jeu.
8. Corriger puis valider le lot avant de passer au suivant.

## Dialogues dupliqués

Une même réplique peut exister sous une clé principale et plusieurs clés de
secours. Il ne faut pas les corriger séparément au hasard :

1. corriger la clé principale dans `translations/review-overrides.csv` ;
2. exécuter `prepare-backups` pour propager les copies dont le texte source est
   strictement identique ;
3. ne faire relire que les variantes réellement différentes ;
4. fusionner puis contrôler les variables et balises.

Cette règle évite qu’une correction ne soit visible dans une scène mais pas
dans sa variante.

## Colonnes du CSV français

- `key` : identifiant I2 Localization, jamais traduit ;
- `fr` : texte français injecté ;
- `status` : `reviewed` ou `provisional` ;
- `notes` : justification courte seulement si elle apporte du contexte.

## Règles importantes

- Ne jamais altérer les clés, variables (`{0}`, `{PLAYER_COLOR}`, etc.), balises
  ou codes de mise en forme.
- Éviter la traduction littérale lorsqu’une autre langue éclaire mieux le sens.
- Ne pas introduire de typographie française qui risque de casser une variable
  ou une limite d’interface sans validation visuelle.
- Ne pas publier `resources.assets`, même modifié.
- Ne pas publier `work/context.csv` ni les colonnes complètes extraites du jeu.

## Contexte communautaire sans redistribuer le jeu

Le dépôt peut conserver une note courte et originale : type d’écran, personnage,
recette, intention, contrainte visuelle et validation en jeu. Les textes complets
des autres langues restent locaux et sont régénérés par chaque contributeur
possédant la démo ou le jeu.

Une pull request doit indiquer le lot, la version testée et les observations
utiles, sans joindre de fichier original du jeu.

## Lots automatisés

- Un agent ne reçoit aucun historique de conversation : seulement le brief et
  son fichier source compact.
- Deux agents peuvent travailler en parallèle uniquement sur deux fichiers
  distincts dans `translations/batches/`.
- L’agent principal vérifie le nombre de lignes, l’ordre, les clés, les marqueurs,
  les longueurs et les statuts avant de fusionner.
- Les corrections transversales validées vont dans
  `translations/review-overrides.csv`; la fusion les réapplique après les lots,
  ce qui conserve un historique clair sans modifier les sorties des agents.
- Les noms de plats traditionnels exigent une vérification d’usage en français;
  une translittération ou un nom indonésien ne doit jamais être « traduit » par
  approximation.

## Contributions assistées par IA

Codex, Claude ou un autre agent peuvent aider, mais leur sortie n’est jamais
acceptée sans contrôle. Fournissez seulement le brief versionné
`translations/AGENT_BRIEF.md` et un lot compact contenant les clés concernées.
Ne transmettez ni historique privé, ni journal de conversation, ni extraction
complète du jeu.

Le contributeur reste responsable de comparer les langues, de vérifier les
variables, d’expliquer les dépassements de longueur et de signaler ce qui n’a
pas été vu en jeu. Le protocole détaillé se trouve dans
`docs/AGENT_WORKFLOW.md`.
