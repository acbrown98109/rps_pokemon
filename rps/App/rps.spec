# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['rps.py'],
    pathex=[],
    binaries=[],
    datas=[('rock.png', '.'), ('paper.png', '.'), ('scissors.png', '.'), ('C:\\Users\\HNIC\\AppData\\Roaming\\Python\\Python313\\site-packages\\Pillow', 'Pillow')],
    hiddenimports=['PIL', 'collections.abc', 'encodings'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='rps',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
