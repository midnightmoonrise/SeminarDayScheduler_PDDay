import csv
import random

# roomCapacities = {}
# with open("PD_CSV/roomlist.csv", newline='') as infile:
#     reader = csv.DictReader(infile)
#     for row in reader:
#         roomCapacities[row["room"]] = row["capacity"]

# print(roomCapacities)

# the_list = ["Siming Chen", "Avery Burkett", "Amanda Lydon", "Isabelle Wu", "Antonis Alexopoulos", "Ben Juo", "Abe Klein"]

# for x in range(len(the_list)):
#     if the_list[x] == "Rebecca Waterman":
#         the_list[x] = "watermanr1@doversherborn.org"
#     elif the_list[x] == "Leah Li":
#         the_list[x] = "liy@doversherborn.org"
#     else:
#         first, last = the_list[x].split(" ")
#         the_list[x] = last.lower() + first[0].lower() + "@doversherborn.org"

# print(the_list)

# num_periods = random.randint(1, 10)
# period_capacities = [0 for i in range(num_periods)]
# print(num_periods)
# print(period_capacities)

# check if preferences is reading right
# preferences_csv = open("PD_CSV/testing_data_sample.csv")
# preferences_reader = csv.reader(preferences_csv)

# for student in preferences_reader:
#             email = student[1]
#             # print(student)
#             print(email)
#             print("\n")

# Create something that will set all preferences to "Presenting" for someone who answered "yes"
preferences = []
with open("PD_CSV/small_testing_sample.csv", newline='') as infile:
    reader = csv.reader(infile)
    for row in reader:
        preferences.append(row)

for teacher_data in preferences:
    if teacher_data[2] == "Yes":
        for i in range(3,8):
            teacher_data[i] = "Presenting"
    if teacher_data[8] == "Yes":
        for i in range(9,14):
            teacher_data[i] = "Presenting"
    if teacher_data[14] == "Yes":
        for i in range(15,20):
            teacher_data[i] = "Presenting"

print(preferences[9])
# print(preferences)
