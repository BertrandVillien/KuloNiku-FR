# Plan de préparation publique

Ce document transforme le cahier de demandes du 20 août 2026 en tâches
versionnées. Il sert de source de vérité si le travail reprend dans une autre
conversation ou avec un autre agent.

## Priorité 1 — dépôt publiable et sûr

- [x] Vérifier que Git ne contient aucun fichier du jeu, texte source complet,
  chemin personnel, journal Codex ou artefact local.
- [x] Garder `work/`, `outputs/`, les fichiers Unity et les journaux locaux hors
  du dépôt.
- [x] Contrôler automatiquement à chaque CI les fichiers suivis et les chemins
  personnels courants.
- [x] Séparer clairement la licence du code de la traduction communautaire et
  rappeler que les droits du jeu restent à Gambir Studio et Raw Fury.
- [ ] Documenter la sauvegarde, la restauration, la simulation et la signature
  macOS afin que l'installation soit compréhensible et vérifiable.
- [ ] Faire vérifier le projet par l'éditeur avant une première publication
  largement diffusée.

## Priorité 2 — expérience GitHub

- [x] README français court, illustré par des captures réelles et doté de badges
  factuels.
- [x] README anglais équivalent.
- [x] FAQ courte : lancement Steam, sauvegarde, mises à jour, allemand remplacé,
  antivirus/macOS, démo et désinstallation.
- [x] Formulaire GitHub de correction accessible sans compétence technique,
  acceptant clé facultative, capture, texte vu, proposition et contexte.
- [x] Formulaire séparé pour les problèmes d'installation.
- [x] Guide de contribution expliquant le parcours débutant et le parcours avec
  agent IA.
- [ ] Demander de l'aide pour améliorer le français jusqu'à une localisation
  officielle et inviter les autres communautés à forker le moteur.
- [x] Ajouter une capture de la page d'accueil française de la version complète
  avant publication. Ne pas utiliser une capture marquée « Demo ».

## Priorité 3 — maintenance de la traduction

- [x] Faire de `translations/fr.csv` l'unique traduction principale.
- [x] Conserver la démo comme profil de compatibilité exceptionnel, sans copie
  complète concurrente.
- [x] Éviter les corrections partielles des dialogues de secours : corriger la
  clé principale puis régénérer les duplications identiques.
- [x] Documenter le brief de traduction, les voix, le lore, les priorités
  anglais/indonésien, le genre neutre, le tutoiement, les balises et les limites
  de longueur.
- [x] Documenter l'extraction locale du contexte multilingue sans publier les
  textes originaux du jeu.
- [x] Documenter le passage à une nouvelle version : ajouts, suppressions,
  modifications anglais/indonésien, lots compacts, fusion, empreintes et tests.

## Priorité 4 — mises à jour distribuées

- [x] Distinguer trois états : jeu repatché nécessaire, traduction plus récente
  disponible, moteur du patch plus récent disponible.
- [x] Détecter qu'une mise à jour Steam a restauré ou modifié
  `resources.assets`, puis proposer une nouvelle simulation.
- [ ] Permettre une mise à jour des seuls fichiers de traduction signés ou
  vérifiés, sans imposer une nouvelle release du moteur.
- [ ] Signaler une nouvelle release du moteur sans mise à jour forcée.
- [x] Ne jamais exécuter silencieusement un téléchargement ou une écriture dans
  le jeu ; présenter la version, la source et demander confirmation.
- [x] Prévoir le fonctionnement hors connexion avec les fichiers embarqués.

## Priorité 5 — confort optionnel

- [x] Rechercher où le jeu stocke la langue sélectionnée.
- [x] N'activer automatiquement le français que si la modification est locale,
  documentée, réversible et stable sur Mac et Windows.
- [x] Abandonner cette fonction si elle exige de modifier une sauvegarde, le
  registre de façon fragile ou un format propriétaire incertain.

Décision actuelle : sélection manuelle pour la première release. macOS utilise
une préférence Unity simple, mais la démo et le jeu complet la partagent ; le
stockage Windows doit être vérifié avant toute automatisation réversible.

## Recherche juridique et diffusion

- [ ] Identifier les conditions officielles de Raw Fury/Gambir Studio utiles
  aux mods et contenus communautaires.
- [x] Comparer les précautions du patch coréen sans recopier ses fichiers.
- [x] Préparer un message bref à l'éditeur : but non commercial, aucun asset
  distribué, achat déclenché par la démo traduite, retrait possible sur demande.
- [x] Documenter les limites : marque, textes du jeu, captures, absence
  d'affiliation, absence de garantie et demande de retrait.
- [x] Étudier les Guides Steam, les discussions et le Workshop uniquement selon
  les fonctions réellement activées pour le jeu.

## Décisions déjà prises

- Le patch remplace techniquement l'emplacement allemand, car une neuvième
  langue est masquée par le menu du jeu.
- L'anglais installé reste le repli sûr.
- Les empreintes anglais/indonésien empêchent l'injection d'une traduction dont
  le sens source a changé.
- La version complète est la référence ; la démo `0.10.5` utilise seulement ses
  exceptions.
- Aucun `resources.assets`, texte source multilingue complet ou journal Codex ne
  doit être publié.
- Le patch doit disparaître comme solution active si le français devient
  officiel, tout en pouvant rester archivé comme outil et base de fork.

## Questions à trancher avec le mainteneur

- [x] Dépôt GitHub privé créé sous `BertrandVillien/KuloNiku-FR` ; passage en
  public à confirmer après autorisation et validations.
- Adresse ou canal public à utiliser pour contacter Raw Fury/Gambir Studio.
- Licence souhaitée pour les traductions françaises si elle doit différer de la
  licence MIT du code.
- Capture française de la version complète à ajouter au README.
