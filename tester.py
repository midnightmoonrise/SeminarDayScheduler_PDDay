import csv
import random

# seminars = set()

# print(seminars)
# initial_index = 3

# with open("PD_CSV/testing_data_sample.csv", newline='') as infile:
#     reader = csv.reader(infile)
#     for row in reader:
#         for period in range(3):
#             if row[initial_index + period*6 - 1] == "Yes":
#                 continue
#             for pref in range(5):
#                 sem = (row[initial_index + period*6 + pref], period+1)
#                 if sem == '':
#                     print(row)
#                 seminars.add(sem)


# for seminar in seminars:
#     if str(seminar).find("Chris Luczkow") != -1:
#         print(seminar)

# seminar_names = set()
# for name, _ in seminars:
#     seminar_names.add(name)


# csv_seminars = set()

# with open("PD_CSV/seminar_roomassignments.csv", newline='') as infile:
#     reader = csv.reader(infile)
#     for row in reader:
#         csv_seminars.add(row[0])

# print(len(seminar_names))
# print(len(csv_seminars))

# print(seminar_names.difference(csv_seminars))
# print(len(csv_seminars.intersection(seminar_names)))

# for sem in (csv_seminars):
#     if str(sem).find("Luczkow") != -1:
#         print(sem)
# # roomCapacities = {}
# # with open("PD_CSV/roomlist.csv", newline='') as infile:
# #     reader = csv.DictReader(infile)
# #     for row in reader:
# #         roomCapacities[row["room"]] = row["capacity"]

# # print(roomCapacities)

# # the_list = ["Siming Chen", "Avery Burkett", "Amanda Lydon", "Isabelle Wu", "Antonis Alexopoulos", "Ben Juo", "Abe Klein"]

# # for x in range(len(the_list)):
# #     if the_list[x] == "Rebecca Waterman":
# #         the_list[x] = "watermanr1@doversherborn.org"
# #     elif the_list[x] == "Leah Li":
# #         the_list[x] = "liy@doversherborn.org"
# #     else:
# #         first, last = the_list[x].split(" ")
# #         the_list[x] = last.lower() + first[0].lower() + "@doversherborn.org"

# # print(the_list)

# # num_periods = random.randint(1, 10)
# # period_capacities = [0 for i in range(num_periods)]
# # print(num_periods)
# # print(period_capacities)

# # check if preferences is reading right
# # preferences_csv = open("PD_CSV/testing_data_sample.csv")
# # preferences_reader = csv.reader(preferences_csv)

# # for student in preferences_reader:
# #             email = student[1]
# #             # print(student)
# #             print(email)
# #             print("\n")

# # Create something that will set all preferences to "Presenting" for someone who answered "yes"
# preferences = []
# with open("PD_CSV/small_testing_sample.csv", newline='') as infile:
#     reader = csv.reader(infile)
#     for row in reader:
#         preferences.append(row)

# for teacher_data in preferences:
#     if teacher_data[2] == "Yes":
#         for i in range(3,8):
#             teacher_data[i] = "Presenting"
#     if teacher_data[8] == "Yes":
#         for i in range(9,14):
#             teacher_data[i] = "Presenting"
#     if teacher_data[14] == "Yes":
#         for i in range(15,20):
#             teacher_data[i] = "Presenting"

# print(preferences[9])
# # print(preferences)

# Check for duplicate form fills!
temp_emailtoname = {}
with open("PD_CSV/teachernames.csv", newline='') as infile:
    reader = csv.reader(infile)
    for row in reader:
        try:
            print(temp_emailtoname[row[0].rstrip()])
            print(f"{row[0].rstrip()} filled out the form twice")
        except KeyError:
            temp_emailtoname[row[0].rstrip()] = row[1].rstrip()

# check why my missing teachers-presenters are wrong??
presenting_period_1 = ["Tom Duprey", "Mike Sweeney", "Alex Carroll"]
presenting_period_2 = ["Tom Duprey", "Toni Milbourn", "Andrew McCorkle", "Mike Sweeney", "Alex Carroll", "Addie Perez Krebs"]
presenting_period_3 = ["Toni Milbourn", "Andrew McCorkle", "Phil Rodino", "Addie Perez Krebs"]
print(temp_emailtoname["dupreyt@doversherborn.org"])
print(temp_emailtoname["dupreyt@doversherborn.org"] in presenting_period_1)

# Populate class list

# classes_csv = open("PD_CSV/seminar_roomassignments.csv")
# classes_reader = csv.reader(classes_csv)
# classes = []
# # fills in classes list. 
# for aclass in classes_reader:
#     print(aclass)
#     classes += [aclass[0]]

# What's wrong with mrs. Memmott's seminar? 

# for teacher in preferences: 
#     if teacher[1] != "levasseurc@doversherborn.org": 
#         continue
#     else: 
#         for x in teacher[2:]:
#             print(x)
#             print(x in classes)
#             print(f"It is {teacher[7].strip() == classes[6].strip()}")
#             print(teacher[7])
#             print(classes[6])

# classes[6] is wendy rush and mary memmott
