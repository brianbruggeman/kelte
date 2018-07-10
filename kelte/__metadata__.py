import subprocess

import pkg_resources

__all__ = (
    "__name__",
    "__description__",
    "__version__",
    "__author__",
    "__author_email__",
    "__maintainer__",
    "__maintainer_email__",
    "__copyright_years__",
    "__license__",
    "__url__",
    "__version_info__",
    "__classifiers__",
    "__keywords__",
    "package_metadata",
)

# ----------------------------------------------------------------------
# Package Metadata (Update manually)
# ----------------------------------------------------------------------
__name__ = "kelte"
__description__ = "7wrl(2018): /r/RoguelikeDev does Roguelike in 2018"
__ver__ = "1.4.0"  # Must follow pep440

__author__ = "Brian Bruggeman"
__author_email__ = "brian.m.bruggeman@gmail.com"

__maintainer__ = "Brian Bruggeman"
__maintainer_email__ = "brian.m.bruggeman@gmail.com"

__copyright_years__ = "2018"
__license__ = "MIT"
__url__ = "https://www.pypi.org"

__keywords__ = ["kelte", "roguelike", "roguelikedev", "roguelite"]


# See: https://pypi.python.org/pypi?%3Aaction=list_classifiers
__classifiers__ = [
    "Programming Language :: Python",
    "Natural Language :: English",
    "Development Status :: 3 - Alpha",
    "Natural Language :: English",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.6",
]


# ----------------------------------------------------------------------
# Programmatic values (Do not update)
# ----------------------------------------------------------------------
def _run(cmd):
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout = proc.stdout.decode("utf-8").strip("\n") if proc.returncode == 0 else None
    return stdout


# Programmatic values
_sha = _run("git rev-parse --short HEAD")
if _sha:
    _sep = "-b"
    __ver__ = f"{__ver__}{_sep}{_sha}"

__version__ = pkg_resources.parse_version(__ver__).public
__version_info__ = tuple(
    int(ver_i)
    for ver_i in pkg_resources.parse_version(__version__).base_version.split(".")
    if ver_i.isdigit()
)


# Package metadata is used in setup
package_metadata = {
    k.strip("_"): v
    for k, v in locals().items()
    if k.startswith("__")
    # Clean items that don't mix with setup
    if k.strip("_") not in ["all", "copyright_years", "ver", "version_info"]
}
