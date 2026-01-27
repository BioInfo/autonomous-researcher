#!/usr/bin/env python3
"""CLI wrapper that ensures venv exists before running main.py."""

import subprocess
import sys
import os
from pathlib import Path


def ensure_venv(root_dir):
    """Ensure a virtual environment exists and is used."""
    venv_dir = root_dir / "venv"
    venv_python = venv_dir / "bin" / "python"

    # If we are already running in the venv, continue
    if sys.prefix == str(venv_dir):
        return sys.executable

    # Create venv if it doesn't exist
    if not venv_dir.exists():
        print("[SETUP] Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=root_dir, check=True)

        # Install requirements
        print("[SETUP] Installing dependencies...")
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "-q", "-r", "requirements.txt"],
            cwd=root_dir,
            check=True,
        )

    # Re-execute this script using the venv python
    print("[SETUP] Switching to virtual environment...")
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)


def main():
    root_dir = Path(__file__).parent.resolve()

    # Ensure venv before proceeding
    ensure_venv(root_dir)

    # Forward all args to main.py
    main_py = root_dir / "main.py"
    args = [sys.executable, str(main_py)] + sys.argv[1:]

    os.execv(sys.executable, args)


if __name__ == "__main__":
    main()
