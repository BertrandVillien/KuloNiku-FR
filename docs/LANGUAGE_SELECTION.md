# Sélection de la langue française

## Décision pour la première version

L’installateur n’impose pas automatiquement la langue. Après installation,
l’utilisateur choisit « Français » dans les paramètres du jeu.

## Observation macOS en lecture seule

KuloNiku utilise les préférences Unity du domaine
`com.gambirstudio.kuloniku`. La clé `I2 Language` contient le nom interne de
l’emplacement sélectionné. Comme le patch réutilise l’emplacement allemand, la
valeur interne correspondant au français est actuellement `German`.

La démo et le jeu complet ont le même identifiant d’application et partagent
donc cette préférence. Une modification automatique affecterait les deux
installations qui coexistent.

## Condition avant automatisation

La fonction ne sera ajoutée que si le stockage Windows est vérifié sur une
installation réelle et si elle peut :

- sauvegarder la valeur précédente ;
- ne modifier que `I2 Language` ;
- fonctionner après installation comme une option explicite ;
- restaurer la valeur antérieure avec le patch ;
- ne jamais toucher aux sauvegardes de partie.

Sans ces garanties, la sélection manuelle reste plus simple et plus sûre.
