#!/usr/bin/env python
import subprocess
import sys

from ..config import settings
from ..vendored import click


# Notes:
#   Pyinstaller seems to build a bad binary on Windows when:
#     - using upx
#     - using windowed mode

@click.command()
@click.option(
    "-u",
    "--upx",
    is_flag=True,
    default=True if sys.platform != "win32" else False,
    help="Create a debug build",
)
@click.option("-C/-w", "--console/--window", 'console', is_flag=True, default=False, help="Toggle window/console build")
@click.option("-d", "--debug", is_flag=True, help="Create a debug build")
@click.option("-c", "--clean", is_flag=True, help="Use pyinstaller clean")
@click.option("-v", "--verbose", count=True, help="Increase output")
def build(console, clean, verbose, debug, upx):
    package_name = settings.name
    sys_id_mapping = {"darwin": "mac", "win32": "win"}
    options = (
        "-F -y"
        + (" -w" if not console else " -c")
        + (" -d" if debug else "")
        + (" --clean" if clean else "")
        + (" --noupx" if not upx else "")
    )
    levels = ["ERROR", "WARNING", "INFO", "DEBUG"]
    log_level = levels[min(verbose, len(levels) - 1)]
    sys_id = sys_id_mapping.get(sys.platform, "linux")
    script_path = settings.repo_path / "run.py"
    # script_path = settings.repo_path / 'kelte' / 'cli' / 'run.py'
    hooks_path = settings.repo_path / "scripts" / "pyinstaller" / "hooks"
    build_path = settings.repo_path / "build" / sys_id
    sep = ";" if sys_id == "win" else ":"
    command = " ".join(
        [
            f"pyinstaller {options}",
            f"--name {package_name}",
            f"--workpath {build_path}",
            f"--log-level {log_level}",
            f"--additional-hooks-dir {hooks_path}",
            f"--add-data assets{sep}assets",
            str(script_path),
        ]
    )
    print(command)
    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    build()
