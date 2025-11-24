"""Linear assignment example."""
from ortools.graph.python import min_cost_flow
import csv 
import random
import os
from copy import deepcopy

# anyone you want to give special priority to
the_list = []

# email maker for teachers if we wanna do the whole the_list thing
for x in range(len(the_list)):
    if the_list[x] == "Rebecca Waterman":
        the_list[x] = "watermanr1@doversherborn.org"
    elif the_list[x] == "Leah Li":
        the_list[x] = "liy@doversherborn.org"
    else:
        first, last = the_list[x].split(" ")
        the_list[x] = last.lower() + first[0].lower() + "@doversherborn.org"

# student_led_seminar_students = [
#     "Jacob Spilman", "Nathan Zeng", "Vivian Kamphaus", "Alexander Mroz", "Patrick Driscoll", "Simon Hart", "Joshua Dias", "Gabriella Schroeder", "Dagny Abbett", "Nora Olson", "james davies", "tessa correll",
#     "Armaan Tamber", "Cillian Moss", "Felix Giesen" 
# ]

# for x in range(len(student_led_seminar_students)):
#     first, last = student_led_seminar_students[x].split(" ")
#     student_led_seminar_students[x] = last.lower() + "." + first.lower() + "@doversherborn.org"

# TODO: output to pdf
# TODO: some output thing
# TODO: STUDENT LED SEMINAR
# TODO: Get rid of grade distinctions
# TODO: Missing students change to most popular seminars (if time, lowest priority)

# duplicate preferences can be done during preproccesing >>> done
# duplicate students has also been handled (incase that happens somehow)

# students not responding can be dealt with in pre or post processing
# pre-processing would be adding missing students with random preferences  >>> done, missing students also have the least weight
# post-processing would be adding missing students into any avaliable seminars



output_directory = "Output"

csv_file_paths = {}

forms_reader = 0
forms_csv = 0

preferences_reader = 0
preferences_csv = 0

studenttograde = {}
emailtoname = {}
# use a CSV File to read room capacities (may not be needed)
roomCapacities = {}
with open("PD_CSV/roomlist.csv", newline='') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        print(row)
        roomCapacities[row["room"]] = row["capacity"]

print(roomCapacities)

total_emails = []
emails = []
schedules = []

classes_reader = 0
num_periods = 3
num_preferences_per_period = 6

seminars_by_period = [[] for _ in range(num_periods)]

classes = []
class_capacities = [[] for _ in range(num_periods)]
master_list = []


#Called by the web interface
def init(uploaded_csv_file_paths, uploaded_output_dir):
    global csv_file_paths, output_directory

    reset()
    csv_file_paths = uploaded_csv_file_paths
    output_directory = uploaded_output_dir

    csv_processing()

def reset():
    global preferences_csv, preferences_reader, studenttograde, emailtoname, total_emails, emails, schedules, classes_reader, num_periods, seminars_by_period, classes, class_capacities, master_list

    preferences_reader = 0
    preferences_csv = 0

    # can consider removing this dictionary as it's not needed
    studenttograde = {}
    emailtoname = {}

    total_emails = []
    emails = []
    schedules = []

    classes_reader = 0
    num_periods = 3
    num_preferences_per_period = 5

    seminars_by_period = [[] for _ in range(num_periods)]
    classes = []
    class_capacities = [[] for _ in range(num_periods)]
    master_list = []




