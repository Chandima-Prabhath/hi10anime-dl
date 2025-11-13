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
        # Candidate locations to look for an openssl zip (cwd, project dir, parent, repo root)
        candidates = []
        cwd = os.getcwd()
        candidates.append(os.path.join(cwd, 'openssl.zip'))
        candidates.append(os.path.join(project_dir, 'openssl.zip'))
        # parent of project_dir
        parent = os.path.dirname(project_dir)
        candidates.append(os.path.join(parent, 'openssl.zip'))

        # Also include any file matching openssl*.zip in project_dir
        for p in glob.glob(os.path.join(project_dir, 'openssl*.zip')):
            candidates.append(p)

        checked = []
        found_and_copied = False
        for zip_path in candidates:
            if not zip_path:
                continue
            checked.append(zip_path)
            if os.path.exists(zip_path):
                print(f"Found zip at: {zip_path}. Extracting and searching for openssl.exe...")
                tmpdir = tempfile.mkdtemp(prefix='openssl_extract_')
                try:
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as z:
                            z.extractall(tmpdir)
                    except zipfile.BadZipFile:
                        print(f"The file '{zip_path}' is not a valid zip archive. Skipping.")
                        continue

                    # Search extracted files for openssl.exe (recursive)
                    matches = glob.glob(os.path.join(tmpdir, '**', 'openssl.exe'), recursive=True)
                    if matches:
                        found = matches[0]
                        os.makedirs(openssl_dir, exist_ok=True)
                        shutil.copy2(found, openssl_path)
                        print(f"Copied openssl.exe from '{found}' to '{openssl_path}'.")
                        found_and_copied = True
                        break
                    else:
                        print(f"Could not find 'openssl.exe' inside '{zip_path}'.")
                finally:
                    try:
                        shutil.rmtree(tmpdir)
                    except Exception:
                        pass

        if not checked:
            print("No candidate 'openssl.zip' files were found during the search.")
        else:
            print("Checked the following zip paths:")
            for p in checked:
                print(f" - {p}")

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
