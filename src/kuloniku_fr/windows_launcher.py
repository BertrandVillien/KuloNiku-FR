from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
from typing import Callable
import urllib.request
import webbrowser

from . import __version__


REPOSITORY_URL = "https://github.com/BertrandVillien/KuloNiku-FR"
RELEASES_API_URL = "https://api.github.com/repos/BertrandVillien/KuloNiku-FR/releases?per_page=1"
STEAM_APP_ID = "3357960"


def engine_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    return environment


def decode_engine_output(output: bytes) -> str:
    try:
        return output.decode("utf-8")
    except UnicodeDecodeError:
        return output.decode("cp1252", errors="replace")


def version_tuple(version: str) -> tuple[int, ...]:
    numbers = re.findall(r"\d+", version)
    return tuple(int(number) for number in numbers[:3])


def available_update_kind(
    manifest: dict,
    *,
    edition: str,
    bundled_translation_hash: str,
    current_version: str = __version__,
) -> str | None:
    if version_tuple(str(manifest.get("version", "0"))) > version_tuple(current_version):
        return "engine"
    remote_hash = manifest.get("translation_bundles", {}).get(edition)
    if remote_hash and remote_hash != bundled_translation_hash:
        return "translations"
    return None


def latest_release_from_payload(payload: object) -> dict | None:
    """Return GitHub's most recent published release, including prereleases."""
    if not isinstance(payload, list) or not payload or not isinstance(payload[0], dict):
        return None
    release = payload[0]
    if not isinstance(release.get("html_url"), str) or not isinstance(
        release.get("assets"), list
    ):
        return None
    return release


def parse_steam_library_paths(text: str) -> list[Path]:
    """Extract Steam library roots from either old or new VDF layouts."""
    paths: list[Path] = []
    for raw in re.findall(r'"path"\s+"((?:\\.|[^"\\])*)"', text, flags=re.IGNORECASE):
        decoded = raw.replace(r"\\", "\\")
        candidate = Path(decoded)
        if candidate not in paths:
            paths.append(candidate)
    return paths


