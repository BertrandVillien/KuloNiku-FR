# Feuille de route

## Fait

- extraction et réécriture exacte de la table I2 Localization ;
- injection française dans l’emplacement allemand reconnu par le menu ;
- repli anglais pour toute clé absente, y compris après mise à jour ;
- simulation, sauvegarde SHA-256, remplacement atomique et restauration ;
- détection macOS/Windows et Démo/Complet par la structure installée ;
- CSV de contexte local, contrôle des marqueurs et budget de caractères ;
- CI macOS/Windows et fabrication de paquets autonomes sur GitHub Actions.

## À valider avant la première release publique

- installation, apparition et sélection de `Français` dans la version complète
  macOS ;
- test réel sur Windows ;
- comportement après « Vérifier l’intégrité » et après une mise à jour Steam ;
- rendu des accents et couverture de la police ;
- ouverture des paquets macOS non notariés et ergonomie des lanceurs ;
- autorisation du studio ou formulation finale concernant la traduction non officielle.

Le workflow de paquetage prépare les artefacts, mais aucune release ne doit être
publiée tant que ces validations ne sont pas terminées.
