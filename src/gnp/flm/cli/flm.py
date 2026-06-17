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


def _cmd_parent(args):
    for s in sorted(files.find_parents(args.file)):
        print(s)


def _cmd_orphan(args):
    for s in sorted(files.find_orphans(args.directory)):
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

    parent_parser = subparsers.add_parser(
        "parent",
        help="List the files that reference the given file",
    )
    parent_parser.add_argument("file", help="Path to the file (relative, absolute, or bare filename)")
    parent_parser.set_defaults(func=_cmd_parent)

    orphan_parser = subparsers.add_parser(
        "orphan",
        help="List the files in a directory that no other file references",
    )
    orphan_parser.add_argument("directory", help="Path to the directory (relative, absolute, or bare path)")
    orphan_parser.set_defaults(func=_cmd_orphan)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
