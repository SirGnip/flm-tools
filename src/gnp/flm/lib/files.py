from pathlib import Path
BASE = Path(r'c:\folder')

def find_strings(filepath: str | Path, min_length: int = 4) -> list[str]:
    """
    Find all ASCII strings in a binary file, similar to the Unix `strings` command.

    Args:
    filepath: Path to the binary file.
    min_length: Minimum string length to include (default: 4).

    Returns:
    List of ASCII strings found in the file.
    """
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


if __name__ == '__main__':
    strings = find_strings(BASE / "My Songs/MyMobileSongs/Be Still My Soul final.flm")

    strings = [s for s in strings if '/' in s]
    strings = [s for s in strings if not s.startswith('Resources')]  # strip ^Resources as these paths are duplicated elsewhere
    strings = [s for s in strings if not s.startswith('/storage/emulated')]

    for s in sorted(set(strings)):
        print(s)
    print('count', len(strings))
