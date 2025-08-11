# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['hidzor.py'],
    pathex=[],
    binaries=[],
    datas=[('icons', 'icons'), ('config.yaml', '.')],
    hiddenimports=['imageio.plugins.ffmpeg', 'imageio.plugins.pillow', 'imageio.plugins.gif'],
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
    a.zipfiles,
    a.datas,
    [],
    name='Hidzor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/icons.gif',
)
app = BUNDLE(
    exe,
    name='Hidzor.app',
    icon='icons/icons.gif',
    bundle_identifier=None,
)
