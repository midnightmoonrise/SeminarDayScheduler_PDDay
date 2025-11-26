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

# TODO: output to pdf
# TODO: some output thing
# TODO: Get rid of grade distinctions
# TODO: Missing teachers change to most popular seminars (if time, lowest priority)

# duplicate preferences can be done during preproccesing >>> done
# duplicate teachers has also been handled (incase that happens somehow)

# teachers not responding can be dealt with in pre or post processing
# pre-processing would be adding missing teachers with random preferences  >>> done, missing teachers also have the least weight
# post-processing would be adding missing teachers into any avaliable seminars



output_directory = "Output"

csv_file_paths = {}

forms_reader = 0
forms_csv = 0

preferences_reader = 0
preferences_csv = 0

teachertograde = {}
emailtoname = {}

# use a CSV File to read room capacities
roomCapacities = {}
with open("PD_CSV/roomlist.csv", newline='') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        roomCapacities[row["room"]] = row["capacity"]

ordered_emails = []
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
    global preferences_csv, preferences_reader, teachertograde, emailtoname, ordered_emails, emails, schedules, classes_reader, num_periods, seminars_by_period, classes, class_capacities, master_list

    preferences_reader = 0
    preferences_csv = 0

    # can consider removing this dictionary as it's not needed
    teachertograde = {}
    emailtoname = {}

    ordered_emails = []
    emails = []
    schedules = []

    classes_reader = 0
    num_periods = 3

    seminars_by_period = [[] for _ in range(num_periods)]
    classes = []
    class_capacities = [[] for _ in range(num_periods)]
    master_list = []




