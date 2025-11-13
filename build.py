import PyInstaller.__main__
import os
import shutil
import zipfile
import glob
import tempfile

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

    # Prepare path for openssl.exe in project `openssl` directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    openssl_dir = os.path.join(project_dir, 'openssl')
    openssl_path = os.path.join(openssl_dir, 'openssl.exe')

    # If openssl.exe isn't present, try to extract it from openssl.zip if available
    if not os.path.exists(openssl_path):
        zip_path = os.path.join(project_dir, 'openssl.zip')
        if os.path.exists(zip_path):
            print(f"Found '{os.path.basename(zip_path)}'. Extracting and searching for openssl.exe...")
            tmpdir = tempfile.mkdtemp(prefix='openssl_extract_')
            try:
                with zipfile.ZipFile(zip_path, 'r') as z:
                    z.extractall(tmpdir)

                # Search extracted files for openssl.exe (recursive)
                matches = glob.glob(os.path.join(tmpdir, '**', 'openssl.exe'), recursive=True)
                if matches:
                    found = matches[0]
                    os.makedirs(openssl_dir, exist_ok=True)
                    shutil.copy2(found, openssl_path)
                    print(f"Copied openssl.exe to '{openssl_path}'.")
                else:
                    print("Could not find 'openssl.exe' inside the zip archive.")
            except zipfile.BadZipFile:
                print("The file 'openssl.zip' is not a valid zip archive.")
            finally:
                try:
                    shutil.rmtree(tmpdir)
                except Exception:
                    pass

    # Check again for openssl.exe and add it to the build if it exists
    if os.path.exists(openssl_path):
        print("Found openssl.exe, adding it to the build.")
        pyinstaller_command.extend([
            '--add-binary',
            f'{openssl_path}{os.pathsep}.'
        ])
    else:
        print("Warning: openssl.exe not found in the 'openssl' directory. The build will continue without it, but you may encounter SSL errors.")
        print("Please download a portable version of OpenSSL and place 'openssl.exe' in the 'openssl' directory, or provide 'openssl.zip' containing it.")


    PyInstaller.__main__.run(pyinstaller_command)

if __name__ == "__main__":
    build()
