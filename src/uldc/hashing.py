import hashlib
from pathlib import Path


def get_file_hash(path: Path) -> str:
    """Computes the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except IOError:
        return ""


def get_unique_filename(destination_path: Path) -> Path:
    """Generates a unique filename by appending a number if the file already exists."""
    if not destination_path.exists():
        return destination_path

    parent, stem, suffix = destination_path.parent, destination_path.stem, destination_path.suffix
    counter = 1
    while (new_path := parent / f"{stem}_{counter}{suffix}").exists():
        counter += 1
    return new_path