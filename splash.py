#!/usr/bin/env python3
"""Connection status window for HomeScreen +."""
import os
import sys
import tkinter as tk

path = sys.argv[1]
root = tk.Tk(className="homescreen-plus")
root.title("HomeScreen +")
root.tk.call("tk", "appname", "homescreen-plus")
root.configure(bg="#17191d")
root.geometry("400x310")
root.minsize(360, 300)

icon = tk.PhotoImage(width=32, height=32)
icon.put("#17191d", to=(0, 0, 32, 32))
icon.put("#e0e3e8", to=(9, 2, 23, 30))
icon.put("#17191d", to=(11, 5, 21, 26))
icon.put("#7dbece", to=(13, 10, 19, 21))
root.iconphoto(True, icon)

canvas = tk.Canvas(root, height=160, bg="#17191d", highlightthickness=0)
canvas.pack(fill="both", expand=True, padx=20, pady=(18, 0))
label = tk.Label(root, text="Searching for phone", bg="#17191d",
                 fg="#e0e3e8", font=("Sans", 12))
label.pack(pady=(4, 26))

previous = None
phase = 0
closing = False

def refresh():
    global previous, phase, closing
    phase += 1
    canvas.delete("all")
    w, h = max(240, canvas.winfo_width()), max(150, canvas.winfo_height())
    x, y = w / 2, h / 2
    canvas.create_rectangle(x-39, y-64, x+39, y+64,
                            outline="#c8d0dc", width=2)
    canvas.create_line(x-9, y-56, x+9, y-56, fill="#c8d0dc", width=2)
    canvas.create_oval(x-2, y+54, x+2, y+58, fill="#c8d0dc", outline="")
    color = "#7dbece" if phase % 8 < 5 else "#36434b"
    for radius in (32, 23, 14):
        canvas.create_arc(x-radius, y-radius+9, x+radius, y+radius+9,
                          start=45, extent=90, style="arc",
                          outline=color, width=3)
    canvas.create_oval(x-3, y+10, x+3, y+16, fill=color, outline="")

    try:
        with open(path, encoding="utf-8") as stream:
            current = stream.read().strip()
    except OSError:
        current = ""
    if current and current != previous:
        previous = current
        if current.startswith("connecting:"):
            label.config(text="Connecting")
        elif current == "searching":
            label.config(text="Searching for phone")
        elif current == "launching":
            label.config(text="Connected")
            if not closing:
                root.after(650, root.destroy)
                closing = True
        elif current == "notfound":
            label.config(text="Phone not found")
            if not closing:
                root.after(2200, root.destroy)
                closing = True
    root.after(100, refresh)

refresh()
root.mainloop()
