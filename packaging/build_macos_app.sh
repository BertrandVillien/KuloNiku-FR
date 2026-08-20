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
case "$(uname -m)" in
  arm64) patcher_name="KuloNiku-FR-arm64" ;;
  x86_64) patcher_name="KuloNiku-FR-x86_64" ;;
  *) echo "Architecture macOS non prise en charge : $(uname -m)" >&2; exit 1 ;;
esac
cp "$patcher" "$resources/$patcher_name"
cp translations/fr.csv translations/source-hashes.csv translations/demo-overrides.csv translations/known-sources.json "$resources/translations/"
cp translations/review-overrides.csv translations/AGENT_BRIEF.md translations/NOTICE.md "$resources/translations/"
cp docs/TERMINOLOGY.md "$resources/translations/TERMINOLOGY.md"
cp README.md LICENSE SECURITY.md THIRD_PARTY_NOTICES.md "$resources/"

chmod +x "$macos/KuloNiku FR" "$resources/$patcher_name"
codesign --force --deep --sign - "$app"
codesign --verify --deep --strict "$app"

echo "Application créée : $app"
