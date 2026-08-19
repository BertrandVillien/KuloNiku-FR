#!/bin/zsh
set -u

base_dir="${0:A:h}"
patcher="$base_dir/KuloNiku-FR"

print "Glissez ici KuloNiku.app, ou saisissez son chemin, puis validez :"
read -r game_path
game_path="${(Q)game_path}"

"$patcher" restore "$game_path"
print ""
print -n "Restaurer la sauvegarde ? Tapez O pour confirmer : "
read -r answer
if [[ "$answer" == [oO] ]]; then
  "$patcher" restore "$game_path" --apply
else
  print "Aucune modification effectuée."
fi
print "Appuyez sur Entrée pour fermer."
read -r
