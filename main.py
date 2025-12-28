import concurrent.futures
import os
import sys

from tqdm import tqdm

from config.presets import PRESETS
from config.settings import DEFAULT_WORKERS
from core.hardware import detect_gpu_codec
from core.processor import process_file


def clean_path(path_str):
    """Removes quotes typically added when dragging and dropping files."""
    return path_str.strip().strip('"').strip("'")


def select_preset():
    print("\nSelect Compression Preset:")
    # Sort keys to ensure they appear in order (1, 2, 3...)
    sorted_keys = sorted(PRESETS.keys())

    for key in sorted_keys:
        val = PRESETS[key]
        print(f"[{key}] {val['name']}")
        print(f"    └─ {val['description']}")

    # Create a dynamic prompt string (e.g., "1/2/3/4/5")
    options_str = "/".join(sorted_keys)
    choice = input(f"\nEnter choice ({options_str}): ").strip()

    return PRESETS.get(choice)


def main():
    print("==========================================")
    print("      MASS VIDEO COMPRESSOR (MVC)         ")
    print("==========================================\n")

    preset = select_preset()
    if not preset:
        print("Invalid selection. Exiting.")
        return

    print("\n(Tip: Drag and drop folders into this window)")
    source_folder = clean_path(input("Source Folder: "))
    dest_folder = clean_path(input("Output Folder: "))

    if not os.path.exists(source_folder):
        print(f"Error: Source folder does not exist: {source_folder}")
        return

    if not os.path.exists(dest_folder):
        print(f"Creating output folder: {dest_folder}")
        os.makedirs(dest_folder)

    gpu_codec = None
    if preset["use_gpu"]:
        print("  ⚙ Analyzing Hardware...")
        gpu_codec = detect_gpu_codec()
        if gpu_codec:
            print(f"✔ GPU Accelerated: Using {gpu_codec}")
        else:
            print("⚠ GPU requested but not found. Falling back to CPU.")

    files = [f for f in os.listdir(source_folder) if f.lower().endswith(".mp4")]
    if not files:
        print("No .mp4 files found.")
        return

    tasks = []
    for f in files:
        tasks.append(
            (os.path.join(source_folder, f), os.path.join(dest_folder, f), f, preset, gpu_codec)
        )

    print(f"\nProcessing {len(files)} files with {DEFAULT_WORKERS} threads...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=DEFAULT_WORKERS) as executor:
        futures = {executor.submit(process_file, task): task for task in tasks}
        pbar = tqdm(
            concurrent.futures.as_completed(futures), total=len(tasks), unit="file", mininterval=0.5
        )
        for _ in pbar:
            pass

    print("\nAll tasks finished.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
