import argparse

from gnp.flm.lib import files


def _cmd_strings(args):
    funcs = {
        1: files.find_strings_lvl3,
        2: files.find_strings_lvl2,
        3: files.find_strings,
    }
    for s in funcs[args.verbose](args.file):
        print(s)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flm",
        description="Tools for working with FL Studio Mobile (.flm) files",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    strings_parser = subparsers.add_parser(
        "strings",
        help="Dump strings found in an .flm file",
    )
    strings_parser.add_argument("file", help="Path to the .flm file (relative, absolute, or bare filename)")
    strings_parser.add_argument(
        "-v", "--verbose",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="Filtering level: 1=raw strings, 2=interesting paths, 3=cleaned (default: 1)",
    )
    strings_parser.set_defaults(func=_cmd_strings)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
