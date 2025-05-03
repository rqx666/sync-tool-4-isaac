import os
import sys
import glob
import shutil
import datetime
import subprocess
import customtkinter as ctk
from tkinter import messagebox

# === FIND ISAAC SAVE PATH (Steam Cloud) ===
def find_isaac_cloud_save_path():
    base = "C:\\Program Files (x86)\\Steam\\userdata"
    if not os.path.exists(base):
        return None
    candidates = glob.glob(os.path.join(base, "*", "250900", "remote"))
    return candidates[0] if candidates else None

ISAAC_PATH = find_isaac_cloud_save_path()
if ISAAC_PATH is None:
    raise FileNotFoundError("Could not locate Isaac save folder in Steam userdata.")

# === DETECT CORRECT SAVE FILE FORMAT ===
def find_save_file_template():
    rep_path = os.path.join(ISAAC_PATH, "rep+persistentgamedata1.dat")
    vanilla_path = os.path.join(ISAAC_PATH, "persistentgamedata1.dat")
    if os.path.exists(rep_path):
        return os.path.join(ISAAC_PATH, "rep+persistentgamedata{}.dat")
    elif os.path.exists(vanilla_path):
        return os.path.join(ISAAC_PATH, "persistentgamedata{}.dat")
    else:
        raise FileNotFoundError("No Isaac save files found in Rep+ or vanilla format.")

SAVE_FILE_TEMPLATE = find_save_file_template()

# === STEAM CONFIG FOR LAUNCH ===
STEAM_PATH = "C:\\Program Files (x86)\\Steam\\steam.exe"
ISAAC_APP_ID = "250900"

# === RESOURCE PATH (for icon when bundled with PyInstaller) ===
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# === GUI SETUP ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sync Tool 4 Isaac")
app.geometry("400x450")
app.resizable(False, False)

# Load icon (optional but recommended)
icon_path = resource_path("icon.ico")
try:
    app.iconbitmap(icon_path)
except Exception as e:
    print(f"Warning: Failed to load icon: {e}")

# === FUNCTIONS ===
def get_save_path(slot):
    return SAVE_FILE_TEMPLATE.format(slot)

def backup_file(filepath):
    if os.path.exists(filepath):
        backup_dir = os.path.join(ISAAC_PATH, "Backups")
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = os.path.join(backup_dir, os.path.basename(filepath) + f".bak_{timestamp}")
        shutil.copy2(filepath, backup_name)

def sync_saves():
    source_slot = source_var.get()
    dest_slots = [i for i, var in enumerate(dest_vars, start=1) if var.get() == 1]
    backup = backup_var.get()
    launch = launch_var.get()

    source_path = get_save_path(source_slot)

    if not os.path.exists(source_path):
        messagebox.showerror("Error", f"Source slot {source_slot} not found!")
        return

    for slot in dest_slots:
        if slot == source_slot:
            continue
        dest_path = get_save_path(slot)
        if backup:
            backup_file(dest_path)
        shutil.copy2(source_path, dest_path)

    status_label.configure(text="✅ Sync completed successfully!", text_color="green")

    if launch:
        try:
            subprocess.Popen([STEAM_PATH, "-applaunch", ISAAC_APP_ID])
        except Exception as e:
            messagebox.showwarning("Steam Error", f"Could not launch Isaac:\n{e}")

# === UI ELEMENTS ===
title = ctk.CTkLabel(app, text="Sync Tool 4 Isaac", font=ctk.CTkFont(size=20, weight="bold"))
title.pack(pady=(20, 10))

source_label = ctk.CTkLabel(app, text="Select source slot:")
source_label.pack()
source_var = ctk.IntVar(value=1)
source_menu = ctk.CTkOptionMenu(app, variable=source_var, values=["1", "2", "3"])
source_menu.pack(pady=(0, 10))

dest_label = ctk.CTkLabel(app, text="Select destination slots:")
dest_label.pack()
frame = ctk.CTkFrame(app)
frame.pack(pady=5)

dest_vars = [ctk.IntVar() for _ in range(3)]
for i in range(3):
    cb = ctk.CTkCheckBox(frame, text=f"Slot {i+1}", variable=dest_vars[i])
    cb.grid(row=0, column=i, padx=10)

backup_label = ctk.CTkLabel(app, text="Backup Options:")
backup_label.pack(pady=(10, 0))

backup_var = ctk.IntVar(value=1)
backup_cb = ctk.CTkCheckBox(app, text="Create backup before overwrite", variable=backup_var)
backup_cb.pack(pady=(2, 10))

launch_label = ctk.CTkLabel(app, text="Post-Sync Actions:")
launch_label.pack(pady=(5, 0))

launch_var = ctk.IntVar()
launch_cb = ctk.CTkCheckBox(app, text="Launch Isaac after sync", variable=launch_var)
launch_cb.pack(pady=(2, 15))

sync_button = ctk.CTkButton(app, text="🔁 Sync Save Files", command=sync_saves)
sync_button.pack(pady=(0, 10))

status_label = ctk.CTkLabel(app, text="", text_color="gray")
status_label.pack()

app.mainloop()
