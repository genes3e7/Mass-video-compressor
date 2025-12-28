"""
build.py
freezes the application into a standalone executable using PyInstaller.
"""

import os
import shutil

import PyInstaller.__main__


def build():
    # 1. Clean previous build artifacts
    print("Cleaning previous builds...")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    print("Building Mass Video Compressor...")

    # 2. Run PyInstaller
    # --onefile: Create a single .exe file
    # --console: Keep the command line window open (Required for CLI tools)
    # --name: Name of the output file
    # --hidden-import: Ensure imageio_ffmpeg binaries are found if necessary
    PyInstaller.__main__.run(
        [
            "main.py",
            "--name=MVC_Compressor",
            "--onefile",
            "--console",
            "--clean",
            # Explicitly tell PyInstaller to look for our local modules if it misses them
            "--paths=.",
            # Add data or hidden imports if specific libraries fail to load
            "--hidden-import=tqdm",
            "--hidden-import=imageio_ffmpeg",
        ]
    )

    print("\n------------------------------------------------")
    print("Build Complete!")
    print(f"Executable is located at: {os.path.abspath('dist')}")
    print("------------------------------------------------")


if __name__ == "__main__":
    build()
