# État de qualité de la traduction

Instantané du 20 août 2026, établi sur la démo macOS `v0.10.5`.

## Couverture

- 12 211 clés présentes dans la table de localisation.
- 12 196 traductions françaises.
- 15 clés sans français : elles sont également vides dans les huit langues
  officielles et utilisent donc le repli anglais vide.
- 12 181 traductions `reviewed`.
- 9 traductions `provisional`, toutes accompagnées d'une raison vérifiable en
  jeu.

## Contrôles réussis

- clés inconnues : 0 ;
- traductions vides dans le CSV français : 0 ;
- variables ou balises cassées : 0 ;
- tests automatisés : 9/9 ;
- reconstruction puis réextraction : 12 211 valeurs vérifiées, 0 divergence ;
- dialogues de secours identiques : 5 315 synchronisés automatiquement avec
  leur dialogue principal ;
- variantes de secours réellement différentes : 247 traduites séparément.

## Longueurs

La limite est un garde-fou heuristique : le maximum de caractères observé parmi
les huit langues officielles, pas la largeur réelle en pixels.

- 178 avertissements concernent les clés actives, dont 18 dépassements jugés
  importants ;
- 96 concernent les anciennes variantes de dialogues de secours, dont 8
  importants ;
- 1 731 concernent des sauvegardes strictement identiques, automatiquement
  synchronisées. Elles expliquent l'essentiel du total sans représenter 1 731
  textes français différents.

Une passe dédiée a raccourci 66 formulations sévères et économisé 1 199
caractères. Les dépassements conservés nécessiteraient de perdre du sens, une
voix de personnage, une relation ou un marqueur dynamique. Le test en jeu reste
la mesure décisive.

## Arbitrages éditoriaux

Les neuf entrées auparavant provisoires ont été arbitrées après le premier test
en jeu. Il ne reste plus aucune traduction marquée `provisional`. Les contrôles
visuels et les retours de partie restent néanmoins indispensables.

Les six règles de festival suivent désormais l'anglais et l'indonésien, qui
concordent sur deux ingrédients.
