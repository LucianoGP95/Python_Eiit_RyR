### Version 1.0: 07/06/2024

### Script to quickly sets the parent folder software into a Desktop folder.
### Run after cloning the repository in your PC.

import os
import shutil
import getpass
import subprocess

def copytree_overwrite(source, target):
    '''Wrapper function to delete the destination folder and copy the desired files over it'''
    try:
        if os.path.exists(target):
            print("Copying files")
            shutil.rmtree(target)
        shutil.copytree(source, target)
        os.remove(os.path.join(target, "_prepare_software.py"))
        return True
    except OSError as e:
        print(f"Error: {e}")
        return False

def create_venv(target):
    '''Tries to execute a PowerShell script to create a Python env'''
    script_path = os.path.join("C:\\Users", getpass.getuser(), "Powershell", "Scripts", "PythonVenv.ps1")
    try:
        os.chdir(target)
        print("Creating venv")
        subprocess.run(["powershell.exe", "-File", script_path])
        return True
    except OSError as e:
        print(f"Error: {e}")
        return False

def main():
    source = os.path.dirname(os.path.abspath(__file__))
    username = getpass.getuser()
    target = os.path.join("C:\\Users", username, "Desktop", "Analyser")

    if copytree_overwrite(source, target):
        print(f"Success: Files copied to {target}")
    else:
        print("Error: Unable to copy files.")

    if create_venv(target):
        print(f"Success: Venv created in {target}")
    else:
        print("Error: Unable to create venv.")

if __name__ == "__main__":
    main()
