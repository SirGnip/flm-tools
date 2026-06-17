from pathlib import Path
from gnp.flm.lib import files


def find_strs(fname: str):
    # strings = files.find_strings(Path(fname).resolve())
    # strings = files.find_strings_lvl2(Path(fname).resolve())
    strings = files.find_strings_lvl3(Path(fname).resolve())
    for s in strings:
        print(s)


if __name__ == '__main__':
    find_strs(r'c:\path\mysong.flm')
