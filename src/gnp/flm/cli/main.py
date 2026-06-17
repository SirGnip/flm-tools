import argparse

from gnp.flm.cli import dumpstr


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flm",
        description="Tools for working with FL Studio Mobile (.flm) files",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    dumpstr_parser = subparsers.add_parser(
        "dumpstr",
        help="Dump interesting strings (file paths) found in an .flm file",
    )
    dumpstr_parser.add_argument("file", help="Path to the .flm file")
    dumpstr_parser.set_defaults(func=lambda args: dumpstr.find_strs(args.file))

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
