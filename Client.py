import os
import re
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
from datetime import datetime
import json
from flask import Flask
import subprocess
import sys
import requests



# Directories
defaultsSettings = data = '''
{
  "DROPBOX_SECRET": null,
  "DROPBOX_KEY": null,
  "DROPBOX_ACCESS_TOKEN": null,
  "DROPBOX_REFRESH_TOKEN": null,
  "AIRTABLE_API_KEY": null,
  "AIRTABLE_BASE_KEY": null,
  "AIRTABLE_TABLE_NAME": null,
  "AIRTABLE_URL":  null,
  "CONTENT_SOURCE": null,
  "THUMB_DEPOT": null,
  "THUMB_DEPOT_LOCAL": null,
  "THUMB_DB_PATH": null,
  "REPORTS_DIR": null
}
'''
defaults =json.loads(defaultsSettings)
settingsPath = 'secrets.json'

with open('secrets.json', 'r') as json_file:
    data = json.load(json_file)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = data["REPORTS_DIR"]
IGNORE_FILE = os.path.join(SCRIPT_DIR, r"ignored_folders.json")
os.makedirs(REPORTS_DIR, exist_ok=True)

FILENAME_PATTERN = re.compile(r"^(\d{3})_(.+)_v(\d{2,})(?:_frame\d+)?\..+$")
STOREFILE = re.compile(r'.DS_Store')
print(IGNORE_FILE)
# Store ignored folders here (relative to root_dir)
ignored_folders = []


        
def load_secrets():
    if os.path.exists(settingsPath):
        with open(settingsPath, "r") as f:
            return json.load(f)
    return {}

def save_secrets(secrets):
    with open(settingsPath, "w") as f:
        json.dump(secrets, f, indent=4)

def choose_thumbnail_directory():
    path = filedialog.askdirectory()
    if path:
        thumb_var.set(path)
        secrets = load_secrets()
        secrets["THUMB_DEPOT_LOCAL"] = path
        save_secrets(secrets)

def choose_reports_directory():
    path = filedialog.askdirectory()
    if path:
        reports_var.set(path)
        secrets = load_secrets()
        secrets["REPORTS_DIR"] = path
        save_secrets(secrets)
        

def analyze_filenames(root_dir):
    issues = []
    prefix_map = {}

    for dirpath, _, filenames in os.walk(root_dir):
        relative_dirpath = os.path.relpath(dirpath, root_dir)

        # Skip ignored folders
        if any(relative_dirpath.startswith(ignored) for ignored in ignored_folders):
            continue

        for filename in filenames:
            if filename == ".DS_Store":
                continue
                
            filepath = os.path.join(dirpath, filename)
            relpath = os.path.relpath(filepath, root_dir)
            
            match = FILENAME_PATTERN.match(filename)
            if not match:
                issues.append((relpath, "", "Filename format is invalid"))
                continue

            prefix, base, version = match.groups()

            folder_key = relative_dirpath
            if folder_key not in prefix_map:
                prefix_map[folder_key] = {}

            if prefix not in prefix_map[folder_key]:
                prefix_map[folder_key][prefix] = {base: [relpath]}
            else:
                if base in prefix_map[folder_key][prefix]:
                    prefix_map[folder_key][prefix][base].append(relpath)
                else:
                    conflicting_files = [
                        f for files in prefix_map[folder_key][prefix].values() for f in files
                    ]
                    issues.append((
                        relpath,
                        "; ".join(conflicting_files),
                        f"Prefix {prefix} reused with different base name"
                    ))
                    prefix_map[folder_key][prefix][base] = [relpath]

    return issues
    print(REPORTS_DIR)