def csv_processing():
    global num_periods, preferences_csv, preferences_reader, studenttograde, emailtoname, classes_csv, classes_reader, classes, class_capacities, total_emails, emails, master_list, schedules, csv_file_paths, seminars_by_period

    try:
        os.mkdir(output_directory)
    except FileExistsError:
        pass
    except PermissionError:
        status.log("Cannot create/open target directory")
        return
    
    for path in csv_file_paths:
        try:
            assert path
        except AssertionError:
            status.log()

    # break try catch statements
    try:
        # DONE: Change variable to filename for hardcoding
        preferences_csv = open("PD_CSV/testing_data_sample.csv")
        preferences_reader = csv.reader(preferences_csv)

        for x, teacher in enumerate(preferences_reader):
            emailtoname[teacher[1]] = teacher[1].split('@')[0]
            emails += [teacher[1]]

        # Temporarily commented out until mr conklin gets back with list of email to names and this can be hardcoded
        
        # studenttograde_csv = open(csv_file_paths['grades'])
        # studenttograde_reader = csv.reader(studenttograde_csv) 

        # writes emails in
        # for student in studenttograde_reader: #studenttograde_reader just reads the grades CSV.
        #     emailtoname[student[0]] = student[2]
        #     emails += [student[0]]

        num_students = sum(1 for _ in preferences_reader)

        preferences_csv.seek(0)

        schedules = []
        for _ in range(num_periods):
            schedules += [[0] * len(emails)]

        # CHANGE THIS TO HARD CODE AS WELL.
        classes_csv = open("PD_CSV/seminar_roomassignments.csv")
        classes_reader = csv.reader(classes_csv)

        period_capacities = [0 for i in range(num_periods)]

        # fills in class capacities in the classes list
        for aclass in classes_reader:
            print(aclass)
            classes += [aclass[0]]
            for x, room in enumerate(aclass[1:]):
                class_capacities[x] += [int(roomCapacities[room.strip()])]
                period_capacities[x] += int(roomCapacities[room.strip()])

                if room != "0":
                    seminars_by_period[x].append(aclass[0])


        Presenting_Seminar = ["Presenting","Check Schedule","Check Schedule","Check Schedule"]
    
        classes += [Presenting_Seminar[0]]
        for x, room in enumerate(Presenting_Seminar[1:]):
            class_capacities[x] += [int(roomCapacities[room.strip()])]
            period_capacities[x] += int(roomCapacities[room.strip()])

        # Remove all duplicate students TODO: fill missing students !!!DONE!!!
        rows = []
        missing_students = deepcopy(emails)
        for student in preferences_reader:
            email = student[1]
            total_emails.append(email)
            for x, s in enumerate(missing_students):
                if s == email:
                    missing_students.pop(x)

            print(student)

        for email in missing_students:

            print("MISSING STUDENT:", email)

            total_emails.append(email)

            student = ["time", email]

            for period in range(num_periods):

                for _ in range(num_preferences_per_period):
                    student.append(
                        seminars_by_period[period][random.randint(0, len(seminars_by_period[period])-1)]
                    )

            for _ in range(20):
                student.append("")

            studenttograde[email] = 0
            rows += [student]
        
        write_prefs = open("PD_CSV/testing_data_sample.csv", "at", newline='')
        preferences_writer = csv.writer(write_prefs)
        preferences_writer.writerows(rows)
        write_prefs.close()

        preferences_csv.seek(0)

        for period in range(num_periods):
            try:
                # num = num_students/2 if (period == 2 or period == 3) else num_students
                num = num_students # we shouldn't have to deal with funny situations so I'm commenting it out
                assert (period_capacities[period] >= num)
            except AssertionError:
                raise AssertionError(f"Not enough slots for students in period {period}, {period_capacities[period]} < {num}")
            
        # initializing master list, ignore variable names :pleading_face:
        master_list = []
        for i in range(len(classes)):
            ohio = []
            for j in range(num_periods):
                ohio.append([])
            master_list.append(ohio)

    except AssertionError as a:
       # status.log(a.args[0])
        print(a.args[0])
        return
    except Exception as e:
        raise e
    
    

    for period in range(num_periods):
        try:
            main(period)
        except Exception as e:
            status.log(f"ERROR SCHEUDLING PERIOD {period}\n {e}")
            print(f"ERROR SCHEUDLING PERIOD {period}\n {e}")
            raise e
        # status.log(f"Period {period} scheduled")
        print(f"Period {period+1} scheduled")

    # status.log("Min Cost Flow solved, outputting...")
    print("Min Cost Flow solved,outputting...")
    output()

    

