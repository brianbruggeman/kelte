#!/usr/bin/env python
import shutil
import subprocess
import sys

from ..config import settings
from ..vendored import click


@click.command()
def build():
    package_name = settings.name
    sys_id_mapping = {
        'darwin': 'mac',
        'win32': 'win',
        }
    sys_id = sys_id_mapping.get(sys.platform, 'linux')
    spec_filepath = settings.repo_path / f'{package_name}-{sys_id}.spec'
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
