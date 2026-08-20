#!/bin/bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 /path/to/KuloNiku-FR /path/to/package" >&2
  exit 2
fi

patcher="$1"
package_dir="$2"
app="$package_dir/KuloNiku FR.app"
contents="$app/Contents"
macos="$contents/MacOS"
resources="$contents/Resources"

if [[ ! -x "$patcher" ]]; then
  echo "Le moteur est absent ou non exécutable : $patcher" >&2
  exit 1
fi

mkdir -p "$macos" "$resources/translations"

swiftc \
  -O \
  -framework Cocoa \
  packaging/macos/KuloNikuFRLauncher.swift \
  -o "$macos/KuloNiku FR"

cp packaging/macos/Info.plist "$contents/Info.plist"
cp packaging/icons/KuloNikuFR.icns "$resources/KuloNikuFR.icns"
version="$($patcher --version | awk '{print $2}')"
plutil -replace CFBundleShortVersionString -string "$version" "$contents/Info.plist"
plutil -replace CFBundleVersion -string "$version" "$contents/Info.plist"
cp "$patcher" "$resources/KuloNiku-FR"
cp translations/fr.csv translations/source-hashes.csv translations/demo-overrides.csv translations/known-sources.json "$resources/translations/"
cp translations/NOTICE.md "$resources/translations/"
cp README.md LICENSE SECURITY.md THIRD_PARTY_NOTICES.md "$resources/"

chmod +x "$macos/KuloNiku FR" "$resources/KuloNiku-FR"
codesign --force --deep --sign - "$app"
codesign --verify --deep --strict "$app"

echo "Application créée : $app"
