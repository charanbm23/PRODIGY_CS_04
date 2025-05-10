import PyInstaller.__main__
import os

def build_executable():
    """Build the keylogger executable"""
    PyInstaller.__main__.run([
        'gui.py',
        '--onefile',
        '--windowed',
        '--name=SimpleKeylogger',
        '--add-data=README.md;.',
        '--icon=NONE',
        '--clean',
        '--noconfirm'
    ])

if __name__ == "__main__":
    build_executable() 