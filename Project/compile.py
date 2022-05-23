import PyInstaller.__main__

# pyinstaller predict.py --noconsole --onefile --windowed

PyInstaller.__main__.run([
    'cubeScan.py',
    "--name=Rubiks cube solver",
    '--noconsole',
    '--onefile',
    '--windowed'
])