# Traduction assistée par agent

Ce document conserve le procédé reproductible sans dépendre d’une conversation
Codex particulière. Les journaux privés ne sont ni nécessaires ni publiables.

## Contexte minimal à fournir

Un agent reçoit seulement :

1. `translations/AGENT_BRIEF.md` ;
2. un CSV borné avec `key`, toutes les langues disponibles et
   `max_source_chars` ;
3. éventuellement une note de scène originale et courte ;
4. le nom exact de son unique fichier de sortie.

Il ne reçoit pas l’historique des autres agents. Les décisions durables sont
dans `docs/TERMINOLOGY.md`, jamais seulement dans une conversation.

## Mission type

> Traduis chaque ligne en français naturel, comme une localisation officielle.
> Compare toutes les langues, considère l’anglais comme référence des faits et
> l’indonésien comme référence culturelle et culinaire. Respecte la voix du
> personnage, le genre neutre du joueur, le tutoiement, les variables, balises
> et retours à la ligne. Vise `max_source_chars` sans sacrifier le sens. Modifie
> uniquement le CSV de sortie et marque `provisional` toute ambiguïté réelle.

## Contrat de retour

Le CSV produit contient exactement `key,fr,status,notes`, dans le même ordre.
L’agent termine par un résumé très court : nombre de lignes, entrées
provisoires, dépassements justifiés et doutes culinaires ou narratifs.

## Contrôle humain et automatique

- comparaison des clés et de leur ordre avec le lot source ;
- variables, balises et retours techniques identiques ;
- aucun `oe` remplacé par la ligature `œ` ;
- longueurs contrôlées ;
- terminologie déjà décidée respectée ;
- validation visuelle requise pour les écrans étroits ;
- correction transversale mise dans `review-overrides.csv`, puis propagation
  des dialogues de secours identiques.

Codex, Claude et d’autres agents peuvent suivre ce contrat. Le nom de l’outil ne
remplace ni les preuves multilingues ni la relecture en jeu.
