# 🖥️ Terracina OS v.6.77
A cloud-connected Virtual OS built in Python. Manage files, run apps, and explore a decentralized marketplace.

---

## 🚀 Marketplace Ecosystem
Terracina OS features a two-tier application store inspired by the "Geometry Dash" level system.

### 🌟 Featured Apps (Verified)
The `APPS/` directory contains officially verified applications. These apps are manually audited for safety and quality by the administrator. 

### 🌐 Community Apps (Unlisted/Recent)
The `COMMUNITY/` area is a decentralized space where any developer can publish their work. These apps are hosted on independent servers and added automatically by our **Marketplace Bot**.

---

## 🛠️ Developer Registration (How to Publish)
If you want to become a developer and add your server to the `PROVIDERS.TXT` list, follow these steps:

1. **Host your files**: Create a GitHub repository with your `.EXE` or `.BAT` scripts.
2. **Submit a Request**: Open a **New Issue** in this repository using the **[ADD_ME]** template.
3. **Automatic Approval**: Our GitHub Bot will automatically verify your link and add you to the global provider list.
4. **Get Featured**: If your app receives positive feedback (Issues/Stars), it will be audited and moved to the **Official Featured List**.

---

## ⌨️ Command Reference

| Command | Description |
| :--- | :--- |
| **DIR** | List files and directories in the current path. |
| **SAVE / EDIT** | Create or modify files. Use `END` to save in SAVE, and `SAVE` to exit EDIT. |
| **MD / RD / CD** | Directory management (Make, Remove, Change). |
| **RUN [FILE]** | Execute applications. |
| **GET [FILE]** | Download apps from Featured or Community servers. |
| **SOURCES** | View all registered Featured and Community providers. |
| **TASK / KILL** | Manage running processes and system RAM. |
| **TREE** | Display the full disk structure. |
| **CUT / COPY / REN**| Advanced file manipulation (Move, Duplicate, Rename). |

Enjoy!
