# Consignes du projet KuloNiku FR

- Parler français avec l’utilisateur.
- Ne jamais versionner ni distribuer un fichier original ou reconstruit du jeu.
- Conserver les gros artefacts Unity exclusivement sous `work/` ou `outputs/`.
- Avant tout remplacement dans une installation Steam, vérifier le SHA-256 exact
  du fichier source et prévoir une restauration testée.
- Toute installation commence par une simulation, puis crée une sauvegarde
  vérifiée avant écriture.
- Une version inconnue peut être acceptée seulement si la table I2 est lisible,
  que l’anglais existe et que des clés françaises correspondent; les nouvelles
  clés utilisent l’anglais.
- Pour chaque nouveau lot de traduction française, confier la traduction à un
  sous-agent borné. Il doit comparer toutes les langues extraites, utiliser la clé
  comme contexte, rechercher les ambiguïtés réelles et signaler les entrées à
  valider en jeu.
- Le sous-agent de traduction ne modifie que `translations/fr.csv` ou le fichier
  de lot explicitement désigné. L’agent principal valide le CSV, construit le
  patch et garde la responsabilité du test en jeu.
- Préserver à l’identique les variables, balises, retours à la ligne et marqueurs
  de mise en forme présents dans la source.
- Pour chaque lot automatique, comparer la longueur française au maximum observé
  dans toutes les langues source; raccourcir naturellement ou documenter le
  dépassement.
