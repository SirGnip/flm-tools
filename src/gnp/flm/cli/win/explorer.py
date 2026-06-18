from collections import defaultdict
from pathlib import Path


class TooManyWindows(Exception):
    """Raised when opening the requested paths would exceed the window limit."""


def open_in_explorer(paths: list[str | Path], max_windows: int = 15) -> None:
    """Open the given file and directory paths selected in Windows Explorer.

    Paths are grouped by their parent directory; one Explorer window is opened
    per distinct parent, with that parent's items selected. If the number of
    windows that would be opened exceeds max_windows, TooManyWindows is raised
    and no windows are opened.
    """
    from win32com.shell import shell  # imported lazily so the module loads off-Windows

    # Group paths by parent directory so each window selects its items at once.
    groups: dict[Path, list[Path]] = defaultdict(list)
    for path in paths:
        resolved = Path(path).resolve()
        groups[resolved.parent].append(resolved)

    if len(groups) > max_windows:
        raise TooManyWindows(
            f"Opening these paths would require {len(groups)} windows, "
            f"which exceeds the limit of {max_windows}"
        )

    desktop = shell.SHGetDesktopFolder()
    for folder, items in groups.items():
        try:
            folder_pidl = shell.SHParseDisplayName(str(folder), 0, None)[0]
            parent_folder = desktop.BindToObject(folder_pidl, None, shell.IID_IShellFolder)
            child_pidls = [
                parent_folder.ParseDisplayName(0, None, item.name, 0)[1]
                for item in items
            ]
            shell.SHOpenFolderAndSelectItems(folder_pidl, child_pidls, 0)
        except Exception as exc:
            print(f"failed opening folder {folder}. Continuing.")
