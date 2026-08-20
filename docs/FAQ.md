# Questions fréquentes

## Le patch fonctionne-t-il avec Steam ?

Oui. Il modifie uniquement la copie locale du jeu après une simulation et une
sauvegarde vérifiée. Le jeu se lance ensuite normalement depuis Steam.

## Démo ou jeu complet ?

Les deux sont reconnus automatiquement. La version complète est la référence.
La démo `0.10.5` reçoit uniquement les exceptions nécessaires à son ancienne
version des textes.

## Pourquoi l’allemand disparaît-il ?

Le menu actuel masque une neuvième langue. Le patch réutilise donc l’emplacement
allemand et conserve l’anglais comme repli sûr. Restaurer le fichier original
rend immédiatement l’allemand au jeu.

## Pourquoi le jeu passe-t-il en allemand après la restauration ?

Lorsque vous choisissez **Français**, le jeu mémorise en réalité l’emplacement
interne de l’allemand. Restaurer ou désinstaller le patch remet les textes
allemands, mais ne change pas cette préférence : l’interface peut donc apparaître
en allemand au lancement suivant.

C’est normal et cela n’affecte pas votre sauvegarde. Ouvrez les paramètres du jeu
et choisissez simplement la langue souhaitée.

## Que se passe-t-il après une mise à jour Steam ?

Steam peut remettre un fichier original ou nouveau. La commande `status`
relit le vrai fichier, contrôle la présence du français et compare son SHA-256 ;
elle ne se fie pas seulement à une date ou à un numéro enregistré localement.
L’installateur refait alors une simulation sur la nouvelle version avant toute
écriture.

## Dois-je retélécharger l’application pour chaque correction française ?

Non. L’application peut télécharger et vérifier le petit lot de traduction
publié sur GitHub. Elle demande seulement une nouvelle version complète si ce
lot déclare avoir besoin d’un moteur plus récent.

## Une nouvelle phrase peut-elle casser le jeu ?

Les traductions sont liées à l’empreinte des textes anglais et indonésien. Si
leur sens change, l’ancienne version française n’est pas injectée : l’anglais
installé reste affiché jusqu’à la prochaine traduction.

## Puis-je annuler ?

Oui. Chaque installation crée d’abord une sauvegarde dont l’empreinte SHA-256
est vérifiée. La commande ou le lanceur « Restaurer KuloNiku » remet cette
sauvegarde.

## Pourquoi macOS affiche-t-il parfois un avertissement ?

La préversion macOS n’est pas notariée par Apple. Ne contournez jamais un
avertissement pour un fichier obtenu ailleurs que dans les releases officielles
du projet. La procédure d’ouverture sûre est indiquée dans la note de release.

## Mon antivirus Windows réagit : que faire ?

N’ajoutez pas d’exclusion générale. Fermez le programme, conservez l’alerte et
ouvrez un rapport d’installation avec la version téléchargée, son empreinte et
une capture. Le code et la fabrication des paquets sont publics.

## Comment proposer une meilleure formulation ?

Utilisez le formulaire GitHub
[« Proposer une correction française »](https://github.com/BertrandVillien/KuloNiku-FR/issues/new?template=translation.yml).
Aucune
connaissance de Git n’est nécessaire. Indiquez le contexte et, si possible, une
capture limitée à l’écran concerné.

## Le projet continuera-t-il si le français devient officiel ?

Le patch n’a pas vocation à concurrencer une traduction officielle. Il pourra
être archivé comme outil et comme base technique pour d’autres communautés.
