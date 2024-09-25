import tkinter as tk
from tkinter import filedialog
import main
from main import *

def select_file():
    file_path = filedialog.askopenfilename(title="Select a file")
    file_path_label.config(text=file_path)


root = tk.Tk()
root.title ('Kontur Grapher')

root.geometry("450x450")

headers = tk.Label(root, text = 'Kontur to Tkinter')
headers.pack(pady = 35)


file_path_label = tk.Label(root,text = '')
file_path_label.pack(pady=10)

file_button = tk.Button(root, text = 'Select csv file', command = select_file)
file_button.pack()

button = tk.Button(root, text = 'Clean CSV file', command = lambda : header_cleaner_csv(file_path_label.cget("text")))
button.pack()

root.mainloop()

