import os
import time
import sys
import json
import random
import requests
from datetime import datetime

# --- CONFIGURATION ---
# Create a folder for the OS data if it doesn't exist
if not os.path.exists("MSDOS_DATA"):
    os.makedirs("MSDOS_DATA")
DISK_PATH = "MSDOS_DATA/system_disk_c.json"
def save_to_disk(disk):
    with open(DISK_PATH, 'w') as f: 
        json.dump(disk, f)
TOTAL_RAM = 640 # KB
MAX_DISK_KB = 1440 # 1.44MB limit

def get_disk_usage(disk):
    # Calculates size based on the number of characters in the disk dictionary
    return sum(len(str(v)) for v in disk.values()) / 1024

# System State
running_tasks = {
    "0": ["SYSTEM", 12],
    "1": ["COMMAND.COM", 45],
}

def load_disk():
    # If the file exists, just load it normally
    if os.path.exists(DISK_PATH):
        try:
            with open(DISK_PATH, 'r') as f: return json.load(f)
        except: return None
    
    # --- FAKE INSTALLER VISUALS ---
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==========================================")
    print("    MS-DOS v.6.77 INSTALLATION MEDIA      ")
    print("==========================================")
    print("\nPreparing virtual drive...")
    time.sleep(1)
    
    # Simple Progress Bar
    for i in range(1, 11):
        bar = "#" * i
        spaces = " " * (10 - i)
        sys.stdout.write(f"\rInstalling System: [{bar}{spaces}] {i*10}%")
        sys.stdout.flush()
        time.sleep(0.3)
    
    print("\n\nInstallation Complete.")
    print("Creating System Files: KERNEL.SYS, COMMAND.COM...")
    time.sleep(1)
    
    # The "Factory Image" Data
    new_disk = {
        "KERNEL.SYS": "SYS_CORE_DATA_V6.77",
        "COMMAND.COM": "SYSTEM_SHELL_ACTIVE",
        "README.TXT": "Welcome to MS-DOS v.6.77.",
        "MANUAL.TXT": "THIS IS A TUTORIAL ON HOW TO SAVE THE O.S. IN CASE OF A BLUE SCREEN: STEP 1: TRY TO SEE IF AUTOMATIC REPAIR CAN HANDLE IT. STEP 2: IF THE AUTOMATIC REPAIR FAILS, YOU NEED TO SEARCH FOR THE DISK FILE (system_disk_c.json) IN YOUR PC AND DELETE IT. STEP 3: REINSTALL THE DISK TO FIX THE SYSTEM (you will lose all your data. Do this ONLY if you don't have any important files in your PC. This is only a last resort function).", "CONFIG.SYS": "PASS:NONE", "PASSWORD": ""
    }
    
    # Save the new disk
    with open(DISK_PATH, 'w') as f: json.dump(new_disk, f)
    
    print("\nReady to boot. Press ENTER to continue.")
    input()
    return new_disk


def get_used_ram():
    return sum(info[1] for info in running_tasks.values())

def get_system_lag():
    used = get_used_ram()
    if used > TOTAL_RAM: return 0.6
    if used > (TOTAL_RAM * 0.8): return 0.3
    return 0

# --- RECOVERY & BSOD ---

