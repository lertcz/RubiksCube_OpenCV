import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
#hide the root
root.withdraw()

# the input dialog
USER_INP = simpledialog.askstring(title="IP",
                                  prompt="What's your cam IP?")


# check it out
print("Hello", USER_INP)