from PyInstaller.utils.hooks import collect_dynamic_libs

hiddenimports = ["scipy._lib.messagestream"]

# Install shared libraries to the working directory.
binaries = collect_dynamic_libs("scipy", destdir=".")