def _registry_steam_roots() -> list[Path]:
    if os.name != "nt":
        return []
    import winreg

    roots: list[Path] = []
    keys = (
        (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", "InstallPath"),
    )
    for hive, key_name, value_name in keys:
        try:
            with winreg.OpenKey(hive, key_name) as key:
                value, _ = winreg.QueryValueEx(key, value_name)
        except OSError:
            continue
        candidate = Path(value)
        if candidate not in roots:
            roots.append(candidate)
    return roots


def steam_library_roots() -> list[Path]:
    roots = _registry_steam_roots()
    program_files = os.environ.get("PROGRAMFILES(X86)")
    if program_files:
        fallback = Path(program_files) / "Steam"
        if fallback not in roots:
            roots.append(fallback)

    for steam_root in list(roots):
        for relative in ("steamapps/libraryfolders.vdf", "config/libraryfolders.vdf"):
            configuration = steam_root / relative
            try:
                discovered = parse_steam_library_paths(
                    configuration.read_text(encoding="utf-8", errors="replace")
                )
            except OSError:
                continue
            for candidate in discovered:
                if candidate not in roots:
                    roots.append(candidate)
    return roots


def is_windows_game_folder(folder: Path) -> bool:
    try:
        assets = list(folder.glob("*_Data/resources.assets"))
    except OSError:
        return False
    return len(assets) == 1 and assets[0].is_file()


def installed_game_candidates(library_roots: list[Path] | None = None) -> list[Path]:
    """Find installed copies without recursively walking whole Steam libraries."""
    candidates: list[Path] = []
    for root in library_roots if library_roots is not None else steam_library_roots():
        steamapps = root / "steamapps"
        common = steamapps / "common"

        manifest = steamapps / f"appmanifest_{STEAM_APP_ID}.acf"
        try:
            manifest_text = manifest.read_text(encoding="utf-8", errors="replace")
            match = re.search(r'"installdir"\s+"([^"]+)"', manifest_text, re.IGNORECASE)
            if match:
                candidates.append(common / match.group(1).replace(r"\\", "\\"))
        except OSError:
            pass

        try:
            entries = list(common.iterdir())
        except OSError:
            continue
        candidates.extend(entry for entry in entries if "kuloniku" in entry.name.lower())

    unique: dict[str, Path] = {}
    for candidate in candidates:
        try:
            normalized = candidate.resolve()
        except OSError:
            normalized = candidate.absolute()
        if is_windows_game_folder(normalized):
            unique[os.path.normcase(str(normalized))] = normalized
    return sorted(
        unique.values(),
        key=lambda path: ("demo" in str(path).lower(), str(path).lower()),
    )


class LauncherPaths:
    def __init__(self, base: Path | None = None):
        if base is None:
            base = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path.cwd()
        self.base = base
        self.engine = base / "KuloNiku-FR.exe"
        self.translations = base / "translations" / "fr.csv"

    def validate(self) -> list[str]:
        missing = []
        if not self.engine.is_file():
            missing.append(str(self.engine))
        if not self.translations.is_file():
            missing.append(str(self.translations))
        return missing


class WindowsLauncher:
    def __init__(self, paths: LauncherPaths | None = None):
        import tkinter as tk
        from tkinter import ttk

        self.tk = tk
        self.ttk = ttk
        self.paths = paths or LauncherPaths()
        self.game: Path | None = None
        self.simulation_succeeded = False
        self.restore_available = False
        self.busy = False
        self.release_url: str | None = None
        self.update_check_started = False

        self.root = tk.Tk()
        self.root.title("KuloNiku FR")
        self.root.geometry("760x480")
        self.root.minsize(680, 440)
        try:
            self.root.iconbitmap(str(self.paths.base / "KuloNikuFR.ico"))
        except tk.TclError:
            pass

        style = ttk.Style(self.root)
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Status.TLabel", font=("Segoe UI", 15, "bold"))
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(18, 9))
        style.configure("Secondary.TButton", padding=(12, 7))

        outer = ttk.Frame(self.root, padding=24)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="KuloNiku FR", style="Title.TLabel").pack(anchor="w")

        status_frame = ttk.LabelFrame(outer, text=" État ", padding=18)
        status_frame.pack(fill="x", pady=(18, 0))
        status_row = ttk.Frame(status_frame)
        status_row.pack(fill="x")
        self.status_symbol = ttk.Label(status_row, text="●", font=("Segoe UI", 25), foreground="#c27c0e")
        self.status_symbol.pack(side="left", padx=(0, 14))
        status_text = ttk.Frame(status_row)
        status_text.pack(side="left", fill="x", expand=True)
        self.status_title = ttk.Label(status_text, text="Recherche de KuloNiku…", style="Status.TLabel")
        self.status_title.pack(anchor="w")
        self.status_message = ttk.Label(
            status_text,
            text="Recherche de l’installation Steam en cours.",
            wraplength=600,
            foreground="#505050",
        )
        self.status_message.pack(anchor="w", pady=(5, 0))

        game_row = ttk.Frame(outer)
        game_row.pack(fill="x", pady=(18, 12))
        self.game_label = ttk.Label(game_row, text="Aucun jeu sélectionné", foreground="#505050")
        self.game_label.pack(side="left", fill="x", expand=True)
        self.choose_button = ttk.Button(game_row, text="Changer…", command=self.choose_game)
        self.choose_button.pack(side="right")

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(2, 8))
        self.install_button = ttk.Button(
            actions,
            text="Installer le français",
            style="Primary.TButton",
            command=self.install_french,
            state="disabled",
        )
        self.install_button.pack(side="left")
        self.restore_button = ttk.Button(
            actions,
            text="Restaurer l’original",
            style="Secondary.TButton",
            command=self.restore_original,
            state="disabled",
        )
        self.restore_button.pack(side="left", padx=(10, 0))
        self.analyze_button = ttk.Button(
            actions,
            text="Revérifier",
            style="Secondary.TButton",
            command=self.analyze,
            state="disabled",
        )
        self.analyze_button.pack(side="right")

        self.details_button = ttk.Button(
            outer, text="Afficher les détails techniques ▸", command=self.toggle_details
        )
        self.details_button.pack(anchor="w", pady=(8, 0))
        self.details_frame = ttk.Frame(outer)
        self.log = tk.Text(
            self.details_frame,
            height=10,
            wrap="word",
            state="disabled",
            font=("Consolas", 9),
            background="#f5f5f5",
        )
        self.log.pack(fill="both", expand=True, pady=(6, 0))

        footer = ttk.Frame(outer)
        footer.pack(side="bottom", fill="x", pady=(12, 0))
        ttk.Label(footer, text=f"Version {__version__}", foreground="#707070").pack(side="left")
        self.release_button = ttk.Button(footer, text="Nouvelle version disponible", command=self.open_release)
        ttk.Button(footer, text="Projet GitHub", command=lambda: webbrowser.open(REPOSITORY_URL)).pack(side="right")
        ttk.Button(footer, text="À propos", command=self.show_about).pack(side="right", padx=(0, 8))

        self.root.after(80, self.select_default_installation)

    def set_status(self, title: str, message: str, kind: str = "warning") -> None:
        colors = {"good": "#188038", "info": "#1a73e8", "warning": "#c27c0e", "error": "#c5221f"}
        self.status_symbol.configure(foreground=colors[kind])
        self.status_title.configure(text=title)
        self.status_message.configure(text=message)

    def set_log(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.insert("1.0", text.strip())
        self.log.configure(state="disabled")

    def append_log(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.configure(state="disabled")

    def show_about(self) -> None:
        from tkinter import messagebox

        messagebox.showinfo(
            "À propos de KuloNiku FR",
            f"KuloNiku FR {__version__}\n\n"
            "Patch français communautaire non officiel.\n\n"
            "Aucun fichier complet du jeu n’est distribué. Le patch est construit "
            "localement depuis votre propre installation.",
        )

    def open_release(self) -> None:
        if self.release_url:
            webbrowser.open(self.release_url)

    def check_latest_release(self, edition: str, bundled_translation_hash: str) -> None:
        if self.update_check_started:
            return
        self.update_check_started = True

        def worker() -> None:
            try:
                headers = {
                    "Accept": "application/vnd.github+json",
                    "User-Agent": f"KuloNiku-FR/{__version__}",
                }
                request = urllib.request.Request(RELEASES_API_URL, headers=headers)
                with urllib.request.urlopen(request, timeout=8) as response:
                    release = latest_release_from_payload(json.load(response))
                if release is None:
                    return
                assets = release.get("assets", [])
                manifest_asset = next(
                    (asset for asset in assets if asset.get("name") == "update-manifest.json"),
                    None,
                )
                if not manifest_asset:
                    return
                manifest_request = urllib.request.Request(
                    manifest_asset["browser_download_url"], headers=headers
                )
                with urllib.request.urlopen(manifest_request, timeout=8) as response:
                    manifest = json.load(response)
                kind = available_update_kind(
                    manifest,
                    edition=edition,
                    bundled_translation_hash=bundled_translation_hash,
                )
                if kind:
                    self.root.after(
                        0,
                        lambda: self.show_available_update(
                            kind, str(manifest.get("version", "")), release["html_url"]
                        ),
                    )
            except Exception as error:
                self.root.after(
                    0,
                    lambda message=str(error): self.append_log(
                        f"\n\nVérification GitHub indisponible : {message}"
                    ),
                )

        threading.Thread(target=worker, daemon=True).start()

    def show_available_update(self, kind: str, version: str, release_url: str) -> None:
        self.release_url = release_url
        if kind == "engine":
            self.release_button.configure(text=f"Nouvel installateur {version}")
            message = f"Nouvelle version de l’installateur sur GitHub : {version}"
        else:
            self.release_button.configure(text="Nouvelles traductions sur GitHub")
            message = "Un nouveau lot de traductions est disponible sur GitHub."
        if not self.release_button.winfo_manager():
            self.release_button.pack(side="left", padx=(12, 0))
        self.append_log(f"\n\n{message}")

    def set_busy(self, busy: bool) -> None:
        self.busy = busy
        state = "disabled" if busy else "normal"
        self.choose_button.configure(state=state)
        self.analyze_button.configure(state=state if self.game else "disabled")
        if busy:
            self.install_button.configure(state="disabled")
            self.restore_button.configure(state="disabled")
        else:
            self.restore_button.configure(state="normal" if self.restore_available else "disabled")

    def toggle_details(self) -> None:
        if self.details_frame.winfo_manager():
            self.details_frame.pack_forget()
            self.details_button.configure(text="Afficher les détails techniques ▸")
            self.root.geometry("760x480")
        else:
            footer = self.details_button.master.winfo_children()[-1]
            self.details_frame.pack(fill="both", expand=True, before=footer)
            self.details_button.configure(text="Masquer les détails techniques ▾")
            self.root.geometry("760x680")

    def select_default_installation(self) -> None:
        missing = self.paths.validate()
        if missing:
            self.set_log("Fichiers manquants :\n" + "\n".join(missing))
            self.set_status(
                "Installateur incomplet",
                "Retéléchargez puis extrayez entièrement le paquet Windows.",
                "error",
            )
            return
        candidates = installed_game_candidates()
        if candidates:
            self.set_game(candidates[0])
            self.analyze()
        else:
            self.set_status(
                "KuloNiku est introuvable automatiquement",
                "Cliquez sur « Changer… » et choisissez le dossier du jeu.",
            )
            self.set_log("Aucune installation KuloNiku valide n’a été trouvée dans les bibliothèques Steam.")

    def choose_game(self) -> None:
        from tkinter import filedialog

        selected = filedialog.askdirectory(title="Choisir le dossier KuloNiku")
        if not selected:
            return
        candidate = Path(selected)
        if not is_windows_game_folder(candidate):
            from tkinter import messagebox

            messagebox.showerror(
                "Dossier incorrect",
                "Choisissez le dossier contenant KuloNiku_Data (ou KuloNiku Demo_Data).",
            )
            return
        self.set_game(candidate)
        self.analyze()

    def set_game(self, game: Path) -> None:
        self.game = game
        self.simulation_succeeded = False
        edition = "Démo" if "demo" in str(game).lower() else "Jeu complet"
        origin = "Steam" if "steam" in str(game).lower() else "installation locale"
        self.game_label.configure(text=f"{edition} détecté · {origin}")
        self.analyze_button.configure(state="normal")
        self.install_button.configure(state="disabled")

    def command(self, action: str, *, apply: bool = False, json_output: bool = False) -> list[str]:
        assert self.game is not None
        arguments = [str(self.paths.engine), action, str(self.game)]
        if action in {"status", "install"}:
            arguments.extend(["--translations", str(self.paths.translations)])
        if json_output:
            arguments.append("--json")
        if apply:
            arguments.append("--apply")
        return arguments

    def run_async(self, arguments: list[str], callback: Callable[[int, str], None]) -> None:
        self.set_busy(True)

        def worker() -> None:
            try:
                flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                completed = subprocess.run(
                    arguments,
                    cwd=self.paths.base,
                    env=engine_environment(),
                    capture_output=True,
                    creationflags=flags,
                    timeout=600,
                    check=False,
                )
                output = decode_engine_output(completed.stdout + completed.stderr).strip()
                status = completed.returncode
            except Exception as error:
                status, output = 1, f"Impossible de lancer le moteur : {error}"
            self.root.after(0, lambda: callback(status, output))

        threading.Thread(target=worker, daemon=True).start()

    def analyze(self) -> None:
        if not self.game or self.busy:
            return
        self.simulation_succeeded = False
        self.install_button.configure(state="disabled")
        self.set_status("Vérification du jeu…", "Contrôle de la version, de la sauvegarde et des traductions.", "info")
        self.set_log("Analyse en cours…")

        def status_done(code: int, output: str) -> None:
            self.set_log(output)
            if code != 0:
                self.set_busy(False)
                self.set_status("Vérification impossible", "Le jeu n’a pas été modifié. Consultez les détails techniques.", "error")
                return
            try:
                report = json.loads(output)
                if report.get("schema_version") != 1:
                    raise ValueError("version de rapport incompatible")
            except (json.JSONDecodeError, ValueError) as error:
                self.set_busy(False)
                self.set_log(output + f"\n\nRapport invalide : {error}")
                self.set_status("Vérification impossible", "Le rapport du moteur est incompatible.", "error")
                return

            self.restore_available = bool(report.get("backup_available"))
            self.check_latest_release(
                str(report.get("edition", "full")),
                str(report.get("available_bundle_sha256", "")),
            )
            state = report.get("state")
            translation_state = report.get("translation_state")
            if state == "patched" and translation_state == "current":
                self.set_busy(False)
                self.install_button.configure(state="disabled", text="Traduction à jour")
                self.set_status("Installation propre et à jour", "La traduction installée correspond exactement à cette version.", "good")
            elif state == "patched_unknown":
                self.set_busy(False)
                self.install_button.configure(state="disabled", text="Action indisponible")
                self.set_status(
                    "État du jeu à vérifier",
                    "Le français est présent, mais le fichier diffère du dernier état connu. L’écriture est désactivée par sécurité.",
                    "warning",
                )
            else:
                self.validate_install(report, output)

        self.run_async(self.command("status", json_output=True), status_done)

    def validate_install(self, report: dict, previous_output: str) -> None:
        is_update = report.get("state") in {"patched", "game_updated"}

        def simulation_done(code: int, output: str) -> None:
            self.set_busy(False)
            self.set_log(previous_output + "\n\n--- Simulation d’installation ---\n" + output)
            self.simulation_succeeded = code == 0
            self.install_button.configure(
                text="Mettre à jour le français" if is_update else "Installer le français",
                state="normal" if self.simulation_succeeded else "disabled",
            )
            if code != 0:
                self.set_status("Action indisponible", "La simulation a échoué. Aucune modification n’a été faite.", "error")
                return
            if report.get("source_recognition") == "unknown":
                self.set_status(
                    "Version récente, français disponible",
                    "Le patch est compatible. Les nouveaux textes absents resteront en anglais.",
                    "info",
                )
            elif is_update:
                self.set_status("Mise à jour française disponible", "La sauvegarde originale vérifiée sera conservée.", "info")
            else:
                self.set_status("Prêt à installer le français", "Une sauvegarde vérifiée sera créée avant toute écriture.", "info")

        self.run_async(self.command("install"), simulation_done)

    def install_french(self) -> None:
        from tkinter import messagebox

        if not self.game or not self.simulation_succeeded or self.busy:
            return
        updating = self.install_button.cget("text").startswith("Mettre")
        prompt = (
            "Mettre à jour la traduction française ?\n\nLa sauvegarde originale vérifiée sera conservée."
            if updating
            else "Installer la traduction française ?\n\nUne sauvegarde vérifiée sera créée avant toute modification."
        )
        if not messagebox.askokcancel("KuloNiku FR", prompt, icon="info"):
            return
        self.set_status("Mise à jour en cours…" if updating else "Installation en cours…", "Ne fermez pas cette fenêtre.", "info")

        def done(code: int, output: str) -> None:
            self.set_busy(False)
            self.set_log(output)
            self.simulation_succeeded = False
            self.install_button.configure(state="disabled")
            if code == 0:
                self.restore_available = True
                self.restore_button.configure(state="normal")
                self.set_status("Installation propre et à jour", "La traduction et sa sauvegarde originale ont été vérifiées.", "good")
                messagebox.showinfo("Traduction installée", "Relancez le jeu depuis Steam et choisissez Français dans les paramètres.")
            else:
                self.set_status("Installation impossible", "Le jeu reste protégé. Consultez les détails techniques.", "error")
                messagebox.showerror("Installation impossible", "Aucun changement incomplet ne doit rester. Consultez le diagnostic.")

        self.run_async(self.command("install", apply=True), done)

    def restore_original(self) -> None:
        from tkinter import messagebox

        if not self.game or self.busy:
            return
        self.set_status("Vérification de la sauvegarde…", "Contrôle SHA-256 avant restauration.", "info")

        def simulation_done(code: int, output: str) -> None:
            self.set_busy(False)
            self.set_log(output)
            if code != 0:
                self.set_status("Restauration indisponible", "Aucune sauvegarde vérifiée n’a été trouvée.", "error")
                return
            if not messagebox.askokcancel(
                "Restaurer le fichier original ?",
                "La traduction française sera retirée. Vous pourrez la réinstaller plus tard.",
                icon="warning",
            ):
                self.analyze()
                return
            self.set_status("Restauration en cours…", "Le fichier original vérifié est remis en place.", "info")

            def restore_done(restore_code: int, restore_output: str) -> None:
                self.set_busy(False)
                self.set_log(restore_output)
                if restore_code == 0:
                    self.set_status("Fichier original restauré", "La vérification finale SHA-256 a réussi.", "good")
                    messagebox.showinfo("Restauration terminée", "Le jeu a retrouvé son fichier sauvegardé.")
                    self.analyze()
                else:
                    self.set_status("Restauration impossible", "Le jeu reste protégé. Consultez les détails techniques.", "error")

            self.run_async(self.command("restore", apply=True), restore_done)

        self.run_async(self.command("restore"), simulation_done)

    def run(self) -> None:
        self.root.mainloop()


def main() -> int:
    paths = LauncherPaths()
    if "--self-test" in sys.argv:
        if paths.validate():
            return 1
        try:
            import tkinter

            interpreter = tkinter.Tcl()
            interpreter.eval("info patchlevel")
        except Exception:
            return 1
        return 0
    if os.name != "nt":
        print("L’interface graphique est réservée à Windows.", file=sys.stderr)
        return 2
    WindowsLauncher(paths).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
