# Distribution Mac et Windows

## Séparation des contenus

Le dépôt contient seulement :

- les outils d’extraction et de construction ;
- les traductions françaises ;
- les tests et les manifestes de compatibilité.

Les fichiers complets du jeu ne doivent pas être publiés. Une release contient
le patcher, `translations/fr.csv` et la documentation. Le patcher reconstruit le
fichier localement depuis la version installée; aucun binaire Unity n’est livré.

## Parcours utilisateur visé

1. Télécharger le paquet « KuloNiku FR » correspondant à Mac ou Windows.
2. Lancer un unique installateur.
3. L’installateur détecte Steam et le jeu.
4. Il analyse I2, affiche le SHA-256 et effectue d’abord une simulation.
5. Il conserve une sauvegarde récupérable du fichier original.
6. Il applique le correctif et vérifie le résultat.
7. Sur Mac seulement, il restaure une signature ad hoc valide de l’application.
8. Un bouton ou une commande « Restaurer » remet le fichier d’origine.

## Compatibilité adaptative

Chaque manifeste de release devra identifier au minimum :

- la version du jeu ;
- la plateforme (`macos` ou `windows`) ;
- le SHA-256 attendu du fichier original ;
- le SHA-256 du fichier reconstruit ;
- la version de la traduction.

Un hash inconnu n’est pas automatiquement rejeté : le patcher peut accepter une
version plus récente si la table I2 est intégralement lisible, que l’anglais
existe et que des clés françaises correspondent. Il affiche les clés nouvelles,
absentes et le nombre de replis anglais avant de demander `--apply`.

Il s’arrête sans écriture si la structure est ambiguë, si aucune clé ne
correspond ou si une validation échoue. Après une erreur d’installation, la
sauvegarde est restaurée automatiquement.

## Prototype actuel

Le test d’ajout d’une neuvième entrée `French (fr)` a montré que le menu du jeu
la masque. Le mode compatible conserve donc l’emplacement reconnu `German (de)`
et remplace uniquement son contenu et son libellé visible. Les textes absents de
`translations/fr.csv` utilisent l’anglais de la version locale comme repli.

## Inspiration et choix retenus

- Le patch coréen KuloNiku conserve l’emplacement anglais et en remplace le
  contenu. Cette comparaison a confirmé que le menu filtre les codes de langue.
- KuloNiku FR applique la même compatibilité sur l’emplacement allemand afin de
  préserver l’anglais comme langue source et comme repli.
- `pyI2L` valide le principe d’extraction/réinjection d’une table I2 et d’un CSV.
- KuloNiku FR conserve la simplicité, mais génère le patch localement, sauvegarde
  avant écriture et tolère les nouvelles clés grâce au repli anglais.
