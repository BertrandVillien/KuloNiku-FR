# Mises à jour du jeu, des traductions et du patcher

Le projet distingue trois versions indépendantes.

| Axe | Exemple | Action |
|---|---|---|
| Jeu Steam | table I2 ou fichier modifié | restaurer si nécessaire, simuler, puis repatcher |
| Traductions | nouveau lot français | télécharger le lot vérifié, puis restaurer et repatcher |
| Moteur | nouveau patcher | informer, sans installation forcée |

## État local

`kuloniku-fr status CHEMIN_DU_JEU` compare :

- l’empreinte du fichier actuellement installé ;
- le manifeste de la dernière sauvegarde ;
- la présence du libellé français ;
- l’empreinte du lot de traduction local ;
- la version du moteur qui a effectué l’installation.

Il n’écrit rien. Une mise à jour Steam est signalée comme un fichier à simuler
et repatcher, jamais comme une invitation à écraser silencieusement le jeu.

## Contrat de release proposé

Le dépôt GitHub définitif publiera deux canaux :

1. une release du moteur avec les exécutables macOS/Windows ;
2. une release de traduction, installable avec le moteur déjà présent.

Chaque lot de traduction devra contenir uniquement :

- `fr.csv` ;
- `source-hashes.csv` ;
- `demo-overrides.csv` ;
- un petit manifeste JSON donnant version, date, fichiers, tailles et SHA-256.

Le patcher téléchargera d’abord le manifeste depuis l’URL GitHub officielle,
affichera la version et demandera confirmation. Il vérifiera taille et SHA-256
avant de remplacer atomiquement son lot local. Il conservera le lot précédent
pour permettre un retour arrière. Aucun téléchargement ne modifiera directement
le jeu : le repatch restera une action séparée et confirmée.

Une nouvelle version du moteur sera seulement annoncée avec son lien de release.
Elle ne devra jamais être exécutée ou installée automatiquement.

## Ce qui reste à brancher

L’interrogation distante n’est volontairement pas codée tant que le compte,
l’URL finale du dépôt et le mode de publication ne sont pas fixés. Cela évite
d’inscrire un domaine provisoire dans un mécanisme de confiance. GitHub permet
ensuite de récupérer la dernière release et expose l’URL ainsi que l’empreinte
des assets de release.

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
