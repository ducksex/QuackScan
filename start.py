import os
import subprocess
import venv
import sys

ENV_DIR = "venv"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def create_venv():
    if not os.path.exists(ENV_DIR):
        print(f"Creating virtual environment in {ENV_DIR}...")
        venv.create(ENV_DIR, with_pip=True)
    else:
        print(f"Virtual environment {ENV_DIR} already exists.")

def install_dependencies():
    print("Installing dependencies from requirements.txt if present...")
    pip = os.path.join(ENV_DIR, "Scripts" if os.name == "nt" else "bin", "pip")
    if os.path.exists("requirements.txt"):
        subprocess.check_call([pip, "install", "-r", "requirements.txt"])
    else:
        print("No requirements.txt found. Skipping dependency installation.")

def pip_install_package():
    print("Installing quackscan package into the virtual environment...")
    pip = os.path.join(ENV_DIR, "Scripts" if os.name == "nt" else "bin", "pip")
    subprocess.check_call([pip, "install", "."])

def run_quackscan():
    print("Launching QuackScan...")
    python_exe = os.path.join(ENV_DIR, "Scripts" if os.name == "nt" else "bin", "python")
    subprocess.run([python_exe, "-m", "quackscan"] + sys.argv[1:])

def main():
    clear_screen()
    create_venv()
    clear_screen()
    install_dependencies()
    clear_screen()
    pip_install_package()
    clear_screen()
    run_quackscan()

if __name__ == "__main__":
    main()
