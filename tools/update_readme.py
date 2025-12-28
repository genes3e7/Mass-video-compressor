import os
import re
import sys


def validate_version(version_str):
    """
    Validate that a version string is non-empty and matches the numeric pattern.

    Expected format: `major.minor` or `major.minor.patch`.

    Parameters:
        version_str (str): Version string (e.g., "3.8" or "3.8.10").

    Raises:
        ValueError: If version_str is empty or has invalid format.
    """
    if not version_str:
        raise ValueError("Version argument is empty.")
    if not re.match(r"^\d+\.\d+(?:\.\d+)?$", version_str):
        raise ValueError(f"Invalid version format '{version_str}'.")


def update_readme(min_version, max_version, file_path="README.md"):
    """
    Update the README's "Prerequisites: Python" line to a specified version or version range.

    Computes a display string (single version if equal, range otherwise) and updates the file.

    Parameters:
        min_version (str): Minimum Python version (e.g., "3.10").
        max_version (str): Maximum Python version (e.g., "3.13").
        file_path (str): Path to the README file. Defaults to "README.md".

    Notes:
        Exits with status 1 if a version is invalid, file missing, or pattern not found.
    """
    # 1. Validate Inputs
    validate_version(min_version)
    validate_version(max_version)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except IOError as e:
        print(f"Error reading {file_path}: {e}")
        sys.exit(1)

    # Determine string format (e.g., "3.10" or "3.10 - 3.13")
    if min_version == max_version:
        version_string = min_version
    else:
        version_string = f"{min_version} - {max_version}"

    print(f"Updating README to support Python: {version_string}")

    # Regex to find "**Prerequisites:** Python X.X"
    pattern = (
        r"(\*\*Prerequisites:\*\* Python )"
        r"(\d+\.\d+(?:\.\d+)?(?: - \d+\.\d+(?:\.\d+)?)?)(.*)"
    )

    if not re.search(pattern, content):
        print("Critical: Could not find 'Prerequisites' line in README.")
        sys.exit(1)

    def _replace_match(m):
        return f"{m.group(1)}{version_string}{m.group(3)}"

    # Replace with new version range
    new_content = re.sub(pattern, _replace_match, content)

    if new_content != content:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("README.md updated successfully.")
        except IOError as e:
            print(f"Error writing to {file_path}: {e}")
            sys.exit(1)
    else:
        print("README.md already up to date.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update_readme.py <min_version> <max_version>")
        sys.exit(1)

    try:
        update_readme(sys.argv[1], sys.argv[2])
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)
