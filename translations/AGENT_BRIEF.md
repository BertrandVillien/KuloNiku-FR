# Brief compact pour les agents de traduction

## Univers et ton

KuloNiku: Bowl Up! est un jeu chaleureux de cuisine et de gestion, avec humour,
caractères hauts en couleur et moments plus émouvants. Le joueur ou la joueuse
hérite de **Bakuso**, le restaurant de boulettes de viande autrefois célèbre de
sa grand-mère, dans la petite ville de **KuloNiku**. Il faut restaurer sa gloire,
servir les habitants, améliorer et décorer le restaurant, nouer des amitiés et
éclaircir les mystères du passé familial.

La rivale la plus visible est **Stella**, cheffe rock star de **Souper Starz**.
Les rivalités se règlent lors de **duels culinaires** (« Meatball Brawls » dans
la communication anglaise), jugés sur la technique, la stratégie et les demandes
du public. Les personnages peuvent être amis, rivaux, ou les deux.

Personnages et noms propres rencontrés : Stella, Mami, Ume, Rosso, Lado, Shuga,
Mr. Crois, Cassie, Noka, Dan, Mr. Chu, Elio, Runa, Nekora, Tyro, Chil et Sai.
Ne pas franciser les noms propres sans preuve explicite dans les autres langues.

## Niveau d’adaptation attendu

- Produire un français naturel de jeu vidéo, comme une localisation officielle,
  et non un calque mot à mot.
- Préserver la voix du personnage visible dans le lot : registre, énergie,
  hésitations, humour, arrogance, tendresse et jeux de mots.
- Comparer systématiquement les huit langues du fichier source. L’indonésien
  éclaire souvent les plats et la culture; l’espagnol, l’allemand et le portugais
  aident à lever les ambiguïtés; le chinois et le thaï peuvent confirmer le sens.
- Pour les plats indonésiens ou noms traditionnels, conserver le nom consacré
  lorsqu’il n’existe pas d’équivalent français exact. Ajouter une courte
  description seulement si l’interface et les autres langues le font déjà.
- Rechercher l’usage culinaire français en cas de doute réel. Préférer les sources
  institutionnelles, restaurateurs/spécialistes ou dictionnaires culinaires.
- Respecter le genre et le nombre induits par le contexte. Si le contexte reste
  insuffisant, choisir une formulation neutre ou marquer `provisional`.

## Contraintes inviolables

- Ne modifier que le fichier de sortie attribué.
- Ne jamais modifier `key` ni l’ordre des lignes.
- Préserver exactement variables et balises : `[X]`, `[NAME]`, `{0}`, `<br>`,
  `[COLOR=…]`, commandes de dialogue, ponctuation technique et retours à la ligne.
- Viser une longueur française inférieure ou égale à `max_source_chars` quand
  cela reste naturel. Un dépassement justifié est préférable à un contresens;
  l’expliquer brièvement dans `notes`.
- `status=reviewed` si la traduction est sûre; `status=provisional` si une
  validation en jeu, narrative ou culinaire reste nécessaire.
- Le fichier produit contient exactement : `key,fr,status,notes`.

## Terminologie déjà fixée

- Bakuso, KuloNiku, Souper Starz : noms propres inchangés.
- Settings → Paramètres; Gameplay → Jouabilité; Accessibility → Accessibilité.
- Main Menu → Menu principal; Resume → Reprendre; Paused → En pause.
- Meatball → Boulette lorsqu’il s’agit de l’ingrédient générique.
- Fish balls → Boulettes de poisson; rice vermicelli → Vermicelles de riz.
- Broth/soup base selon le contexte : Bouillon ou Soupe, ne pas uniformiser sans
  regarder la clé et les autres langues.
- Cozy Mode → Mode détente.

Le fichier de lot est volontairement le seul contexte textuel détaillé fourni.
Il contient toutes les traductions officielles disponibles pour ses seules clés.

Synopsis de référence : description officielle de KuloNiku: Bowl Up! publiée par
Gambir Studio et Raw Fury sur Steam, complétée par les textes multilingues extraits
de la version installée.
