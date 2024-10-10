import tkinter as tk
from tkinter import filedialog
import csv

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

file = open(file_path)

reader = csv.reader(file)

d = {}

for line in reader:
    d[line[0]] = line[1]

for line in reader:
    print(line)

print(d)

file.close()


# sakib,sksib,skibidi seminar,business seminar,cube seminar,orange seminar,cheese seminar
# skaib,skisb,orange seminar,cube seminar,business seminar,skibidi seminar,cheese seminar
# sksib,skbib,skibidi seminar,cube seminar,cheese seminar,orange seminar,business seminar
# skbib,skdib,cube seminar,orange seminar,business seminar,skibidi seminar,cheese seminar
# skeib,skaib,skibidi seminar,cube seminar,business seminar,orange seminar,cheese seminar
# sakib,sksib,skibidi seminar,business seminar,cube seminar,orange seminar,cheese seminar
# skaib,skisb,orange seminar,cube seminar,business seminar,skibidi seminar,cheese seminar
# sksib,skbib,skibidi seminar,cube seminar,cheese seminar,orange seminar,business seminar
# skbib,skdib,cube seminar,orange seminar,business seminar,skibidi seminar,cheese seminar