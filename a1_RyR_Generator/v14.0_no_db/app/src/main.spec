# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py', 'core_logic.py', 'custom_entry_widget.py', 'database.py', 'file_number_checker.py', 'intelligent_cameras.py', 'light_guides.py', '_db_tools.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../resources/help.json', 'src'),               # Include help.json from the src directory
        ('../assets/background.png', 'assets'),   # Include background.png from the assets directory
        ('../assets/icon.ico', 'assets'),         # Include icon.ico from the assets directory
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
    icon='icon.ico'  #Specify the path to the ICO file
)
