@echo off
chcp 65001 > nul

:: Clean previous builds
if exist setup.spec del setup.spec
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

:: Set virtual environment command prefix
set VENV_CMD=.venv\Scripts\
if not exist .venv set VENV_CMD=

:: Build optimized executable
%VENV_CMD%pyi-makespec ^
  --onefile ^
  --icon=app.ico ^
  --name=Hi10-DL ^
  --strip ^
  --noconsole ^
  --optimize 2 ^
  --hidden-import=win32gui,win32process,win32con ^
  --hidden-import=PyQt6.QtWidgets,PyQt6.QtCore ^
  --hidden-import=darkdetect ^
  --hidden-import=requests,bs4 ^
  --exclude-module=PyQt6.QtWebEngineWidgets ^
  --exclude-module=PyQt6.QtNetwork ^
  --exclude-module=PyQt6.QtMultimedia ^
  --exclude-module=PyQt6.QtBluetooth ^
  --exclude-module=PyQt6.QtPositioning ^
  --exclude-module=PyQt6.QtDesigner ^
  --exclude-module=PyQt6.QtHelp ^
  --exclude-module=PyQt6.QtLocation ^
  --exclude-module=PyQt6.QtOpenGL ^
  --exclude-module=PyQt6.QtPrintSupport ^
  --exclude-module=PyQt6.QtQml ^
  --exclude-module=PyQt6.QtQuick ^
  --exclude-module=PyQt6.QtSql ^
  --exclude-module=PyQt6.QtTest ^
  --exclude-module=PyQt6.QtXml ^
  --exclude-module=PyQt6.QtPdf ^
  --exclude-module=PyQt6.QtWebEngineCore ^
  --exclude-module=PyQt6.QtWebEngineWidgets ^
  setup.py && ^
ren "Hi10-DL.spec" setup.spec && ^
%VENV_CMD%pyinstaller --noconfirm --upx-dir=./upx --clean setup.spec