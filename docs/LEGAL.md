# Cadre juridique et attribution

Ce document décrit une démarche prudente ; il ne constitue pas un avis
juridique.

## Position recommandée avant publication

Le patcher est conçu pour ne distribuer ni `resources.assets`, ni table
multilingue extraite, ni contenu jouable du jeu. Il reconstruit localement le
fichier depuis une copie légalement installée, avec sauvegarde et repli. La
seule exception visuelle est l’icône de l’installateur, dérivée de l’icône du jeu
et marquée d’un macaron « FR » afin d’identifier clairement le mod. Elle demeure
la propriété de ses ayants droit et pourra être remplacée ou retirée sur simple
demande. Cette architecture réduit fortement ce qui est redistribué, mais ne
suffit pas à elle seule à autoriser la publication d’une traduction dérivée des
textes du jeu.

Le droit français réserve en principe la traduction et l’adaptation à l’auteur
ou à ses ayants droit. Les exceptions d’observation, sauvegarde et
interopérabilité des logiciels sont étroites et ne doivent pas être présentées
comme une permission générale de diffuser une localisation. L’accord écrit de
Gambir Studio/Raw Fury est donc recommandé avant une diffusion large.

- [Code de la propriété intellectuelle, article L122-4](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000006278911/2026-02-28)
- [Article L112-3 sur les traductions et adaptations](https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069414/LEGISCTA000006133323/2025-02-16/)
- [Articles relatifs aux logiciels, dont L122-6-1](https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069414/LEGISCTA000006133323/2024-05-28/)
- [Directive européenne 2009/24/CE](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=celex%3A32009L0024)

## Licences

La licence MIT du dépôt couvre uniquement le code et la documentation originale
du projet. Elle ne peut pas accorder des droits sur le jeu, ses textes, sa
marque ou ses assets. Tant qu’un ayant droit n’a pas autorisé une licence de
traduction précise, le dépôt ne doit pas affirmer que le texte français est
librement réutilisable.

Le patch coréen visible sur GitHub interdit modification et redistribution et
promet un retrait sur demande. Cela peut servir à garder une version centrale
et à limiter les variantes, mais ne remplace pas une autorisation de l’ayant
droit. L’absence de fichier de licence libre signifie également qu’un dépôt
visible n’est pas automatiquement open source.

- [Patch communautaire coréen observé](https://github.com/killterm/Localization-KuloNikuBowlUp)
- [Accord de souscription Steam](https://store.steampowered.com/subscriber_agreement/)

## Règles de publication proposées

- projet gratuit, non officiel et sans affiliation revendiquée ;
- aucun contenu jouable, police, binaire ou fichier reconstruit du jeu dans Git
  ou les releases ; l’icône d’identification documentée ci-dessus est la seule
  exception visuelle ;
- captures limitées à l’explication du projet et retirables sur demande ;
- crédits visibles à Gambir Studio et Raw Fury ;
- canal de contact et procédure de retrait publiés ;
- arrêt de la distribution active si une localisation française officielle
  paraît ou si un ayant droit le demande ;
- historique Git conservé uniquement si son contenu est lui-même distribuable.

## Contact avant publication

Le message doit demander explicitement l’autorisation de distribuer les seuls
CSV français et le patcher, préciser que le jeu reste obligatoire, et proposer
un accès préalable au dépôt. Le support public Raw Fury est indiqué sur leur
[page de confidentialité](https://rawfury.com/privacy-policy/). Il faudra
confirmer avec eux le bon interlocuteur avant l’envoi.