def main(period):

    global preferences_csv, preferences_reader, classes, class_capacities, studenttograde, total_emails, emails, schedules, status, seminars_by_period

    """Solving an Assignment Problem with MinCostFlow."""
    # Instantiate a SimpleMinCostFlow solver.
    smcf = min_cost_flow.SimpleMinCostFlow()

    num_classes = len(classes)

    source_start_nodes = []
    source_end_nodes = []
    source_costs = []

    student_start_nodes = []
    student_end_nodes = []
    student_costs = []

    #initialize all class
    class_start_nodes = [x+1 for x in range(num_classes)] * 2

    # tldr loop through this shit twice because of the two costs thingy

    class_costs = [-10000000000] * num_classes
    class_costs += [0] * num_classes
    
    # priority to fill minimum
    

    student_index = 0

    classes_per_period = 5

    #index in the csv where periods start
    # for example: time, name, yes/no, CLASS 1 would be index 3
    initial_index = 3

    min_per_class = 1

    
    
    # the malicious
    class_capacities[period] += [min_per_class] * num_classes
    # subtract off MIN VAL to make sure all capacities are as intended
    for i in range(num_classes):
        if class_capacities[period][i] >= min_per_class:
            class_capacities[period][i] -= min_per_class
        else:
            # set corresp. to 0
            class_capacities[period][i + num_classes] = class_capacities[period][i]
            class_capacities[period][i] = 0
    
    flag = False
    preferences_csv.seek(0)
    preferences_reader = csv.reader(preferences_csv)

    ### CHANGE THIS!!!

    for student in preferences_reader:

        student_index += 1
        # create edge between source and students
        source_start_nodes += [0]
        source_end_nodes += [num_classes + student_index]
        source_costs += [0]

        # Time to deal with duplicate and invalid preferences, first create a list of avaliable seminars for the period
        # if they aren't presenting that is:
        temp = deepcopy(seminars_by_period[period])

        # remove the seminars students have already been scheduled into
        if period != 0:
            for p in range(period):
                try:
                    temp.remove(classes[schedules[p][student_index-1]])
                except:
                    continue

        replace = []
        for pref in range(classes_per_period):
            try:
                temp.remove(student[initial_index + pref + (period) * num_preferences_per_period])
            except ValueError:
                replace += [pref]
            
        if len(replace) > 0:

            print(
                f"Replacing {emailtoname[student[1]]}'s preferences period {period+1}"
            )
            for index, a in enumerate(replace):

                start = initial_index + (period) * num_preferences_per_period + a
                end = initial_index + (period + 1) * num_preferences_per_period - 1

                for pref in range(start, end):
                    student[pref - 1] = student[pref]

            
                for pref in range(index+1, len(replace)):
                    replace[pref] -= 1

                randomval = random.randint(0, len(temp)-1)
                student[initial_index + 4 + (period) * num_preferences_per_period] = temp[randomval]


        for pref in range(classes_per_period):
            # find ID of class that student wants
            # insert at preference
            # period = 1: 1 2 3 4 5
            # period = 2: 6 7 8 9 10

            pref_class = student[initial_index + pref + (period) * num_preferences_per_period]
            if pref_class[-2:] == '""':
                pref_class = pref_class[:-2]
            print(classes)
            class_id = classes.index(pref_class)


            # connect student nodes to classes
            student_start_nodes += [num_classes + student_index]
            student_end_nodes += [class_id + 1]
            # j is cost, weighted by weight. heavier means more influence
            weight = 10000 - student_index

            student_costs += [weight * pref]

    

    # 0, number of classes, number of students, THEN the sink
    # 1 + num_classes + student_index
    # this should be the terminus
    class_end_nodes = [num_classes + student_index + 1] * len(class_start_nodes) * 2

    source_capacities = [1] * len(source_start_nodes)
    student_capacities = [1] * len(student_start_nodes)


    start_nodes = (
        source_start_nodes + student_start_nodes + class_start_nodes
    )
    end_nodes = (
        source_end_nodes + student_end_nodes + class_end_nodes
    )
    capacities = (
        source_capacities + student_capacities + class_capacities[period]
    )
    costs = (
        source_costs + student_costs + class_costs
    )
    print("PHASE 1")
    print(len(source_start_nodes), len(student_start_nodes), len(class_start_nodes), len(start_nodes))
    print(len(source_end_nodes), len(student_end_nodes), len(class_end_nodes), len(end_nodes))
    print(len(source_capacities), len(student_capacities), len(class_capacities[period]), len(capacities))
            

    source = 0
    sink = num_classes + student_index + 1
    supplies = [student_index] + [0] * (num_classes + student_index) + [-student_index]

    # Add each arc.
    for i in range(len(start_nodes)):
        smcf.add_arc_with_capacity_and_unit_cost(
            start_nodes[i], end_nodes[i], capacities[i], costs[i]
        )
    # Add node supplies.
    for i in range(len(supplies)):
        smcf.set_node_supply(i, supplies[i])

    # Find the minimum cost flow between node 0 and node 10.
    smcf_status = smcf.solve()

    

    if smcf_status == smcf.OPTIMAL:
        print("Total cost = ", smcf.optimal_cost())
        print()
        for arc in range(smcf.num_arcs()):
            if smcf.flow(arc) > 0 and smcf.tail(arc) != source and smcf.head(arc) != sink:

                if smcf.tail(arc) - num_classes - 1 >= len(emails):
                    break

                # print(
                #     "Student %s assigned to class %s.  Cost = %d, Flow = %d"
                #     % (emails[smcf.tail(arc) - num_classes - 1], classes[smcf.head(arc) - 1], smcf.unit_cost(arc), smcf.flow(arc))
                # )
                schedules[period][smcf.tail(arc) - num_classes - 1] = smcf.head(arc) - 1
                master_list[smcf.head(arc) - 1][period].append(total_emails[smcf.tail(arc) - num_classes - 1])

                # print(master_list[0][period])

    else:
        raise Exception("There was an issue with the min cost flow input." + f"Status: {smcf_status}")

