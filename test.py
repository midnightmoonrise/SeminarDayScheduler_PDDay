import tkinter as tk
from tkinter import filedialog
import csv

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

file = open(file_path)

reader = csv.reader(file)

print([x for x in range(10)])

for line in reader:
    print(line[0] + ": " + str(line[1:]))

file.close()