def csv_processing():
    global num_periods, preferences_csv, preferences_reader, teachertograde, emailtoname, classes_csv, classes_reader, classes, class_capacities, ordered_emails, emails, master_list, schedules, csv_file_paths, seminars_by_period

    try:
        os.mkdir(output_directory)
    except FileExistsError:
        pass
    except PermissionError:
        # status.log("Cannot create/open target directory")
        return
    
    for path in csv_file_paths:
        try:
            assert path
        except AssertionError as e:
            # status.log()
            raise e


    # break try catch statements
    try:
        # DONE: Change variable to filename for hardcoding
        preferences_csv = open("PD_CSV/preferences_data.csv")
        preferences_reader = csv.reader(preferences_csv)

        # for x, teacher in enumerate(preferences_reader):
        #     emailtoname[teacher[1]] = teacher[1].split('@')[0]
        #     emails += [teacher[1]]
        
        # MAKE SURE TO CHANGE THIS TO THE REAL TEACHER NAMES BEFORE YOU RUN THE REAL THING!!
        teachertograde_csv = open("PD_CSV/teachernames.csv")
        teachertograde_reader = csv.reader(teachertograde_csv) 

        # writes emails in
        for teacher in teachertograde_reader: #teachertograde_reader just reads the teachernames CSV.
            emailtoname[teacher[0]] = teacher[1]
            emails += [teacher[0]]
        print(emails)

        num_teachers = sum(1 for _ in preferences_reader)

        preferences_csv.seek(0)

        schedules = []
        for _ in range(num_periods):
            schedules += [[0] * len(emails)]

        # CHANGE THIS TO HARD CODE AS WELL.
        classes_csv = open("PD_CSV/seminar_roomassignments.csv")
        classes_reader = csv.reader(classes_csv)

        period_capacities = [0 for _ in range(num_periods)]

        # fills in class capacities in the classes list. THIS WORKS. 
        for aclass in classes_reader:
            print(aclass)
            classes += [aclass[0]]
            for x, room in enumerate(aclass[1:]):
                class_capacities[x] += [int(roomCapacities[room.strip()])]
                period_capacities[x] += int(roomCapacities[room.strip()])

                if room != "0":
                    seminars_by_period[x].append(aclass[0])
    
        # specific case handling for a presenting "seminar"
        Presenting_Seminar = ["Presenting","Check Schedule","Check Schedule","Check Schedule"]
    
        classes += [Presenting_Seminar[0]]
        for x, room in enumerate(Presenting_Seminar[1:]):
            class_capacities[x] += [int(roomCapacities[room.strip()])]
            period_capacities[x] += int(roomCapacities[room.strip()])

        preferences_csv.seek(0)

        # Populates missing_teachers with the missing teachers
        rows = []
        missing_teachers = deepcopy(emails)
        for teacher in preferences_reader:
            email = teacher[1]

            # sorting them according to the preferences order
            ordered_emails.append(email)

            # Remove it from this list because its not missing
            missing_teachers.pop(missing_teachers.index(email))

            # Populates the seminar "Presenting" in the blank spots for teachers who are presenting
            if teacher[2] == "Yes":
                for i in range(3,8):
                    teacher[i] = "Presenting"
            if teacher[8] == "Yes":
                for i in range(9,14):
                    teacher[i] = "Presenting"
            if teacher[14] == "Yes":
                for i in range(15,20):
                    teacher[i] = "Presenting"

            print(teacher)
            rows += [teacher]
        

        for email in missing_teachers:

            # sorting them according to the preferences order
            ordered_emails.append(email)

            print("MISSING teacher:", email)

            teacher = ["time", email]

            temp = deepcopy(seminars_by_period)

            for period in range(num_periods):

                for _ in range(num_preferences_per_period):

                    r = random.randint(0, len(temp[period])-1)
                    sem = temp[period][r]
                    temp[period].pop(r)

                    teacher.append(
                        sem
                    )
            # Casework for when missing teachers are presenting.
            presenting_period_1 = ["Tom Duprey", "Mike Sweeney", "Alex Carroll"]
            presenting_period_2 = ["Tom Duprey", "Toni Milbourn", "Andrew McCorkle", "Mike Sweeney", "Alex Carroll", "Addie Perez Krebs"]
            presenting_period_3 = ["Toni Milbourn", "Andrew McCorkle", "Phil Rodino", "Addie Perez Krebs"]
            # Add the Yes/No (No matters because the code to handle presenting checks for "No", not "Yes")
            if emailtoname[teacher[1]] in presenting_period_1:
                print(f"{emailtoname[teacher[1]]} is presenting period 1")
                teacher[2] = "Yes"
                for i in range(3,8):
                    teacher[i] = "Presenting"
            else:
                teacher[2] = "No"
            if emailtoname[teacher[1]] in presenting_period_2:
                print(f"{emailtoname[teacher[1]]} is presenting period 2")
                teacher[8] = "Yes"
                for i in range(9,14):
                    teacher[i] = "Presenting"
            else:
                teacher[8] = "No"
            if emailtoname[teacher[1]] in presenting_period_3:
                print(f"{emailtoname[teacher[1]]} is presenting period 3")
                teacher[14] = "Yes"
                for i in range(15,20):
                    teacher[i] = "Presenting"
            else:
                teacher[14] = "No"
                
            teachertograde[email] = 0
            rows += [teacher]        

        # The below writes the prefs for the missing teachers, and the missing teachers ONLY.
        # rn it actually writes all of them, including updating any empty preferences after a "Yes" to "Presenting".
        # realistically this shold open to the same file that we read prefrences from
        write_prefs = open("PD_CSV/preferences_data.csv", "wt", newline='')
        preferences_writer = csv.writer(write_prefs)
        preferences_writer.writerows(rows)
        write_prefs.close()

        preferences_csv.seek(0)

        for period in range(num_periods):
            try:
                num = num_teachers 
                assert (period_capacities[period] >= num)
            except AssertionError:
                raise AssertionError(f"Not enough slots for teachers in period {period}, {period_capacities[period]} < {num}")
            
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
            # status.log(f"ERROR SCHEUDLING PERIOD {period}\n {e}")
            print(f"ERROR SCHEUDLING PERIOD {period}\n {e}")
            raise e
        # status.log(f"Period {period} scheduled")
        print(f"Period {period+1} scheduled")

    # status.log("Min Cost Flow solved, outputting...")
    print("Min Cost Flow solved,outputting...")
    output()

    

