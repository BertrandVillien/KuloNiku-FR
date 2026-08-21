# Distribution Windows, macOS et Steam Deck

## Séparation des contenus

Le dépôt contient seulement :

- les outils d’extraction et de construction ;
- les traductions françaises ;
- les tests et les manifestes de compatibilité.

Les fichiers complets du jeu ne doivent pas être publiés. Une release contient
le patcher, `translations/fr.csv` et la documentation. Le patcher reconstruit le
fichier localement depuis la version installée; aucun binaire Unity n’est livré.

L’icône utilisée par les installateurs se trouve dans
`packaging/icons/KuloNikuFR.png`. Sa source vectorielle publique
`packaging/icons/KuloNikuFR.svg` peut servir de base aux adaptations du mod dans
d’autres langues.

## Étapes de sécurité

Le moteur suit toujours le même enchaînement :

1. détecter Steam et le jeu ;
2. analyser la table I2 et effectuer une simulation ;
3. conserver une sauvegarde vérifiée du fichier original ;
4. appliquer le correctif et vérifier le résultat ;
5. restaurer une signature ad hoc valide sur macOS ;
6. permettre le retour au fichier d’origine.

## Moteur commun

Les interfaces macOS, Windows et Linux ne contiennent pas la logique de patch. Elles
utilisent la sortie JSON versionnée de `status --json` (`schema_version: 1`),
puis lancent les mêmes commandes de simulation, d’installation et de
restauration.

L’application macOS distribuée est universelle. Son lanceur contient les
architectures Apple Silicon et Intel, puis choisit automatiquement le moteur
correspondant inclus dans le même paquet.

La sauvegarde, la compatibilité et les mises à jour restent ainsi gérées au même
endroit, indépendamment de l’interface utilisée.

Sur Steam Deck, le moteur et l’interface PyInstaller sont réunis dans une
AppImage x86-64 autonome. Depuis la version `1.3.0`, elle est fabriquée avec les
paquets Windows et macOS et jointe aux releases stables.

L’AppImage ne demande ni installation système ni privilège administrateur. Les
sauvegardes sont placées dans le répertoire XDG de l’utilisateur, en dehors des
préfixes Proton. Le parcours Linux masque provisoirement la relecture, l’import
de corrections et les mises à jour intégrées.

## Compatibilité adaptative

Chaque manifeste de release indique au minimum :

- la version du jeu ;
- la plateforme (`macos` ou `windows`, y compris le jeu Windows lancé par Proton) ;
- le SHA-256 attendu du fichier original ;
- le SHA-256 du fichier reconstruit ;
- la version de la traduction.

Un hash inconnu n’est pas automatiquement rejeté : le patcher peut accepter une
version plus récente si la table I2 est intégralement lisible, que l’anglais
existe et que des clés françaises correspondent. Il affiche les clés nouvelles,
absentes et le nombre de replis anglais avant de demander `--apply`.

`translations/known-sources.json` ne contient pas les textes du jeu : il recense
seulement l’empreinte des tables déjà vérifiées. Une empreinte inconnue déclenche
une information douce dans l’interface, jamais un refus à elle seule.

Il s’arrête sans écriture si la structure est ambiguë, si aucune clé ne
correspond ou si une validation échoue. Après une erreur d’installation, la
sauvegarde est restaurée automatiquement.

## Versions réellement testées

- jeu complet `1.1.1` sur macOS et Windows ;
- branche bêta du jeu disponible le 20 août 2026 sur Windows ;
- jeu complet `1.1.1` sur Steam Deck ;
- démo `0.10.5` sur macOS et Steam Deck.

L’application Windows de KuloNiku FR a installé et utilisé correctement la
traduction avec la branche bêta du jeu lors de ce test.

## Pourquoi le patch remplace l’allemand

Le test d’ajout d’une neuvième entrée `French (fr)` a montré que le menu du jeu
la masque. Le mode compatible conserve donc l’emplacement reconnu `German (de)`
et remplace uniquement son contenu et son libellé visible. Les textes absents de
`translations/fr.csv` utilisent l’anglais de la version locale comme repli.

L’anglais est conservé comme langue source et comme repli pour les phrases
inconnues. La sélection manuelle de « Français » et le comportement après une
restauration sont détaillés dans
[Sélection de la langue française](LANGUAGE_SELECTION.md).
