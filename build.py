import PyInstaller.__main__
import os
import shutil

def build():
    # Clean previous builds
    for folder in ['dist', 'build']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    if os.path.exists('Hi10-DL.spec'):
        os.remove('Hi10-DL.spec')

    # Path to the UPX folder in your repo
    upx_path = os.path.join(os.getcwd(), 'upx')

    pyinstaller_command = [
        'setup.py',
        '--name=Hi10-DL',
        '--onefile',
        '--noconsole',
        '--icon=app.ico',
        # Restored 'email' because requests/urllib3 require it 
        '--exclude-module', 'tkinter',
        '--exclude-module', 'unittest',
        '--exclude-module', 'pydoc',
        '--exclude-module', 'test',
        # Aggressively exclude large unused PyQt6 components
        '--exclude-module', 'PyQt6.QtWebEngineCore',
        '--exclude-module', 'PyQt6.QtWebEngineWidgets',
        '--exclude-module', 'PyQt6.QtQuick',
        '--exclude-module', 'PyQt6.QtQml',
        '--add-data', f'app.ico{os.pathsep}.',
        '--add-data', f'app.png{os.pathsep}.',
        '--add-data', f'app/icons{os.pathsep}icons',
        '--add-data', f'config.json{os.pathsep}.',
        '--hidden-import', 'PyQt6.QtNetwork',
    ]

    if os.path.exists(upx_path):
        pyinstaller_command.extend(['--upx-dir', upx_path])

    # OpenSSL binary handling
    openssl_path = os.path.join('openssl', 'openssl.exe')
    if os.path.exists(openssl_path):
        pyinstaller_command.extend(['--add-binary', f'{openssl_path}{os.pathsep}.'])

    PyInstaller.__main__.run(pyinstaller_command)

if __name__ == "__main__":
    build()