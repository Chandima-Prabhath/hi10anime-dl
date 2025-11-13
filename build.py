import PyInstaller.__main__
import os
import shutil

def build():
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('Hi10-DL.spec'):
        os.remove('Hi10-DL.spec')

    # Base PyInstaller command
    pyinstaller_command = [
        'setup.py',
        '--name=Hi10-DL',
        '--onefile',
        '--noconsole',
        '--icon=app.ico',
        '--hidden-import', 'PyQt6.QtNetwork'
    ]

    # Check for openssl.exe and add it to the build if it exists
    openssl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openssl', 'openssl.exe')
    if os.path.exists(openssl_path):
        print("Found openssl.exe, adding it to the build.")
        pyinstaller_command.extend([
            '--add-binary',
            f'{openssl_path}{os.pathsep}.'
        ])
    else:
        print("Warning: openssl.exe not found in the 'openssl' directory. The build will continue without it, but you may encounter SSL errors.")
        print("Please download a portable version of OpenSSL and place 'openssl.exe' in the 'openssl' directory.")


    PyInstaller.__main__.run(pyinstaller_command)

if __name__ == "__main__":
    build()
