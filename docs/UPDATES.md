# Mises à jour du jeu, des traductions et de l’installateur

Ce document couvre l’application macOS actuelle, la future interface Windows,
leur moteur de patch commun et les petits lots de traduction téléchargeables
séparément. Le projet distingue trois versions indépendantes.

| Axe | Exemple | Action |
|---|---|---|
| Jeu Steam | table I2 ou fichier modifié | restaurer si nécessaire, simuler, puis repatcher |
| Traductions | nouveau lot français | télécharger le petit lot vérifié, puis mettre à jour directement |
| Application / moteur | nouvel installateur ou moteur de patch | informer, sans installation forcée |

## État local

`kuloniku-fr status CHEMIN_DU_JEU` compare :

- l’empreinte du fichier actuellement installé ;
- le manifeste de la dernière sauvegarde ;
- la présence du libellé français ;
- l’empreinte du lot de traduction local ;
- la version du moteur qui a effectué l’installation.

Il n’écrit rien. Une mise à jour Steam est signalée comme un fichier à simuler
et repatcher, jamais comme une invitation à écraser silencieusement le jeu.

## Contrat de release

Chaque tag publie les applications macOS/Windows, leurs empreintes SHA-256, un
lot autonome `KuloNiku-FR-translations.zip` et un petit
`update-manifest.json`. Celui-ci contient une empreinte distincte pour la
traduction du jeu complet et celle de la démo, l’empreinte du téléchargement et
la version minimale du moteur capable de l’appliquer.

L’application interroge la dernière release GitHub. Si l’empreinte de
traduction de l’édition détectée diffère, elle télécharge automatiquement le
petit lot, contrôle son SHA-256, l’ouvre dans un cache utilisateur puis demande
au moteur de confirmer son empreinte logique avant de le proposer. Le jeu n’est
jamais patché sans confirmation.

Si le lot demande un moteur plus récent, aucun fichier n’est appliqué et le
bouton conduit à la release complète. Une évolution du moteur seul n’est donc
pas présentée comme une mise à jour française. Lorsque le moteur courant suffit,
la mise à jour du jeu est directe et conserve la sauvegarde originale ; aucune
restauration préalable n’est demandée.

## Activation

Le dépôt de référence est `BertrandVillien/KuloNiku-FR`. Le téléchargement et
ses contrôles sont branchés, mais GitHub renvoie actuellement « aucune release ».
Le parcours deviendra donc réellement observable lors de la première
publication taguée.

## Après une mise à jour Steam

Le manifeste local n’est pas pris comme preuve suffisante. À chaque ouverture,
le moteur relit la table du jeu, vérifie si le libellé français existe et calcule
le SHA-256 du véritable `resources.assets`. Si Steam remet un original ou une
nouvelle version, cette empreinte ne correspond plus ni au fichier patché ni à
l’original sauvegardé : l’état devient `game_updated` et une nouvelle simulation
est obligatoire avant de créer une nouvelle sauvegarde et de repatcher.

## Passage à une nouvelle version du jeu

1. conserver localement l’extraction de la version précédemment prise en charge ;
2. extraire la nouvelle table dans `work/` ;
3. exécuter `prepare-update-batches` ;
4. relire les clés ajoutées et celles dont l’anglais ou l’indonésien a changé ;
5. fusionner, propager les dialogues de secours identiques et lancer `lint` ;
6. régénérer `source-hashes.csv` ;
7. reconstruire puis réextraire afin de prouver l’égalité des valeurs attendues ;
8. tester visuellement avant de publier le lot de traduction.

Les clés retirées peuvent rester dans `fr.csv` : elles ne sont injectées que si
elles existent. La démo conserve ses anciennes formulations dans son seul
fichier d’exceptions plutôt que dans une deuxième traduction complète.

## Références de sécurité GitHub

- [API officielle des releases](https://docs.github.com/en/rest/releases/releases)
- [Téléchargement et empreintes des assets](https://docs.github.com/en/rest/releases/assets)
- [Vérification de l’intégrité d’une release](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/verify-release-integrity)
