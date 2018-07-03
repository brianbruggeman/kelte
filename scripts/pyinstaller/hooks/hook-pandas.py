from PyInstaller.utils.hooks import collect_dynamic_libs

hiddenimports = [
    "pandas._libs.tslibs.np_datetime",
    "pandas._libs.tslibs.nattype",
    "pandas._libs.skiplist",
]

# Install shared libraries to the working directory.
binaries = collect_dynamic_libs("pandas", destdir=".")
