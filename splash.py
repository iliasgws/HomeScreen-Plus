#!/usr/bin/env python3
"""Animated, dependency-light HomeScreen + connection splash."""
import math
import os
import sys
import tkinter as tk

status_path = sys.argv[1]
root = tk.Tk()
root.title("HomeScreen +")
root.tk.call("tk", "appname", "homescreen-plus")
root.iconname("HomeScreen +")
app_icon = tk.PhotoImage(width=32, height=32)
app_icon.put("#0b1020", to=(0,0,32,32))
app_icon.put("#edf4ff", to=(8,2,24,30))
app_icon.put("#243450", to=(10,5,22,26))
app_icon.put("#64d7ff", to=(12,8,20,23))
root.iconphoto(True, app_icon)
root.configure(bg="#0b1020")
root.geometry("380x410")
root.resizable(False, False)
canvas = tk.Canvas(root, width=380, height=410, highlightthickness=0, bg="#0b1020")
canvas.pack()
C = {"accent": "#64d7ff", "muted": "#8894ad", "white": "#edf4ff",
     "red": "#ff7286", "green": "#65e0b2"}
canvas.create_text(190, 47, text="HomeScreen +", fill=C["white"], font=("Sans", 21, "bold"))
canvas.create_text(190, 79, text="WIRELESS MIRROR", fill=C["muted"], font=("Sans", 10, "bold"))
# Soft backdrop and handset
canvas.create_oval(66, 99, 314, 347, fill="#111c33", outline="")
canvas.create_rectangle(126, 122, 254, 313, fill="#243450", outline="#5e7394", width=3)
canvas.create_rectangle(137, 139, 243, 292, fill="#101b30", outline="")
canvas.create_line(172, 131, 207, 131, fill="#8395b2", width=4)
canvas.create_oval(185, 300, 195, 310, fill="#8395b2", outline="")
# Four independent animated Wi-Fi elements
arcs = [
    canvas.create_arc(144, 171, 236, 263, start=45, extent=90, style=tk.ARC, outline=C["accent"], width=5),
    canvas.create_arc(158, 185, 222, 249, start=45, extent=90, style=tk.ARC, outline=C["accent"], width=5),
    canvas.create_arc(171, 198, 209, 236, start=45, extent=90, style=tk.ARC, outline=C["accent"], width=5),
]
dot = canvas.create_oval(185, 221, 195, 231, fill=C["accent"], outline="")
status_text = canvas.create_text(190, 357, text="Searching for phone", fill=C["white"], font=("Sans", 13, "bold"))
detail = canvas.create_text(190, 382, text="Looking for an authorized Android device", fill=C["muted"], font=("Sans", 10))
state = "searching"
last = None
frame = 0
end_scheduled = False

def tick():
    global last, state, frame, end_scheduled
    frame += 1
    try:
        with open(status_path, encoding="utf-8") as f:
            current = f.read().strip()
    except OSError:
        current = ""
    if current and current != last:
        last = current
        if current.startswith("connecting:"):
            state = "connecting"
            canvas.itemconfig(status_text, text="Connecting", fill=C["white"])
            canvas.itemconfig(detail, text="Checking " + current.split(":", 1)[1][:35])
        elif current == "searching":
            state = "searching"
            canvas.itemconfig(status_text, text="Searching for phone", fill=C["white"])
            canvas.itemconfig(detail, text="Looking for an authorized Android device")
        elif current == "launching":
            state = "launching"
            canvas.itemconfig(status_text, text="Connected", fill=C["green"])
            canvas.itemconfig(detail, text="Opening screen mirror")
            if not end_scheduled:
                root.after(650, root.destroy)
                end_scheduled = True
        elif current == "notfound":
            state = "notfound"
            canvas.itemconfig(status_text, text="Phone not found", fill=C["red"])
            canvas.itemconfig(detail, text="Check Wi-Fi and ADB debugging")
            if not end_scheduled:
                root.after(2400, root.destroy)
                end_scheduled = True
    accent = C["red"] if state == "notfound" else C["green"] if state == "launching" else C["accent"]
    for index, item in enumerate(arcs):
        strength = (math.sin(frame * 0.21 - index * 0.7) + 1) / 2
        dim = "#304764"
        canvas.itemconfig(item, outline=accent if strength > 0.35 else dim)
    canvas.itemconfig(dot, fill=accent if frame % 12 < 9 else "#304764")
    root.after(65, tick)

tick()
root.mainloop()