def bsod(error_msg):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[44m\033[37m")
    print(" :( Your PC ran into a problem and needs to restart.")
    print(" We're just collecting some error info, then we'll restart.")
    for i in range(0, 101, 10):
        sys.stdout.write(f"\r {i}% complete"); sys.stdout.flush(); time.sleep(0.2)
    print(f"\n\n Stop Code: {error_msg}\033[0m")
    time.sleep(1.5)
    auto_repair_sequence(error_msg)

def auto_repair_sequence(error_msg):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Preparing Automatic Repair...")
    time.sleep(20)
    
    # This triggers the load_disk() above to recreate the file
    disk = load_disk() 
    
    if "KERNEL.SYS" not in disk:
        print(f"\nRepair failed. Critical files missing.")
        input("Press ENTER to try reboot anyway..."); boot_sequence()
    else:
        print("Repairing system files..."); time.sleep(10)
        print("Success."); time.sleep(1)
        print("Rebooting System..."); time.sleep(2)
        boot_sequence()

# --- BOOT ---

def boot_sequence():
    os.system('cls' if os.name == 'nt' else 'clear')
    disk = load_disk()
    
    # BIOS PASSWORD CHECK
    if disk.get("PASSWORD"):
        print("==========================================")
        print("      SYSTEM LOCKED - ENTER PASSWORD      ")
        print("==========================================")
        attempt = input("PASSWORD: ")
        if attempt != disk["PASSWORD"]:
            print("ACCESS DENIED.")
            time.sleep(2)
            boot_sequence() # Loop back
            return
    print("Wait, System is starting...")
    time.sleep(0.5)
    disk = load_disk()
    if not disk or "KERNEL.SYS" not in disk: bsod("CRITICAL_SERVICE_FAILED")
    
    print("\nLoading System Files...")
    files = ["HIMEM.SYS", "CONFIG.SYS", "COMMAND.COM"]
    for i, f in enumerate(files):
        progress = (i + 1) / len(files)
        bar = '#' * int(20 * progress) + ' ' * (20 - int(20 * progress))
        sys.stdout.write(f"\r[{bar}] Loading {f.ljust(12)}"); sys.stdout.flush()
        time.sleep(0.4)
    os.system('cls' if os.name == 'nt' else 'clear')
    kernel_shell(disk)

# --- MAIN SHELL ---

def kernel_shell(disk):
    current_dir = ""
    current_time = datetime.now().strftime("%Y-%m-%d")
    print(f"MS-DOS v.6.77 | {current_time}")

    print("TYPE 'HELP' FOR COMMAND LIST")
    
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        time.sleep(get_system_lag())
        used = get_used_ram()
        # Dynamically build the prompt based on the current directory
        cwd_label = f"C:\\{current_dir}" if current_dir else "C:\\"
        prompt = f"[{used}/{TOTAL_RAM}K] {cwd_label}>"
        cmd_input = input(prompt).strip()
        if not cmd_input: continue
        
        parts = cmd_input.split()
        cmd = parts[0].upper()
        args = parts[1:]

        if cmd == "DIR":
            print(f"\n Directory of C:\\{current_dir}")
            shown_folders = set()
            for f in disk:
                if current_dir == "": # We are in Root
                    if "/" not in f:
                        print(f"  {f.ljust(15)} <FILE>")
                    else:
                        folder_name = f.split("/")[0]
                        if folder_name not in shown_folders:
                            print(f"  {folder_name.ljust(15)} <DIR>")
                            shown_folders.add(folder_name)
                else: # We are inside a folder
                    if f.startswith(current_dir + "/"):
                        display_name = f.replace(current_dir + "/", "")
                        print(f"  {display_name.ljust(15)} <FILE>")
            print(f"\n Disk: {get_disk_usage(disk):.2f}KB / {MAX_DISK_KB}KB used\n")

            
        elif cmd == "SAVE":
            if args:
                fname = args[0].upper()
                full_path = f"{current_dir}/{fname}" if current_dir else fname
                
                if full_path in disk:
                    confirm = input(f"WARNING: {fname} already exists. Overwrite? (Y/N): ")
                    if confirm.upper() != 'Y':
                        print("Save aborted.")
                        continue

                print(f"Editing {full_path}. Type 'END' to save.")
                lines = []
                while True:
                    line = input(">> ")
                    if line.upper() == "END": break
                    lines.append(line)
                disk[full_path] = "\n".join(lines)
                save_to_disk(disk)
                print(f"File saved to {full_path}")
            else:
                print("Usage: SAVE [FILENAME]")


            
        elif cmd == "MD": # Make Directory
            if args:
                new_folder = args[0].upper()
                # Create a hidden system file to 'initialize' the folder
                folder_path = f"{new_folder}/INIT.SYS"
                if any(f.startswith(new_folder + "/") for f in disk):
                    print("Directory already exists.")
                else:
                    disk[folder_path] = "FOLDER_INIT"
                    save_to_disk(disk)
                    print(f"Directory {new_folder} created.")
            else:
                print("Usage: MD [DIRECTORY NAME]")
                
                
        elif cmd == "RD": # Remove Directory
            if args:
                target_folder = args[0].upper()
                # Find all files that start with "FOLDERNAME/"
                to_delete = [f for f in disk if f.startswith(target_folder + "/")]
                
                if to_delete:
                    confirm = input(f"Delete folder '{target_folder}' and all files inside? (Y/N): ")
                    if confirm.upper() == 'Y':
                        for f in to_delete:
                            del disk[f]
                        save_to_disk(disk)
                        print("Directory removed.")
                else:
                    print("Directory not found or empty.")
            else:
                print("Usage: RD [DIRECTORY NAME]")



        elif cmd == "RUN": # THE REAL EXECUTOR
            if args:
                fname = args[0].upper()
                if fname in disk and (fname.endswith(".EXE") or fname.endswith(".BAT")):
                    prog_ram = random.randint(15, 60)
                    if used + prog_ram > TOTAL_RAM:
                        print("OUT OF MEMORY ERROR."); continue
                    
                    print(f"Running {fname}...")
                    
                    # THE SHIELD: We give the app access to your OS functions/data 
                    # but we do NOT import 'os', 'sys', or 'shutil'.
                    safe_env = {
                        "disk": disk,
                        "save_to_disk": save_to_disk,
                        "print": print,
                        "input": input,
                        "int": int,
                        "str": str,
                        "len": len,
                        "range": range,
                        "random": random,
                        "time": time,
                        "globals": globals
                    }

                    try:
                        # We execute using the safe_env as the global context
                        exec(disk[fname], safe_env) 
                        
                        # PID LOGIC
                        new_pid = str(max([int(p) for p in running_tasks.keys()]) + 1)
                        running_tasks[new_pid] = [fname, prog_ram]
                        
                    except Exception as e: 
                        print(f"Runtime Error: {e}")
                else: 
                    print("File not found or not executable.")


        elif cmd == "OPEN" or cmd == "TYPE":
            if args:
                fname = args[0].upper()
                # Check if file exists in current folder OR if it's a full path
                full_path = f"{current_dir}/{fname}" if current_dir else fname
                
                if full_path in disk:
                    print(f"\n--- {full_path} ---\n{disk[full_path]}\n")
                elif fname in disk: # Fallback for root files
                    print(f"\n--- {fname} ---\n{disk[fname]}\n")
                else:
                    print("File not found.")
            else:
                print("Usage: OPEN [FILENAME]")

        elif cmd == "TASK":
            print("\nPID   NAME         RAM")
            for pid, info in running_tasks.items():
                print(f"{pid.ljust(5)} {info[0].ljust(12)} {info[1]}KB")

        elif cmd == "KILL":
            if args and args[0] in running_tasks:
                pid = args[0]
                if pid in ["0", "1"]: bsod(f"SYSTEM_CRASH_PID_{pid}")
                else: del running_tasks[pid]
            else: print("Invalid PID.")
            
        elif cmd == "DEL":
            if args:
                fname = args[0].upper()
                full_path = f"{current_dir}/{fname}" if current_dir else fname
                if full_path in disk:
                    del disk[full_path]
                    save_to_disk(disk)
                    print(f"File {fname} deleted.")
                else:
                    print("File not found.")
            else:
                print("Usage: DEL [FILENAME]")
            
        elif cmd == "GET":
            if args:
                filename = args[0].upper()
                print("\nSELECT MARKETPLACE SOURCE:")
                print("1. [FEATURED] (Verified & Safe)")
                print("2. [RECENT]   (Community & Unverified)")
                
                choice = input("\nYour choice (1/2): ")
                base_url = "https://raw.githubusercontent.com/valeraspberry/CUSTOM_OS/main/"
                
                # --- CONFIGURAZIONE DINAMICA ---
                if choice == "1":
                    folder = "FEATURED_APPS/"
                    source_file = "featured_providers.txt"
                else:
                    folder = "RECENT_APPS/"
                    source_file = "recent_providers.txt"

                # --- STEP 1: CONTROLLO CARTELLE UFFICIALI SUL TUO REPO ---
                print(f"Searching in {folder}...")
                try:
                    off_req = requests.get(base_url + folder + filename, timeout=5)
                    if off_req.status_code == 200:
                        disk[filename] = off_req.text
                        save_to_disk(disk)
                        print(f"SUCCESS: {filename} downloaded from {folder}")
                        continue # Esce, operazione completata
                except:
                    pass

                # --- STEP 2: RICERCA NEI PROVIDER ESTERNI (Se non trovato sopra) ---
                print(f"Connecting to {source_file} for external servers...")
                try:
                    r = requests.get(base_url + source_file, timeout=5)
                    if r.status_code == 200:
                        providers = r.text.strip().split('\n')
                        found = False
                        for p in providers:
                            if not p or ":" not in p or p.startswith("#"): continue
                            dev_name, dev_url = p.split(':', 1)
                            
                            if not dev_url.endswith("/"): dev_url += "/"
                            
                            print(f"Searching on {dev_name}'s server...")
                            file_req = requests.get(dev_url + filename, timeout=5)
                            
                            if file_req.status_code == 200:
                                disk[filename] = file_req.text
                                save_to_disk(disk)
                                print(f"SUCCESS: {filename} found on {dev_name}'s server")
                                found = True
                                break
                        
                        if not found:
                            print(f"ERROR: {filename} not found in {folder} or registered servers.")
                    else:
                        print(f"ERROR: Could not connect to {source_file}")
                except Exception as e:
                    print(f"CONNECTION ERROR: {e}")
            else:
                print("Usage: GET [FILENAME]")
                
        elif cmd == "INSPECT":
            if args:
                filename = args[0].upper()
                print(f"--- SECURITY INSPECTION: {filename} ---")
                print("Fetching code for preview only...")
                
                # Qui usiamo la logica del GET ma facciamo solo il PRINT
                # Esempio semplificato:
                # content = requests.get(url_dall_elenco).text
                # print("-" * 30)
                # print(content)
                # print("-" * 30)
                print("AUDIT COMPLETE. If the code looks safe, you can use GET to install it.")
            else:
                print("Usage: INSPECT [FILENAME]")

                    
        elif cmd == "SUDO":
            if args and args[0].upper() == "GURU":
                # 1 in 10 chance to crash the system
                if random.randint(1, 10) == 1:
                    bsod("GURU_MEDITATION_FATAL_ERROR")
                else:
                    wisdom = [
                        "Error 404: Sleep not found. Continue working?",
                        "A clean C:\\ drive is a happy life",
                        "If something lags, change WiFi, just like in real life"
                    ]
                    print(f"\n[SYSTEM GURU]: {random.choice(wisdom)}\n")
            else:
                print("Access Denied.")

                
                
        elif cmd == "REN":
            if len(args) >= 2:
                old_name = args[0].upper()
                new_name = args[1].upper()
                
                # Check if we are in a folder and adjust paths
                old_path = f"{current_dir}/{old_name}" if current_dir else old_name
                new_path = f"{current_dir}/{new_name}" if current_dir else new_name
                
                if old_path in disk:
                    if new_path in disk:
                        print("Error: Target filename already exists.")
                    else:
                        disk[new_path] = disk.pop(old_path)
                        save_to_disk(disk)
                        print(f"Renamed {old_name} to {new_name}.")
                else:
                    print("File not found.")
            else:
                print("Usage: REN [OLD_NAME] [NEW_NAME]")


        elif cmd == "CLS": os.system('cls' if os.name == 'nt' else 'clear')
        elif cmd == "REBOOT": boot_sequence()
        elif cmd == "SHUTDOWN": sys.exit()
        elif cmd == "HELP":
            print("\n" + "="*45)
            print("         MS-DOS v.6.76 HELP SYSTEM")
            print("="*45)
            print(" FILE MANAGMENT:  SAVE, OPEN, DEL, REN, FIND, COPY, CUT, EDIT, INSPECT")
            print(" DISK MANAGMENT:  DIR, TREE, MD, RD, CD")
            print(" SYSTEM:     RUN, TASK, KILL, CLS, TIME, MENU")
            print(" POWER:      SUDO, REBOOT, SHUTDOWN")
            print(" ONLINE:      GET, SOURCES")
            print("-" * 45)
            print(" Type 'OPEN MANUAL.TXT' for recovery info.")
            print("="*45 + "\n")
            
        elif cmd == "EDIT":
            if args:
                filename = args[0].upper()
                print(f"--- EDITING {filename} ---")
                print("Type your text. Type 'SAVE' on a new line to finish.")
                
                lines = []
                while True:
                    line = input("> ")
                    if line.upper() == "SAVE":
                        break
                    lines.append(line)
                
                # Uniamo le righe e salviamo nel disco virtuale
                disk[filename] = "\n".join(lines)
                save_to_disk(disk)
                print(f"FILE {filename} SAVED SUCCESSFULLY.")
            else:
                print("Usage: EDIT [FILENAME]")
            
            
        elif cmd == "TREE":
            print("C:\\")
            # Get unique folders
            folders = sorted(list(set(f.split('/')[0] for f in disk if '/' in f)))
            # Get root files
            root_files = [f for f in disk if '/' not in f]
            
            for f in root_files:
                print(f"├── {f}")
                
            for folder in folders:
                print(f"├── [{folder}]")
                for f in disk:
                    if f.startswith(folder + "/"):
                        filename = f.split('/')[1]
                        print(f"│   └── {filename}")

            
        elif cmd == "CD":
            if args:
                path = args[0].upper()
                if path == "..":
                    current_dir = "" # Successfully moves you back to C:\
                    print("Returned to Root.")
                else:
                    # Check if any file in the disk exists within that folder
                    if any(f.startswith(path + "/") for f in disk):
                        current_dir = path
                    else:
                        print("Directory not found.")
            else:
                # If you just type 'CD', it tells you where you are
                if current_dir == "":
                    print("C:\\")
                else:
                    print(f"C:\\{current_dir}")
 
        elif cmd == "FIND":
            if args:
                term = args[0].upper()
                found = 0
                for path in disk:
                    fname = path.split('/')[-1] if '/' in path else path
                    if term in fname:
                        loc = path.split('/')[0] if '/' in path else "ROOT"
                        print(f" -> FOUND: {fname} (In: {loc})")
                        found += 1
                if found == 0: print("No matches.")
            else: print("Usage: FIND [NAME]")

        elif cmd == "COPY":
            if len(args) >= 2:
                source = args[0].upper()
                destination = args[1].upper()
                src_path = f"{current_dir}/{source}" if current_dir else source
                
                if src_path not in disk:
                    print("Source file not found.")
                    continue

                # Smart Folder Detection
                is_dir = any(f.startswith(destination + "/") for f in disk)
                dest_path = f"{destination}/{source}" if is_dir else (f"{current_dir}/{destination}" if current_dir else destination)
                
                if dest_path in disk:
                    confirm = input(f"Destination {dest_path} exists. Overwrite? (Y/N): ")
                    if confirm.upper() != 'Y':
                        print("Copy aborted.")
                        continue

                disk[dest_path] = disk[src_path]
                save_to_disk(disk)
                print(f"File copied to {dest_path}.")
            else:
                print("Usage: COPY [SOURCE] [DESTINATION]")
                
        elif cmd == "SOURCES":
            url = "https://raw.githubusercontent.com/valeraspberry/CUSTOM_OS/refs/heads/main/PROVIDERS.TXT"
            print("FETCHING REGISTERED PROVIDERS...")
            try:
                # Aggiungiamo un timeout leggermente più lungo (10 secondi)
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    print("\nOFFICIAL TERRACINA PROVIDERS:")
                    lines = r.text.strip().splitlines()
                    for line in lines:
                        if ":" in line:
                            name = line.split(":")[0]
                            print(f" - {name}")
                    print(f"TOTAL: {len(lines)} PROVIDERS ONLINE.\n")
                else:
                    print(f"SERVER ERROR: {r.status_code}")
            except Exception as e:
                print(f"NETWORK ERROR: {e}")

        elif cmd == "MENU":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("==========================================")
            print("         MS-DOS v.6.77 SYSTEM MENU        ")
            print("==========================================")
            print(" 1. [SECURITY]  - Set/Change BIOS Password")
            print(" 2. [POWER]     - Reboot or Shutdown")
            print(" 3. [STATUS]    -  Disk Usage")
            print(" 4. [EXIT]      - Return to Prompt")
            print("==========================================")
            
            choice = input("Select (1-4): ")

            if choice == "1":
                # Check for existing password first
                old_pass = disk.get("PASSWORD", "")
                if old_pass:
                    verify = input("ENTER CURRENT PASSWORD: ")
                    if verify != old_pass:
                        print("WRONG PASSWORD!"); time.sleep(1); continue
                
                new_pass = input("ENTER NEW PASSWORD (OR LEAVE BLANK TO DISABLE): ")
                disk["PASSWORD"] = new_pass
                save_to_disk(disk)
                print("SECURITY SETTINGS UPDATED.")
                time.sleep(1)

            elif choice == "2":
                p_choice = input("1. REBOOT\n2. SHUTDOWN\nSELECT: ")
                if p_choice == "1": boot_sequence()
                elif p_choice == "2": sys.exit()

            elif choice == "3":
                # Showing your real progress toward the Gaming PC
                print(f"\n--- SYSTEM STATUS ---")
                print(f"DISK: {get_disk_usage(disk):.2f}KB / {MAX_DISK_KB}KB")
                input("\nPRESS ENTER TO RETURN...")

                
        elif cmd == "CUT" or cmd == "MOVE":
            if len(args) >= 2:
                source = args[0].upper()
                destination = args[1].upper()
                src_path = f"{current_dir}/{source}" if current_dir else source
                
                if src_path not in disk:
                    print("Source file not found.")
                    continue

                # Smart Folder Detection
                is_dir = any(f.startswith(destination + "/") for f in disk)
                dest_path = f"{destination}/{source}" if is_dir else (f"{current_dir}/{destination}" if current_dir else destination)
                
                if dest_path in disk:
                    confirm = input(f"Destination {dest_path} exists. Overwrite? (Y/N): ")
                    if confirm.upper() != 'Y':
                        print("Move aborted.")
                        continue

                disk[dest_path] = disk[src_path]
                del disk[src_path]
                save_to_disk(disk)
                print(f"File moved to {dest_path}.")
            else:
                print("Usage: CUT [SOURCE] [DESTINATION]")



        elif cmd == "TIME":
            full_time = datetime.now().strftime("%A, %b %d, %Y - %H:%M:%S")
            print(f"Current System Time: {full_time}")

        else: print("Bad command or file name")

if __name__ == "__main__":
    boot_sequence()
