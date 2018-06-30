#!/usr/bin/env python
import subprocess

from .. import __metadata__ as package_info
from .. import api
from ..vendored import click
from ..config import settings


@click.command()
@click.option('-d/-b', '--dev/--binary', 'dev', default=True, is_flag=True, help='Run development mode')
@click.option('-D', '--debug', is_flag=True, help='Run in debug mode.')
@click.option('-v', '--verbose', count=True, help='Increase verbosity.')
@click.option('-V', '--version', is_flag=True, help='Show version and exit.')
def run(dev, debug, verbose, version):
    if version:
        print(f'{package_info.__version__}')
        exit(0)

    if dev:
        api.run(debug=debug, verbose=verbose)
    else:
        bin_path = settings.repo_path / 'dist' / settings.name
        if bin_path.exists():
            subprocess.run(str(bin_path), shell=True, )
        else:
            print(f'Error: Could not find {bin_path}\n')
            print(f'Try running in developer mode:\n')
            print(f'    run --dev\n')
            exit(1)


if __name__ == '__main__':
    run()