def main(period):

    global preferences_csv, preferences_reader, classes, class_capacities, ordered_emails, emails, schedules, seminars_by_period

    """Solving an Assignment Problem with MinCostFlow."""
    # Instantiate a SimpleMinCostFlow solver.
    smcf = min_cost_flow.SimpleMinCostFlow()

    num_classes = len(classes)

    source_start_nodes = []
    source_end_nodes = []
    source_costs = []

    teacher_start_nodes = []
    teacher_end_nodes = []
    teacher_costs = []

    #initialize all class
    class_start_nodes = [x+1 for x in range(num_classes)] * 2

    # tldr loop through this shit twice because of the two costs thingy

    # they were backwards for some reason???
    class_costs = [0] * num_classes
    class_costs += [-10000000] * num_classes
    
    # priority to fill minimum
    

    teacher_index = 0 

    classes_per_period = 5

    #index in the csv where periods start
    # for example: time, name, yes/no, CLASS 1 would be index 3
    initial_index = 3

    min_per_class = 3

    
    
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

    for teacher in preferences_reader:

        teacher_index += 1
        # create edge between source and teachers
        source_start_nodes += [0]
        source_end_nodes += [num_classes + teacher_index]
        source_costs += [0]

        # Time to deal with duplicate and invalid preferences, first create a list of avaliable seminars for the period
        # if they aren't presenting that is:
        if teacher[initial_index + period*num_preferences_per_period - 1] == "No":
            temp = deepcopy(seminars_by_period[period])

            # remove the seminars teachers have already been scheduled into
            if period != 0:
                for p in range(period):
                    try:
                        temp.remove(classes[schedules[p][teacher_index-1]])
                    except:
                        continue

            replace = []
            for pref in range(classes_per_period):
                try:
                    temp.remove(teacher[initial_index + pref + (period) * num_preferences_per_period])
                except ValueError:
                    replace += [pref]
                
            if len(replace) > 0:

                print(
                    f"Replacing {emailtoname[teacher[1]]}'s preferences {replace} period {period+1}"
                )
                for index, replace_pref in enumerate(replace):

                    # Find the range of preferences we gotta shift over
                    start = initial_index + (period) * num_preferences_per_period + replace_pref
                    end = initial_index + (period + 1) * num_preferences_per_period - 2

                    # Shift over each preference, put the replaced one last
                    for pref in range(start, end):
                        teacher[pref] = teacher[pref + 1]

                    # If there are any other preferences to replace, they were just shifted so we gotta fix that
                    for pref in range(index+1, len(replace)):
                        replace[pref] -= 1

                    # Choose a random seminar, put it in, then remove it so it cant be selected again
                    randomval = random.randint(0, len(temp)-1)
                    teacher[initial_index + 4 + (period) * num_preferences_per_period] = temp[randomval]
                    temp.pop(randomval)
        else:
            for pref in range(classes_per_period):
                teacher[initial_index + period*num_preferences_per_period + pref] = "Presenting"

        print("BEGIN PREFERENCES IN RANGE(CLASSES_PER_PERIOD)")
        for pref in range(classes_per_period):
            # find ID of class that teacher wants
            # insert at preference
            # period = 1: 1 2 3 4 5
            # period = 2: 6 7 8 9 10

            pref_class = teacher[initial_index + pref + (period) * num_preferences_per_period]
            if pref_class[-2:] == '""':
                pref_class = pref_class[:-2]
            class_id = classes.index(pref_class.strip())


            # connect teacher nodes to classes
            teacher_start_nodes += [num_classes + teacher_index]
            teacher_end_nodes += [class_id + 1]
            # j is cost, weighted by weight. heavier means more influence
            weight = 10000 - teacher_index

            teacher_costs += [weight * pref]

    

    # 0, number of classes, number of teachers, THEN the sink
    # 1 + num_classes + teacher_index
    # this should be the terminus
    class_end_nodes = [num_classes + teacher_index + 1] * len(class_start_nodes)

    source_capacities = [1] * len(source_start_nodes)
    teacher_capacities = [1] * len(teacher_start_nodes)


    start_nodes = (
        source_start_nodes + teacher_start_nodes + class_start_nodes
    )
    end_nodes = (
        source_end_nodes + teacher_end_nodes + class_end_nodes
    )
    capacities = (
        source_capacities + teacher_capacities + class_capacities[period]
    )
    costs = (
        source_costs + teacher_costs + class_costs
    )
    print("PHASE 1")
    print(len(source_start_nodes), len(teacher_start_nodes), len(class_start_nodes), len(start_nodes))
    print(len(source_end_nodes), len(teacher_end_nodes), len(class_end_nodes), len(end_nodes))
    print(len(source_capacities), len(teacher_capacities), len(class_capacities[period]), len(capacities))
            

    source = 0
    sink = num_classes + teacher_index + 1
    supplies = [teacher_index] + [0] * (num_classes + teacher_index) + [-teacher_index]

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
                #     "teacher %s assigned to class %s.  Cost = %d, Flow = %d"
                #     % (emails[smcf.tail(arc) - num_classes - 1], classes[smcf.head(arc) - 1], smcf.unit_cost(arc), smcf.flow(arc))
                # )
                schedules[period][smcf.tail(arc) - num_classes - 1] = smcf.head(arc) - 1
                master_list[smcf.head(arc) - 1][period].append(ordered_emails[smcf.tail(arc) - num_classes - 1])

                # print(master_list[0][period])

    else:
        raise Exception("There was an issue with the min cost flow input." + f"Status: {smcf_status}")

