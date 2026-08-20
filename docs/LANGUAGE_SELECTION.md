# Sélection de la langue française

## Fonctionnement actuel

L’installateur n’impose pas automatiquement la langue. Après installation,
l’utilisateur choisit « Français » dans les paramètres du jeu.

## Valeur enregistrée par le jeu

KuloNiku utilise les préférences Unity du domaine
`com.gambirstudio.kuloniku`. La clé `I2 Language` contient le nom interne de
l’emplacement sélectionné. Comme le patch réutilise l’emplacement allemand, la
valeur interne correspondant au français est actuellement `German`.

La démo et le jeu complet ont le même identifiant d’application et partagent
donc cette préférence.

## Après une restauration

La restauration remet les textes allemands d’origine sans modifier la préférence
`I2 Language`. Si « Français » était sélectionné, l’interface apparaît donc en
allemand au lancement suivant. Il suffit de choisir une autre langue dans les
paramètres. Les sauvegardes de partie ne sont pas concernées.
