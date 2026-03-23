#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import shutil
import json
from pathlib import Path

def run_cmd(cmd, check=True):
    print(f">>> {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def detect_os():
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    else:
        return "unknown"

def install_dependencies(os_name):
    # Python packages
    run_cmd(f"{sys.executable} -m pip install --upgrade pip")
    run_cmd(f"{sys.executable} -m pip install -r requirements.txt")

    # OS-specific system dependencies
    if os_name == "linux":
        run_cmd("sudo apt update")
        run_cmd("sudo apt install -y espeak ffmpeg portaudio19-dev python3-dev")
    elif os_name == "macos":
        run_cmd("brew install espeak ffmpeg portaudio")
    elif os_name == "windows":
        # No system packages needed for basic install; user may need to install espeak manually
        print("Windows: Ensure espeak is installed (https://github.com/espeak-ng/espeak-ng)")

def download_local_llm():
    # Use Ollama to pull model if not present
    model_name = "llama3.1:8b"
    result = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
    if model_name not in result.stdout:
        print(f"Pulling local LLM {model_name} with Ollama...")
        run_cmd(f"ollama pull {model_name}")
    else:
        print(f"Local LLM {model_name} already present.")

def setup_env():
    # Create virtual environment
    venv_dir = Path(".venv")
    if not venv_dir.exists():
        run_cmd(f"{sys.executable} -m venv .venv")
    # Activate and install dependencies
    if os.name == "nt":
        python_venv = ".venv\\Scripts\\python"
    else:
        python_venv = ".venv/bin/python"
    run_cmd(f"{python_venv} -m pip install --upgrade pip")
    run_cmd(f"{python_venv} -m pip install -r requirements.txt")

def main():
    os_name = detect_os()
    print(f"Detected OS: {os_name}")

    # Ensure Python 3.10+
    if sys.version_info < (3, 10):
        print("Python 3.10 or higher is required.")
        sys.exit(1)

    # Install dependencies
    install_dependencies(os_name)
    setup_env()
    download_local_llm()

    # Create config from template
    if not os.path.exists("core/config.py"):
        shutil.copy("core/config_template.py", "core/config.py")
        print("Created config.py. Please edit with your API keys if needed.")

    print("Installation complete! Run 'python main.py' to start Stormy.")

if __name__ == "__main__":
    main()
