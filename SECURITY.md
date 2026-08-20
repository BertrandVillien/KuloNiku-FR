# Sécurité

## Signaler un problème

N’ouvrez pas de ticket public si le problème peut permettre l’exécution de code,
le remplacement d’un fichier arbitraire, le contournement d’une vérification
d’empreinte ou l’usurpation d’une mise à jour.

Utilisez la fonction privée « Report a vulnerability » de l’onglet Security du
dépôt GitHub. L’URL exacte sera ajoutée quand le dépôt public sera créé.

Pour un faux positif antivirus sans détail exploitable, utilisez le formulaire
public de problème d’installation en indiquant la release, la plateforme et
l’empreinte du fichier, sans joindre de données personnelles.

## Modèle de confiance

- aucun fichier du jeu n’est distribué ;
- toute installation commence par une simulation ;
- la sauvegarde et les téléchargements sont vérifiés par SHA-256 ;
- les remplacements sont atomiques et restaurables ;
- une mise à jour distante ne doit jamais être exécutée automatiquement ;
- les paquets officiels proviennent uniquement des releases GitHub du projet.
