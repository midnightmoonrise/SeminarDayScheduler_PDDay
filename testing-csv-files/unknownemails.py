import csv
import tkinter as tk
from tkinter import filedialog
from copy import deepcopy

def getFile():
    root = tk.Tk()
    #Hides tkinter window
    root.withdraw()

    #Bring file dialog to front
    root.wm_attributes('-topmost', 1)
    file_path = filedialog.askopenfilename(title='Select a CSV file', filetypes = (("Comma Separated Values","*.csv"),))

    print(file_path)

    #Delete the invisible tk window
    root.quit()
    root.destroy()

    return file_path

def findClosest(target: str, array: list, index: int):

    hits = []
    for item in array:
        if item == target:
            return [item]
        elif item[index] == target[index]:
            hits.append(item)

    if len(hits) <= 1:
        return array
    else:
        return findClosest(target, hits, index + 1)

print("Choose all students file")
students = open(getFile())
students_reader = csv.reader(students)

print("Choose preferences file")
preferences = open(getFile())
preferences_reader = csv.reader(preferences)

emails = []
for student in students_reader:

    if len(student) != 3:
        raise Exception(f"Student Names and Grades file is not formatter properly. First item: {student[0]}")
    if student[0].find("@doversherborn.org") == -1:
        raise Exception(f"Invalid Email. First item: {student[0]}")
    try:
        _ = int(student[1])
    except ValueError:
        raise Exception(f"Student grade(s) is not an integer. First item: {student[0]}")

    emails.append(student[0])

found = []
duplicate_emails = set()
unknown_emails = {}
home_emails = []

for student in preferences_reader:

    email = student[1]

    if email in emails:
        found.append(email)
    else:
        if email in found:
            duplicate_emails.add(email)
        else:
            if email.find("@doversherborn.org") != -1:
                unknown_emails[email] = findClosest(email, emails, 0)
            else:
                home_emails.append(email)

erase = False
if erase:

    rows = []
    preferences.seek(0)

    for student in preferences_reader:
        if not student[1] in home_emails:
            rows.append(student)

    preferences.close()
    preferences = open("CleanedStudentResponses.csv", "xt", newline='')
    csv.writer(preferences).writerows(rows)

students.close()
preferences.close()