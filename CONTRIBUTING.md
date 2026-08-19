# Contribuer à la traduction

La source de travail publique est `translations/fr.csv`. Les traductions
originales du jeu sont extraites localement dans `work/` et ne sont pas
versionnées.

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