def output():
 
    global ordered_emails, emails, num_periods, schedules, classes, master_list, output_directory, classes_csv, classes_reader

    location = output_directory

    classes_csv.seek(0)

    # creates a dictionary that maps classes to their room assignments for ALL periods
    class_to_room = {}
    for aclass in classes_reader:
        class_to_room[aclass[0]] = aclass[1:]
    class_to_room["Presenting"] = ["Check Schedule", "Check Schedule", "Check Schedule"]

    try:
        os.mkdir(location + "\\teachers")
    except FileExistsError:
        pass
    except PermissionError:
        # status.log("Could not create output folders")
        print("Could not create output folders")
        return

    for teacher_id in range(len(emails)):

        name = emailtoname[ordered_emails[teacher_id]]

        seminars = []
        for period in range(num_periods):
            seminars += [str(classes[schedules[period][teacher_id]])]
        print(ordered_emails[teacher_id], seminars)

        # if emails[i] in teacher_led_seminar_teachers:
        #     seminars[4] = "teacher Run Seminar - Arcade Extravaganza"

        rooms = []
        for x, seminar in enumerate(seminars):
            rooms.append(class_to_room[seminar][x])

        fin = []
        for x in range(num_periods):
            fin.append(f"{rooms[x]}: {seminars[x]}\n")

        # status.log("Creating schedule for teacher " + name)
        print("Creating schedule for " + name)

        f = open(f"{location}\\teachers\\{name} Schedule.txt","w", newline='')
        f.writelines(fin)
        f.close()

    # status.log("Schedules complete")
    print("Schedules complete")

    too_empty_seminars: list[str] = []
    
    # master_list: it works like, master_list[class][period]
    for class_id in range(len(classes)):
        for period in range(num_periods):
            if class_to_room[classes[class_id]][period] == "0":
                continue
            print(classes[class_id], "Period " + str(period), master_list[class_id][period])

            try:
                os.mkdir(location + "\\SeminarAttendances")
            except FileExistsError:
                pass
            except PermissionError as e:
                # status.log("Could not create output folders")
                raise e
            
            # status.log(f"Creating attendance for class {classes[i]} period {j+1}")

            f = open(f"{location}\\SeminarAttendances\\{classes[class_id].split('-')[0]}Period{period+1}.csv", "w")


            names = deepcopy(master_list[class_id][period])
            for x, email in enumerate(names):
                names[x] = emailtoname[email]
            if len(names) < 5:
                too_empty_seminars.append(f"{classes[class_id]} Period {period+1}")
            f.write("\n".join(names))
            f.close()

    print("These classes don't have enough people:\n")

    # print(too_empty_seminars)
    for s in too_empty_seminars:
        class_id = classes.index(s[:s.index("Period")].strip())
        period = int(s[-1])-1
        people = master_list[class_id][period]
        print(s, f"with {len(people)} attendees:\n", people, "\n")

    # status.log("Master Lists complete")
    print("Master lists complete")
    #Identified by web interface to tell if completed
    # status.log("Success")
    print("Success")

csv_processing()