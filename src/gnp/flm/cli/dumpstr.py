import sys
from gnp.flm.lib.files import find_strings_clean


def main():
    fname = sys.argv[1]
    strings = find_strings_clean(fname)
    for s in strings:
        print(s)


if __name__ == '__main__':
    main()
