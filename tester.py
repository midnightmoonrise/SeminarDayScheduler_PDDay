import csv

roomCapacities = {}
with open("testing-csv-files/roomlist.csv", newline='') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        roomCapacities[row["room"]] = row["capacity"]

print(roomCapacities)
