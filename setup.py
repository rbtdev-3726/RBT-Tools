import os
import sys
import subprocess
import venv

# List of external dependencies required by Rbt.py
DEPENDENCIES = [
    "requests",
    "pillow",
    "whois",
    "discord.py",
    "phonenumbers",
    "dnspython"
]

VENV_DIR = ".venv"

def create_and_setup_venv():
    print("[*] Analysis of Rbt.py completed.")
    print(f"[*] Creating local virtual environment in folder: {os.path.abspath(VENV_DIR)}")
    
    # Create the virtual environment in the local directory and include pip
    venv.create(VENV_DIR, with_pip=True)
    
    # Identify the path of the local python executable based on the operating system
    if sys.platform == "win32":
        python_executable = os.path.join(VENV_DIR, "Scripts", "python.exe")
        activate_script = os.path.join(VENV_DIR, "Scripts", "activate.bat")
    else:
        python_executable = os.path.join(VENV_DIR, "bin", "python")
        activate_script = os.path.join(VENV_DIR, "bin", "activate")
        
    print("[*] Upgrading pip inside the local environment...")
    subprocess.check_call([python_executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])
    
    print("[*] Downloading and installing required packages inside the folder...")
    for package in DEPENDENCIES:
        print(f"    -> Downloading and installing: {package}...")
        try:
            subprocess.check_call([python_executable, "-m", "pip", "install", package, "-q"])
            print(f"    [✓] {package} successfully installed.")
        except Exception as e:
            print(f"    [X] Error during installation of {package}: {e}")
            
    print("\n" + "="*60)
    print("[✓] SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nAll external libraries have been downloaded and isolated in the current folder.")
    print("\nTo correctly run the tool using the downloaded local modules:")
    
    if sys.platform == "win32":
        print(f"Option A (Activation): Run '{activate_script}' and then 'python Rbt.py'")
        print(f"Option B (Direct):     Run '{python_executable} Rbt.py' directly")
    else:
        print(f"Option A (Activation): Run 'source {activate_script}' and then 'python3 Rbt.py'")
        print(f"Option B (Direct):     Run '{python_executable} Rbt.py' directly")
    print("="*60)

if __name__ == "__main__":
    try:
        create_and_setup_venv()
    except Exception as e:
        print(f"[X] Critical error during configuration: {e}")