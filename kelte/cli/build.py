#!/usr/bin/env python
import shutil
import subprocess

from ..config import settings
from ..vendored import click


@click.command()
def build():
    package_name = settings.name
    spec_filepath = settings.repo_path / f'{package_name}.spec'
    clean_build()
    command = f'pyinstaller {spec_filepath}'
    subprocess.run(command, shell=True, check=True)


def clean_build():
    dist_path = settings.repo_path / 'dist'
    build_path = settings.repo_path / 'build'

    for path in [dist_path, build_path]:
        if path.exists():
            shutil.rmtree(path)


if __name__ == '__main__':
    build()
