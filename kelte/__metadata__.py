import subprocess
from dataclasses import dataclass, field
from typing import Dict, Tuple, Union


__all__ = ('package_metadata', )

# ----------------------------------------------------------------------
# Package Metadata (Update manually)
# ----------------------------------------------------------------------

@dataclass
class PackageMetadata:
    name: str = 'kelte'
    description: str = '7wrl(2018): /r/RoguelikeDev does Roguelike in 2018'

    version: str = '1.4.0'
    ver: str = field(init=False)
    major: int = field(init=False)
    minor: int = field(init=False)
    micro: int = field(init=False)
    build: str = field(init=False)
    version_info: Dict[str, Union[str, int]] = field(init=False)

    author: str = 'Brian Bruggeman'
    author_email: str = 'brian.m.bruggeman@gmail.com'

    maintainer: str = 'Brian Bruggeman'
    maintainer_email: str = 'brian.m.bruggeman@gmail.com'

    copyright_years: Tuple = (2017, 2018)
    copyright: str = field(init=False)

    license: str = 'MIT'
    url: str = 'https://github.com/brianbruggeman/kelte.git'

    keywords: Tuple = (name, 'roguelike', 'roguelite', 'roguelikedev')

    classifiers: Tuple = (
        'Programming Language :: Python',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
    )

    def __post_init__(self):
        # update copyright
        self.copyright = ', '.join(map(str, self.copyright_years))
        # update version
        self.ver = self.version
        self.major, self.minor, self.micro = self.ver.split('.')
        self.build = self._git_rev()
        self.version = f'{self.ver}.{self.build}' if self.build else self.version

    @staticmethod
    def _git_rev():
        proc = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE)
        output = proc.stdout.decode('utf-8').strip()
        return output

    @property
    def setup(self):
        valid_setup_keys = (
            'name', 'description', 'version', 'author', 'author_email',
            'maintainer', 'maintainer_email', 'copyright', 'license',
            'url', 'keywords', 'classifiers'
            )
        data = {
            k: getattr(self, k)
            for k in self.__annotations__.keys()
            if k in valid_setup_keys
            }
        return data


# Package metadata is used in setup
package_metadata = PackageMetadata()
