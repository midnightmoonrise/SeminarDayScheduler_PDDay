import csv

seminars = set()

print(seminars)
initial_index = 3

with open("PD_CSV/testing_data_sample.csv", newline='') as infile:
    reader = csv.reader(infile)
    for row in reader:
        for period in range(3):
            if row[initial_index + period*6 - 1] == "Yes":
                continue
            for pref in range(5):
                sem = (row[initial_index + period*6 + pref], period+1)
                if sem == '':
                    print(row)
                seminars.add(sem)


for seminar in seminars:
    if str(seminar).find("Chris Luczkow") != -1:
        print(seminar)

seminar_names = set()
for name, _ in seminars:
    seminar_names.add(name)


csv_seminars = set()

with open("PD_CSV/seminar_roomassignments.csv", newline='') as infile:
    reader = csv.reader(infile)
    for row in reader:
        csv_seminars.add(row[0])

print(len(seminar_names))
print(len(csv_seminars))

print(seminar_names.difference(csv_seminars))
print(len(csv_seminars.intersection(seminar_names)))

for sem in (csv_seminars):
    if str(sem).find("Luczkow") != -1:
        print(sem)