def output():
 
    global total_emails, emails, num_periods, schedules, classes, master_list, output_directory, classes_csv, classes_reader

    location = output_directory

    classes_csv.seek(0)

    # creates a dictionary that maps classes to their room assignments for ALL periods
    class_to_room = {}
    for aclass in classes_reader:
        class_to_room[aclass[0]] = aclass[1:]

    # class_to_room["First Lunch"] = ["0", "0", "Lunch", "0", "0"]
    # class_to_room["Second Lunch"] = ["0", "0", "0", "Lunch", "0"]
    class_to_room["Presenting"] = ["Check Schedule", "Check Schedule", "Check Schedule"]

    try:
        os.mkdir(location + "\\Students")
    except FileExistsError:
        pass
    except PermissionError:
        # status.log("Could not create output folders")
        print("Could not create output folders")
        return

    for i in range(len(emails)):

        name = emailtoname[total_emails[i]]

        seminars = []
        for j in range(num_periods):
            seminars += [str(classes[schedules[j][i]])]
        print(emails[i], seminars)

        # if total_emails[i] in student_led_seminar_students:
        #     seminars[4] = "Student Run Seminar - Arcade Extravaganza"

        rooms = []
        for x, seminar in enumerate(seminars):
            rooms.append(class_to_room[seminar][x])

        fin = []
        for x in range(num_periods):
            fin.append(f"{rooms[x]}: {seminars[x]}\n")

        # status.log("Creating schedule for student " + name)
        print("Creating schedule for " + name)

        f = open(f"{location}\\Students\\{name} Schedule.txt","w", newline='')
        f.writelines(fin)
        f.close()

    # status.log("Schedules complete")
    print("Schedules complete")

    too_empty_seminars = []
    
    # master_list: it works like, master_list[class][period]
    for i in range(len(classes)):
        for j in range(num_periods):
            print(classes[i], "Period " + str(j), master_list[i][j])
            if class_to_room[classes[i]][j] == "0":
                continue

            try:
                os.mkdir(location + "\\SeminarAttendances")
            except FileExistsError:
                pass
            except PermissionError:
                status.log("Could not create output folders")
                return
            
            # status.log(f"Creating attendance for class {classes[i]} period {j+1}")

            f = open(f"{location}\\SeminarAttendances\\{classes[i].split('-')[0]}Period{j+1}.csv", "w")


            names = deepcopy(master_list[i][j])
            for x, email in enumerate(names):
                names[x] = emailtoname[email]
            if len(names) < 5:
                too_empty_seminars.append(f"{classes[i]} Period {j+1}")
            f.write("\n".join(names))
            f.close()

    print(too_empty_seminars)
    for s in too_empty_seminars:
        print(s)

    # status.log("Master Lists complete")
    print("Master lists complete")
    #Identified by web interface to tell if completed
    # status.log("Success")
    print("Success")

csv_processing()