def write_csv_report(issues, REPORTS_DIR):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"filename_issues_report_{timestamp}.csv"
    full_path = os.path.join(REPORTS_DIR, output_file)

    with open(full_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Problem File", "Conflicts With", "Issue"])
        writer.writerows(issues)
    
    return full_path
    print("Writing file" + full_path)

def open_csv(REPORTS_DIR):
    webbrowser.open(f'file://{os.path.abspath(REPORTS_DIR)}')

def show_popup(is_good):
    popup = tk.Tk()
    popup.withdraw()
    if is_good:
        messagebox.showinfo("Result: ✅ GO", "All files passed!")
    else:
        messagebox.showerror("Result: ❌ NO GO", "Issues found! See the report for details.")

def run_analysis(selected_dir):
    issues = analyze_filenames(selected_dir)
    report_path = write_csv_report(issues, REPORTS_DIR)
#    open_csv(report_path)
    show_popup(is_good=(len(issues) == 0))
    print(report_path)

# GUI actions for ignore list
def choose_directory():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        dir_var.set(selected_dir)
        load_ignored_folders(IGNORE_FILE)

def add_ignored_folder():
    root = dir_var.get()
    if not root:
        messagebox.showwarning("Select root", "Please select a root directory first.")
        return

    selected = filedialog.askdirectory(initialdir=root)
#    if selected and os.path.commonpath([selected, root]) == root:
    relative = os.path.relpath(selected, root)
    if relative not in ignored_folders:
        ignored_folders.append(relative)
        update_ignore_listbox()
        save_ignored_folders(IGNORE_FILE)
        print("Directory" + relative + "ignored.")

def remove_selected_ignored():
    selected_indices = ignore_listbox.curselection()
    for i in reversed(selected_indices):
        ignored_folders.pop(i)
    update_ignore_listbox()
    save_ignored_folders(IGNORE_FILE)
    print(f"[DEBUG] Data being saved: {ignored_folders}")

def start_analysis():
    selected_dir = dir_var.get()
    if not os.path.isdir(selected_dir):
        messagebox.showerror("Error", "Please select a valid directory.")
        return
    run_analysis(selected_dir)
    create_new_files_report(selected_dir) #Delete this line if shit breaks

def get_ignore_file_path(IGNORE_FILE):
    return os.path.join(IGNORE_FILE, "ignored_folders.json")
    print(IGNORE_FILE)

def load_ignored_folders(IGNORE_FILE):
    ignored_folders.clear()
    ignore_file = IGNORE_FILE
    print(f"[DEBUG] Trying to load ignored folders from: {ignore_file}")
    if os.path.isfile(ignore_file):
        try:
            with open(ignore_file, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    ignored_folders.extend(data)
                    print(f"[DEBUG] Loaded ignored folders: {ignored_folders}")
                else:
                    print("[ERROR] Ignored file format is invalid.")
                    messagebox.showerror("Error", "ignored_folders.json is not a valid list.")
        except json.JSONDecodeError:
            print("[ERROR] Failed to parse ignored_folders.json")
            messagebox.showerror("Error", "Could not parse ignored_folders.json (invalid format).")
    else:
        print("[DEBUG] No ignored_folders.json found. Starting with empty ignore list.")
    update_ignore_listbox()

def save_ignored_folders(IGNORE_FILE):
    ignore_file = IGNORE_FILE
    try:
        with open(ignore_file, "w") as f:
            json.dump(ignored_folders, f, indent=2)
        print(f"[DEBUG] Saved ignored folders to: {ignore_file}")
    except Exception as e:
        print(f"[ERROR] Could not save ignored folders: {e}")
        messagebox.showerror("Error", f"Could not save ignore list:\n{e}")

def update_ignore_listbox():
    ignore_listbox.delete(0, tk.END)
    for folder in ignored_folders:
        ignore_listbox.insert(tk.END, folder)

##############################################################
#WHATS NEW ANALYZER HERE
def get_file_creation_time(path):
    return os.path.getctime(path)

def scan_all_files(root_dir):
    file_data = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            full_path = os.path.join(dirpath, file)
            try:
                ctime = get_file_creation_time(full_path)
                rel_path = os.path.relpath(full_path, root_dir)
                file_data[rel_path] = ctime
            except:
                pass  # skip unreadable files
    return file_data

def load_previous_seen():
    seen_path = os.path.join(REPORTS_DIR, "seen_files.json")
    if os.path.isfile(seen_path):
        with open(seen_path, "r") as f:
            return json.load(f)
    return {}

def save_seen_file_list(file_data):
    seen_path = os.path.join(REPORTS_DIR, "seen_files.json")
    with open(seen_path, "w") as f:
        json.dump(file_data, f, indent=2)

def create_new_files_report(root_dir):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = os.path.join(REPORTS_DIR, f"whats_new_{now}.csv")

    prev_seen = load_previous_seen()
    current_files = scan_all_files(root_dir)

    # Detect new files
    new_files = {
        path: ts for path, ts in current_files.items()
        if path not in prev_seen
    }

    # Sort by creation time (descending)
    sorted_new = sorted(new_files.items(), key=lambda x: x[1], reverse=True)

    with open(csv_filename, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Created Date"])
        for path, ts in sorted_new:
            created_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([path, created_str])

    # Save updated seen list
    save_seen_file_list(current_files)

    print(f"New files CSV saved to: {csv_filename}")
    return csv_filename
#######BUILD CONTENT MASTER TABLE HERE######
def build():
    subprocess.run(['python', '_MGMTLocal.py'])
    
#############BUILD AIRTABLE PUSH HERE (Not Working)    
def airtable():
    subprocess.run(['python', '_GUI.py'])
    
##############################################################
def run():
    print("IT IS RUNNING")
    global app, dir_var, thumb_var, reports_var, ignore_listbox

    app = tk.Tk()
    app.title("Content Dash Local Client")
    app.geometry("800x600")
    app.resizable(False, False)

    dir_var = tk.StringVar()
    thumb_var = tk.StringVar()
    reports_var = tk.StringVar()

    secrets = load_secrets()
    
    dir_var.set(secrets.get("CONTENT_SOURCE", ""))
    thumb_var.set(secrets.get("THUMB_DEPOT_LOCAL", ""))
    reports_var.set(secrets.get("REPORTS_DIR", ""))

    frame = tk.Frame(app, padx=10, pady=10)
    frame.pack(fill="both", expand=False)

    label = tk.Label(frame, text="Select root directory to analyze:")
    label.pack(anchor="w")

    entry_frame = tk.Frame(frame)
    entry_frame.pack(fill="x", expand=True)

    entry = tk.Entry(entry_frame, textvariable=dir_var, width=60)
    entry.pack(side="left", fill="x", expand=True)

    browse_btn = tk.Button(entry_frame, text="Browse...", command=choose_directory)
    browse_btn.pack(side="right")
    
    # --- New Thumbnail Directory Input ---
    thumb_label = tk.Label(app, text=r"Select server static\images\ directory:")
    thumb_label.pack(anchor="w", padx=10)

    thumb_frame = tk.Frame(app)
    thumb_frame.pack(fill="x", padx=10)

    thumb_entry = tk.Entry(thumb_frame, textvariable=thumb_var, width=60)
    thumb_entry.pack(side="left", fill="x", expand=True)

    thumb_browse_btn = tk.Button(thumb_frame, text="Browse...", command=choose_thumbnail_directory)
    thumb_browse_btn.pack(side="right")
    # --------------------------------------
    
    # --- Reports Directory ---
    reports_label = tk.Label(app, text="Select reports output directory:")
    reports_label.pack(anchor="w", padx=10)

    reports_frame = tk.Frame(app)
    reports_frame.pack(fill="x", padx=10)

    reports_entry = tk.Entry(reports_frame, textvariable=reports_var, width=60)
    reports_entry.pack(side="left", fill="x", expand=True)

    reports_browse_btn = tk.Button(reports_frame, text="Browse...", command=choose_reports_directory)
    reports_browse_btn.pack(side="right")
    
    #----Ignore Folders-------------------
    ignore_label = tk.Label(app, text="Ignored Subdirectories (relative to root):")
    ignore_label.pack(anchor="w", padx=10)

    ignore_listbox = tk.Listbox(app, height=8, width=80)
    ignore_listbox.pack(padx=10, pady=5)

    ignore_buttons = tk.Frame(app)
    ignore_buttons.pack()

    add_ignore_btn = tk.Button(ignore_buttons, text="➕ Add Folder to Ignore", command=add_ignored_folder)
    add_ignore_btn.pack(side="left", padx=5)

    remove_ignore_btn = tk.Button(ignore_buttons, text="➖ Remove Selected", command=remove_selected_ignored)
    remove_ignore_btn.pack(side="left", padx=5)

    analyze_btn = tk.Button(app, text="Start Analysis", command=start_analysis, bg="blue", fg="white", height=2)
    analyze_btn.pack(pady=20)
    analyze_btn = tk.Button(app, text="Build Table", command=build, bg="blue", fg="white", height=2)
    analyze_btn.pack(pady=0)
    analyze_btn = tk.Button(app, text="Build Airtable", command=airtable, bg="blue", fg="white", height=4)
    analyze_btn.pack(side="right", padx=50, pady=0)

    app.mainloop()




if __name__ == '__main__':

    run()