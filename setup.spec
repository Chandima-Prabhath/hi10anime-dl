# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['setup.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['win32gui,win32process,win32con', 'PyQt6.QtWidgets,PyQt6.QtCore', 'darkdetect', 'requests,bs4'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt6.QtWebEngineWidgets', 'PyQt6.QtNetwork', 'PyQt6.QtMultimedia', 'PyQt6.QtBluetooth', 'PyQt6.QtPositioning', 'PyQt6.QtDesigner', 'PyQt6.QtHelp', 'PyQt6.QtLocation', 'PyQt6.QtOpenGL', 'PyQt6.QtPrintSupport', 'PyQt6.QtQml', 'PyQt6.QtQuick', 'PyQt6.QtSql', 'PyQt6.QtTest', 'PyQt6.QtXml', 'PyQt6.QtPdf', 'PyQt6.QtWebEngineCore', 'PyQt6.QtWebEngineWidgets'],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='Hi10-DL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app.ico'],
)
