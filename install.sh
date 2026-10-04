#!/usr/bin/env bash
set -euo pipefail
BASE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
for command in adb scrcpy nmap ip flock; do
  command -v "$command" >/dev/null || { echo "Missing: $command" >&2; exit 1; }
done
python3 -c "import tkinter" >/dev/null 2>&1 || { echo "Missing Tkinter: sudo dnf install python3-tkinter" >&2; exit 1; }
install -Dm755 "$BASE/phone" "$HOME/.local/bin/homescreen-plus"
install -Dm644 "$BASE/splash.py" "$HOME/.local/share/homescreen-plus/splash.py"
install -Dm644 "$BASE/icons/homescreen-plus.svg" "$HOME/.local/share/icons/hicolor/scalable/apps/homescreen-plus.svg"
mkdir -p "$HOME/.local/share/applications"
cat > "$HOME/.local/share/applications/homescreen-plus.desktop" <<DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=HomeScreen +
Comment=Wireless Android mirror using scrcpy
Exec=$HOME/.local/bin/homescreen-plus
Icon=homescreen-plus
Terminal=false
StartupWMClass=homescreen-plus
Categories=Utility;AudioVideo;
StartupNotify=false
DESKTOP
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
printf 'Installed HomeScreen +. Run: gtk-launch homescreen-plus\n'
