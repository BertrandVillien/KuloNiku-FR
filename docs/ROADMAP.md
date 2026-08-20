# Feuille de route

## Fait

- extraction et réécriture exacte de la table I2 Localization ;
- injection française dans l’emplacement allemand reconnu par le menu ;
- repli anglais pour toute clé absente, y compris après mise à jour ;
- simulation, sauvegarde SHA-256, remplacement atomique et restauration ;
- détection macOS/Windows et Démo/Complet par la structure installée ;
- installation, apparition et sélection de `Français` validées sur la version
  complète macOS ;
- CSV de contexte local, contrôle des marqueurs et budget de caractères ;
- CI macOS Apple Silicon/Intel et Windows, application native macOS et
  fabrication des paquets autonomes sur GitHub Actions ;
- profil de compatibilité de la démo `0.10.5`, sans dupliquer la traduction
  complète et avec repli anglais si le texte source change ;
- commande d’état locale distinguant patch intact, fichier restauré, mise à
  jour Steam et lot de traduction local plus récent ;
- plan public, FAQ, formulaires de contribution, politique de sécurité et
  contrôle CI des artefacts privés/propriétaires ;
- protocole documenté pour séparer les releases du moteur et des traductions.
- interface macOS simplifiée avec détection Steam, journal technique repliable,
  état illustré et mise à jour directe sans restauration ;
- manifeste de release distinguant une vraie évolution des traductions d’une
  simple évolution du moteur ;
- paquet de traduction autonome, téléchargement automatique vérifié et version
  minimale du moteur déclarée ;
- détection d’un remplacement Steam par lecture du fichier réel et comparaison
  SHA-256, indépendamment de la date du manifeste.
- icône commune du mod, déclinée pour les applications macOS et Windows.

## À valider avant la première release publique

- test réel sur Windows ;
- interface graphique Windows novice, avec le même contrat d’état et les mêmes
  garanties que l’application macOS ;
- comportement après « Vérifier l’intégrité » et après une mise à jour Steam ;
- parcours réel de téléchargement autonome après publication d’une release ;
- rendu des accents et couverture de la police ;
- test novice de l’ouverture du paquet macOS non notarié ;
- autorisation du studio ou formulation finale concernant la traduction non
  officielle ;
- première release et manifeste vérifié, nécessaires pour rendre la recherche
  distante déjà implémentée effectivement observable ;
- licence ou autorisation explicite couvrant la redistribution du CSV français ;
- validation réelle des paquets autonomes macOS et Windows, puis publication de
  la première release ;
- test utilisateur du parcours novice complet sur macOS et conception de son
  équivalent graphique Windows ;
- vérification finale du README et des captures sur la page publique du dépôt.

Le workflow de paquetage prépare les artefacts, mais aucune release ne doit être
publiée tant que ces validations ne sont pas terminées.
