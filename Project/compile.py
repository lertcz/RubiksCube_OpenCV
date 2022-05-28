import PyInstaller.__main__
import rubik_solver

def run():
    # pyinstaller predict.py --noconsole --onefile --windowed

    PyInstaller.__main__.run([
        #'--debug=all',
        '--add-data=rubik_solver;rubik_solver',
        '--add-data=icon.ico;.',
        'cubeScan.py',
        '--name=Rubiks cube solver',
        '--icon=icon.ico',
        '--windowed',
        '--onefile',
        #'--onedir',
        '--noconsole'
    ])

run()
