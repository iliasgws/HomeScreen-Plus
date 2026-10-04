#!/usr/bin/env python3
"""HomeScreen + progress window. No external assets."""
import os
import subprocess
import sys
import tkinter as tk

status_path = sys.argv[1]

def dark_mode():
    override = os.environ.get("HOMESCREEN_THEME", "auto").lower()
    if override in ("dark", "light"):
        return override == "dark"
    # GNOME/GTK on Fedora, falling back to the freedesktop portal's setting.
    try:
        p = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            capture_output=True, text=True, timeout=1)
        if "prefer-dark" in p.stdout:
            return True
        if "prefer-light" in p.stdout:
            return False
    except (OSError, subprocess.TimeoutExpired):
        pass
    try:
        p = subprocess.run(
            ["dbus-send", "--session", "--print-reply", "--dest=org.freedesktop.portal.Desktop",
             "/org/freedesktop/portal/desktop", "org.freedesktop.portal.Settings.Read",
             "string:org.freedesktop.appearance", "string:color-scheme"],
            capture_output=True, text=True, timeout=1)
        if "uint32 1" in p.stdout:
            return True
        if "uint32 2" in p.stdout:
            return False
    except (OSError, subprocess.TimeoutExpired):
        pass
    return False

dark = dark_mode()
BG, FG, MUTED, ACCENT = (
    ("#202124", "#f3f4f6", "#aab0bb", "#89b4fa") if dark
    else ("#f7f7f8", "#202124", "#68717d", "#2878ca")
)
root = tk.Tk(className="homescreen-plus")
root.title("HomeScreen +")
root.tk.call("tk", "appname", "homescreen-plus")
root.configure(bg=BG)
root.geometry("410x300")
root.minsize(350, 280)
icon = tk.PhotoImage(width=32, height=32)
icon.put(BG, to=(0, 0, 32, 32))
icon.put(FG, to=(9, 2, 23, 30))
icon.put(BG, to=(11, 5, 21, 26))
icon.put(ACCENT, to=(13, 10, 19, 21))
root.iconphoto(True, icon)
canvas = tk.Canvas(root, height=155, bg=BG, highlightthickness=0)
canvas.pack(fill="both", expand=True, padx=20, pady=(18, 0))
label = tk.Label(root, text="Searching for phone", bg=BG, fg=FG, font=("Sans", 12))
label.pack(pady=(7, 26))
previous = None
angle = 0
closing = False
mode = "searching"

def tick():
    global previous, angle, closing, mode
    angle = (angle + 14) % 360
    canvas.delete("all")
    w, h = max(220, canvas.winfo_width()), max(140, canvas.winfo_height())
    x, y = w / 2, h / 2
    canvas.create_rectangle(x-40, y-65, x+40, y+65, outline=MUTED, width=2)
    canvas.create_line(x-9, y-57, x+9, y-57, fill=MUTED, width=2)
    canvas.create_oval(x-2, y+55, x+2, y+59, fill=MUTED, outline="")
    if mode not in ("launching", "notfound"):
        canvas.create_arc(x-23, y-23, x+23, y+23, start=angle, extent=260,
                          style=tk.ARC, outline=ACCENT, width=4)
    else:
        canvas.create_oval(x-4, y-4, x+4, y+4, fill=ACCENT, outline="")
    try:
        with open(status_path, encoding="utf-8") as stream:
            current = stream.read().strip()
    except OSError:
        current = ""
    if current and current != previous:
        previous = current
        if current.startswith("connecting:"):
            mode = "connecting"
            label.config(text="Connecting")
        elif current == "searching":
            mode = "searching"
            label.config(text="Searching for phone")
        elif current == "launching":
            mode = "launching"
            label.config(text="Connected")
            if not closing:
                closing = True
                root.after(650, root.destroy)
        elif current == "notfound":
            mode = "notfound"
            label.config(text="Phone not found")
            if not closing:
                closing = True
                root.after(2200, root.destroy)
    root.after(65, tick)

tick()
root.mainloop()
