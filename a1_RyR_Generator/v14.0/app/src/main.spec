# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [
        '../src/main.py',
        '../src/core_logic.py',
        '../src/custom_entry_widget.py',
        '../src/tools/database.py',
        '../src/tools/_db_tools.py',
        '../src/logic/file_number_checker.py',
        '../src/logic/intelligent_cameras.py',
        '../src/logic/light_guides.py'
    ],
    pathex=['../src'],
    binaries=[],
    datas=[
        ('../resources/help.json', 'datas'),
        ('../assets/background.png', 'datas/assets'),
        ('../assets/icon.ico', 'datas/assets'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
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
    icon='../src/assets/icon.ico'
)
