from pathlib import Path
BASE = Path(r"c:\Users\scott\Documents\Image-Line\FL Studio Mobile")

def find_strings(filepath: str | Path, min_length: int = 4) -> list[str]:
    """
    Find all ASCII strings in a binary file, similar to the Unix `strings` command.

    Args:
    filepath: Path to the binary file.
    min_length: Minimum string length to include (default: 4).

    Returns:
    List of ASCII strings found in the file.
    """
    filepath = Path(filepath).resolve()
    results = []
    current = []

    with open(filepath, "rb") as f:
        for byte in f.read():
            if 0x20 <= byte < 0x7F:  # printable ASCII range
                current.append(chr(byte))
            else:
                if len(current) >= min_length:
                    results.append("".join(current))
                current = []

    # Catch any string still in progress at EOF
    if len(current) >= min_length:
        results.append("".join(current))

    return results

def _get_interesting(strings):
    strings = [s for s in strings if "/" in s or "\\" in s]
    # strings = [s for s in strings if not s.startswith("Resources")]  # strip ^Resources as these paths are often duplicated elsewhere
    # strings = [s for s in strings if not s.startswith("/storage/emulated") and not s.startswith("C:\\")]  # these are often duplicated elsewhere
    return strings


def _has_interesting_extension(s) -> str | None:
    """These are extensions that identify interesting strings inside raw binary data"""
    extensions = [".wav", ".dwp", ".flmpst", ".flgsynth", ".flm", ".flms", ".fst", ".tmpl", ".mp3", ".flac"]
    lower = s.lower()
    for ext in extensions:
        idx = lower.find(ext)
        if idx != -1:
            return s[idx:idx + len(ext)]  # actual extension from s, preserving its original case
    return None


def _clean_trailing_ascii(s):
    if ext :=_has_interesting_extension(s):
        idx = s.rfind(ext)
        return s[:idx+len(ext)]
    return s


def find_strings_lvl2(filepath: str | Path) -> list[str]:
    strings = find_strings(filepath)
    strings = _get_interesting(strings)
    return sorted(set(strings))  # uniqueify and sort


def find_strings_lvl3(filepath: str | Path):
    strings = find_strings_lvl2(filepath)
    strings = [s for s in strings if _has_interesting_extension(s)]
    strings = [_clean_trailing_ascii(s) for s in strings]
    return sorted(set(strings))  # uniqueify and sort


CATEGORY_DIRS = ["My Drumsets", "My Instruments", "My Presets", "My Racks", "My Songs"]


def _find_data_root(filepath: Path) -> Path | None:
    """Walk up from filepath until a directory containing both "My Songs" and
    "My Recordings" subdirs is found. Return that directory, or None."""
    for parent in filepath.parents:
        if (parent / "My Songs").is_dir() and (parent / "My Recordings").is_dir():
            return parent
    return None


def find_parents(filepath: str | Path) -> set[str]:
    """Return the set of files that reference the given file.

    Locates the data_root by walking up from filepath, enumerates the files
    (one level deep) in the category directories, and returns any whose
    extracted strings reference filepath's name.
    """
    filepath = Path(filepath).resolve()
    data_root = _find_data_root(filepath)
    if data_root is None:
        raise Exception(f"Unable to find FL Studio Mobile data root at or above {filepath}")

    target = filepath.name
    parents = set()
    for category in CATEGORY_DIRS:
        category_dir = data_root / category
        if not category_dir.is_dir():
            raise Exception("The expected subdirectory ({category}) does not exist")
        for candidate in category_dir.rglob("*"):
            if not candidate.is_file() or candidate == filepath:
                continue
            if any(target in s for s in find_strings_lvl3(candidate)):
                parents.add(str(candidate))
    return parents


if __name__ == "__main__":
    strings = find_strings_lvl3(BASE / "My Songs/song.flm")
    for s in sorted(set(strings)):
        print(s)
    print("count", len(strings))
