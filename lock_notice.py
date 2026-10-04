#!/usr/bin/env python3
"""Best-effort unlock reminder. Never reads or handles the PIN."""
import queue
import re
import subprocess
import sys
import threading
import tkinter as tk

target = sys.argv[1]
events = queue.Queue()
root = tk.Tk()
root.title("HomeScreen +")
root.tk.call("tk", "appname", "homescreen-plus")
root.iconname("HomeScreen +")
root.configure(bg="#0b1020")
root.geometry("310x112")
root.resizable(False, False)
root.attributes("-topmost", True)
icon = tk.PhotoImage(width=32, height=32)
icon.put("#0b1020", to=(0, 0, 32, 32))
icon.put("#edf4ff", to=(8, 2, 24, 30))
icon.put("#243450", to=(10, 5, 22, 26))
icon.put("#64d7ff", to=(12, 8, 20, 23))
root.iconphoto(True, icon)
tk.Label(root, text="Unlock your phone", fg="#edf4ff", bg="#0b1020",
         font=("Sans", 15, "bold")).pack(pady=(17, 2))
tk.Label(root, text="Use the PIN on your physical device",
         fg="#8894ad", bg="#0b1020", font=("Sans", 10)).pack()
root.withdraw()
dismissed = False
locked_last = False

def dismiss():
    global dismissed
    dismissed = True
    root.withdraw()

root.protocol("WM_DELETE_WINDOW", dismiss)

def poll():
    # Android ROM builds vary; only show if the lock state is unambiguous.
    try:
        result = subprocess.run(
            ["adb", "-s", target, "shell", "dumpsys", "trust"],
            capture_output=True, text=True, timeout=4, check=False)
        report = result.stdout
        locked = bool(re.search(r"\bdeviceLocked\s*=\s*true\b", report, re.I))
        unlocked = bool(re.search(r"\bdeviceLocked\s*=\s*false\b", report, re.I))
        events.put(True if locked and not unlocked else False)
    except (OSError, subprocess.TimeoutExpired):
        events.put(False)

def update():
    global dismissed, locked_last
    try:
        while True:
            locked = events.get_nowait()
            if locked and not locked_last:
                dismissed = False
            if locked and not dismissed:
                root.deiconify()
            else:
                root.withdraw()
            locked_last = locked
    except queue.Empty:
        pass
    threading.Thread(target=poll, daemon=True).start()
    root.after(1900, update)

update()
root.mainloop()
