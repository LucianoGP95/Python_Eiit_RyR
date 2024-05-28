### Script to quickly set desired software into a dektop folder.
### Run after cloning the repository in your PC.

import os
import shutil
import getpass

def copytree_overwrite(source, target):
    '''Wrapper function to delete the destination folder and copy the desired files over it'''
    try:
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(source, target)
        os.remove(os.path.join(target, "_prepare_software.py"))
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

    if create_venv():
        print(f"Success: Venv created in {target}")
    else:
        print("Error: Unable to create venv.")

def create_venv():
    '''Tries to execute a PowerShell script to create a Python env'''
    script_path = os.path.join("C:\\Users", getpass.getuser(), "Powershell", "Scripts", "PythonVenv.ps1")
    try:
        exec(open(script_path).read())
        print("Creating venv")
        return True
    except OSError as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    main()
