# Assuming your spec file is in the same directory as your project root

a = Analysis(
    ['src/__main.py', 'src/_core.py', 'src/_filenumber_checker.py'],
    pathex=[r'C:\Users\lucio\Desktop\Code\Python_Eiit_RyR\a1_RyR_Generator\v9.0\app'],
    binaries=[],
    datas=[
        ('src/help.json', 'src'),               # Include help.json from the src directory
        ('assets/background.png', 'assets'),   # Include background.png from the assets directory
        ('assets/icon.ico', 'assets'),         # Include icon.ico from the assets directory
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RyR_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # If you want a console application, otherwise set it to False for a GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

