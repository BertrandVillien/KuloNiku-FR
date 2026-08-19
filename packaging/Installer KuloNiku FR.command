#!/bin/zsh
set -u

base_dir="${0:A:h}"
patcher="$base_dir/KuloNiku-FR"
translations="$base_dir/translations/fr.csv"

print "Glissez ici KuloNiku.app, ou saisissez son chemin, puis validez :"
read -r game_path
game_path="${(Q)game_path}"

"$patcher" install "$game_path" --translations "$translations"
print ""
print -n "Installer après cette simulation ? Tapez O pour confirmer : "
read -r answer
if [[ "$answer" == [oO] ]]; then
  "$patcher" install "$game_path" --translations "$translations" --apply
else
  print "Aucune modification effectuée."
fi
print "Appuyez sur Entrée pour fermer."
read -r
