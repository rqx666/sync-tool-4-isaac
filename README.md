# Sync Tool 4 Isaac

A simple tool to copy your desired save file to other save slots in The Binding of Isaac: Repentance+.

---

###  IMPORTANT 

-  When launching Isaac via the "Launch Isaac after sync" option, Steam may prompt you to choose between:

	-  Download from Steam Cloud

	-  Use local files

-  You MUST choose “Use local files” for your synced saves to take effect.

-  If you choose the Steam Cloud version, it may overwrite the synced saves with old cloud data.

---

###  Features

-  Sync your save from slot 1 to slot 2 and 3
-  Supports ONLY **Repentance+** (`rep+` save files)
-  Auto-detects Steam Cloud save paths
-  Optional backups before overwriting
-  One-click launch for Isaac after sync
-  Clean, dark-themed interface with [customtkinter](https://github.com/TomSchimansky/CustomTkinter)

---

###  Requirements (for source)

-  If you're running from source:

```bash
pip install customtkinter