import os
import re
import sys


def validate_version(version_str):
    """
    Validate that a version string is non-empty and matches the numeric pattern `major.minor` or `major.minor.patch`.
    
    Parameters:
    	version_str (str): Version string to validate; expected format is digits.digits or digits.digits.digits (e.g., "3.8" or "3.8.10"). On invalid input the function prints an error message and exits the process with status code 1.
    """
    if not version_str:
        print("Error: Version argument is empty.")
        sys.exit(1)
    if not re.match(r"^\d+\.\d+(?:\.\d+)?$", version_str):
        print(f"Error: Invalid version format '{version_str}'.")
        sys.exit(1)


def update_readme(min_version, max_version, file_path="README.md"):
    # 1. Validate Inputs
    """
    Update the README's "Prerequisites: Python" line to a specified version or version range.
    
    Validates the provided min_version and max_version, computes a display string (uses a single version when they are equal, otherwise "min_version - max_version"), and replaces the existing prerequisites line in the README at file_path with that string. On success the README is rewritten only if its content changed.
    
    Parameters:
        min_version (str): Minimum Python version to set in the README (e.g., "3.10").
        max_version (str): Maximum Python version to set in the README (e.g., "3.13").
        file_path (str): Path to the README file to update. Defaults to "README.md".
    
    Notes:
        - Exits the process with status 1 if a version is invalid, the README file is missing, or the expected "Prerequisites" line cannot be found.
    """
    validate_version(min_version)
    validate_version(max_version)

    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

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

    # Replace with new version range
    new_content = re.sub(pattern, lambda m: f"{m.group(1)}{version_string}{m.group(3)}", content)

    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md updated successfully.")
    else:
        print("README.md already up to date.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update_readme.py <min_version> <max_version>")
        sys.exit(1)
    update_readme(sys.argv[1], sys.argv[2])