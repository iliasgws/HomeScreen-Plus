#!/usr/bin/env python3
"""Responsive HomeScreen + startup splash, Tkinter only."""
import math
import os
import sys
import tkinter as tk

status_path = sys.argv[1]
BG = "#0d1322"
PANEL = "#151f32"
EDGE = "#26334b"
TEXT = "#f1f5ff"
MUTED = "#93a3be"
BLUE = "#68d6ff"
GREEN = "#66e3b5"
RED = "#ff7891"

root = tk.Tk(className="homescreen-plus")
root.title("HomeScreen +")
root.iconname("HomeScreen +")
root.configure(bg=BG)
root.geometry("460x460")
root.minsize(420, 430)
root.resizable(True, True)
root.tk.call("tk", "appname", "homescreen-plus")
icon = tk.PhotoImage(width=32, height=32)
icon.put(BG, to=(0, 0, 32, 32))
icon.put(TEXT, to=(8, 2, 24, 30))
icon.put(EDGE, to=(10, 5, 22, 26))
icon.put(BLUE, to=(12, 8, 20, 23))
root.iconphoto(True, icon)
# Request enough room for the title and bottom status on scaled desktops.
root.update_idletasks()

# Text uses real layout widgets, so it is never clipped by the illustration.
heading = tk.Frame(root, bg=BG)
heading.pack(fill="x", pady=(21, 4))
tk.Label(heading, text="HomeScreen +", bg=BG, fg=TEXT,
         font=("Sans", 15, "bold")).pack()
tk.Label(heading, text="WIRELESS MIRROR", bg=BG, fg=MUTED,
         font=("Sans", 9)).pack(pady=(4, 0))

visual = tk.Canvas(root, bg=BG, highlightthickness=0, height=170)
visual.pack(fill="both", expand=True, padx=12)
status = tk.Label(root, text="Searching for phone", bg=BG, fg=TEXT,
                  font=("Sans", 12, "bold"))
status.pack(fill="x", padx=16, pady=(4, 0))
detail = tk.Label(root, text="Looking for your Android device", bg=BG,
                  fg=MUTED, font=("Sans", 10), wraplength=275)
detail.pack(fill="x", padx=16, pady=(5, 25))

mode = "searching"
last = None
frame = 0
end_scheduled = False

def render():
    visual.delete("all")
    w = max(250, visual.winfo_width())
    h = max(165, visual.winfo_height())
    cx, cy = w / 2, h / 2
    scale = min(w / 300, h / 215, 1.1)
    def xy(x, y):
        return (cx + x * scale, cy + y * scale)
    def oval(x1, y1, x2, y2, **kw):
        visual.create_oval(*xy(x1, y1), *xy(x2, y2), **kw)
    def rect(x1, y1, x2, y2, **kw):
        visual.create_rectangle(*xy(x1, y1), *xy(x2, y2), **kw)
    oval(-98, -100, 98, 100, fill=PANEL, outline="")
    oval(-78, -80, 78, 80, outline=EDGE, width=1)
    rect(-46, -91, 46, 91, fill="#22324b", outline="#657d9b", width=2)
    rect(-37, -77, 37, 70, fill=BG, outline="")
    visual.create_line(*xy(-10, -84), *xy(10, -84), fill=MUTED, width=3)
    oval(-4, 79, 4, 87, fill=MUTED, outline="")
    accent = RED if mode == "notfound" else GREEN if mode == "launching" else BLUE
    for index, radius in enumerate((41, 29, 17)):
        lum = (math.sin(frame * 0.20 - index * 0.85) + 1) / 2
        color = accent if (lum > 0.28 or mode in ("notfound", "launching")) else EDGE
        visual.create_arc(*xy(-radius, -radius + 8), *xy(radius, radius + 8),
                          start=45, extent=90, style=tk.ARC,
                          outline=color, width=max(2, round(3 * scale)))
    oval(-5, 8, 5, 18, fill=accent, outline="")

def tick():
    global mode, frame, last, end_scheduled
    frame += 1
    try:
        with open(status_path, encoding="utf-8") as stream:
            current = stream.read().strip()
    except OSError:
        current = ""
    if current and current != last:
        last = current
        if current.startswith("connecting:"):
            mode = "connecting"
            status.config(text="Connecting", fg=TEXT)
            detail.config(text="Contacting " + current.split(":", 1)[1][:40])
        elif current == "searching":
            mode = "searching"
            status.config(text="Searching for phone", fg=TEXT)
            detail.config(text="Looking for your Android device")
        elif current == "launching":
            mode = "launching"
            status.config(text="Connected", fg=GREEN)
            detail.config(text="Opening your screen mirror")
            if not end_scheduled:
                root.after(650, root.destroy)
                end_scheduled = True
        elif current == "notfound":
            mode = "notfound"
            status.config(text="Phone not found", fg=RED)
            detail.config(text="Check Wi-Fi and ADB debugging")
            if not end_scheduled:
                root.after(2400, root.destroy)
                end_scheduled = True
    render()
    root.after(70, tick)

tick()
root.mainloop()
