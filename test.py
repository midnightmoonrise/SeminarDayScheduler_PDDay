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


# sakib,sksib,skibidi seminar,business seminar,cube seminar,orange seminar,cheese seminar
# skaib,skisb,orange seminar,cube seminar,business seminar,skibidi seminar,cheese seminar
# sksib,skbib,skibidi seminar,cube seminar,cheese seminar,orange seminar,business seminar
# skbib,skdib,cube seminar,orange seminar,business seminar,skibidi seminar,cheese seminar
# skeib,skaib,skibidi seminar,cube seminar,business seminar,orange seminar,cheese seminar
# sakib,sksib,skibidi seminar,business seminar,cube seminar,orange seminar,cheese seminar
# skaib,skisb,orange seminar,cube seminar,business seminar,skibidi seminar,cheese seminar
# sksib,skbib,skibidi seminar,cube seminar,cheese seminar,orange seminar,business seminar
# skbib,skdib,cube seminar,orange seminar,business seminar,skibidi seminar,cheese seminar