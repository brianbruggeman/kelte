#!/usr/bin/env python
import subprocess

from .. import __metadata__ as package_info
from .. import api
from ..config import settings
from ..vendored import click


@click.command()
@click.option("-d/-b", "--dev/--binary", "dev", default=True, is_flag=True, help="Run development mode")
@click.option("-D", "--debug", is_flag=True, help="Run in debug mode.")
@click.option("-v", "--verbose", count=True, help="Increase verbosity.")
@click.option("-V", "--version", is_flag=True, help="Show version and exit.")
@click.option('-s', '--seed', metavar='SEED', help='Set random seed value.')
@click.option('--font-size', metavar='SIZE', help='Set font size', type=int)
def run(dev, debug, verbose, version, seed, font_size):
    if version:
        print(f"{package_info.__version__}")
        exit(0)
    settings.typeface_size = font_size if font_size else settings.typeface_size

    if dev:
        api.main(debug=debug, verbose=verbose, seed=seed)
    else:
        bin_path = settings.repo_path / "dist" / settings.name
        if bin_path.exists():
            bin_path += (
                (' -V' if version else '')
                + (' -d' if debug else '')
                + (f' -{"v" * verbose}' if verbose else '')
                + (f' -s {seed}' if seed else '')
                )
            subprocess.run(str(bin_path), shell=True)
        else:
            print(f"Error: Could not find {bin_path}\n")
            print(f"Try running in developer mode:\n")
            print(f"    run --dev\n")
            exit(1)


if __name__ == "__main__":
    run()
