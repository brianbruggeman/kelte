# -*- mode: python -*-
from pathlib import Path

block_cipher = None


a = Analysis(
    [
        'kelte/__main__.py'
    ],
    pathex=['.'],
    binaries=[
    ],
    datas=[
        ('assets', 'assets')
    ],
    hiddenimports=[
        'packaging.version',
        '_cffi_backend'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='kelte',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False
)

app = BUNDLE(
    exe,
    name='kelte.app',
    icon=None,
    bundle_identifier=None
)
