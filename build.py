import PyInstaller.__main__
import os
import shutil
import glob

def build():
    # Clean previous builds to ensure a fresh, lean executable
    for folder in ['dist', 'build']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    if os.path.exists('Hi10-DL.spec'):
        os.remove('Hi10-DL.spec')

    # Path to the UPX folder already present in your repo
    upx_path = os.path.join(os.getcwd(), 'upx')

    # Base PyInstaller command
    pyinstaller_command = [
        'setup.py',
        '--name=Hi10-DL',
        '--onefile',
        '--noconsole',
        '--icon=app.ico',
        # Exclude heavy modules not typically used in this app to save space
        '--exclude-module', 'tkinter',
        '--exclude-module', 'unittest',
        '--exclude-module', 'pydoc',
        '--exclude-module', 'email',
        '--exclude-module', 'http.server',
        '--exclude-module', 'test',
        # Data files and icons
        '--add-data', f'app.ico{os.pathsep}.',
        '--add-data', f'app.png{os.pathsep}.',
        '--add-data', f'app/icons{os.pathsep}icons',
        '--hidden-import', 'PyQt6.QtNetwork',
    ]

    # Apply UPX compression using your local folder
    if os.path.exists(upx_path):
        print(f"Applying UPX compression from: {upx_path}")
        pyinstaller_command.extend(['--upx-dir', upx_path])
    else:
        print("Warning: Local 'upx' folder not found. Skipping compression.")

    # OpenSSL binary handling
    openssl_path = os.path.join('openssl', 'openssl.exe')
    if os.path.exists(openssl_path):
        pyinstaller_command.extend(['--add-binary', f'{openssl_path}{os.pathsep}.'])

    PyInstaller.__main__.run(pyinstaller_command)

if __name__ == "__main__":
    build()