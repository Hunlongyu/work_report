# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['src\\main.py'],
    pathex=['E:\\Hunlongyu\\work_report'],
    binaries=[
        ('src/components', 'src/components'),
        ('src/config', 'src/config'),
        ('src/resources/app.ico', 'src/resources/app.ico'),
        ('src/utils', 'src/utils'),
        ('src/views', 'src/views'),
        *collect_data_files('qtmodern6'),
        *collect_data_files('qt_themes'),
    ],
    datas=[],
    hiddenimports=[],
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
    name='AI 工作总结',
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
    icon=['src/resources/app.ico'],
)
