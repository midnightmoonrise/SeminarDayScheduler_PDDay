"""Linear assignment example."""
from ortools.graph.python import min_cost_flow
import csv 
import random
import os
from copy import deepcopy

the_list = [
    "Emerson Hirsch", "Daniel Spilman", "Jacob Spilman", "Karn Chutinan", "Serena Baranello", "Selin Gulden", "Daniel Xue", "Iris Chen", "Ethan Filip", "Cecilia Ritchey", "Addison Hirsch", "Alexander Mroz", "Isaac Lee",
    "Elijah Littlefield", "Jaideep Padhi", "Nicholas Wallen", "Kylie Ozerdam", "Selena Pu", "Kaelyn Wu", "Ryan Li", "Gabriel Goldstein", "Felix Giesen", "Eric Liang", "Devon Ntiforo", "Julia Ritchey", "Siming Chen"
]

for x in range(len(the_list)):
    first, last = the_list[x].split(" ")
    the_list[x] = last.lower() + "." + first.lower() + "@doversherborn.org"

student_led_seminar_students = [
    "Jacob Spilman", "Nathan Zeng", "Vivian Kamphaus", "Alexander Mroz", "Patrick Driscoll", "Simon Hart", "Joshua Dias", "Gabriella Schroeder", "Dagny Abbett", "Nora Olson", "james davies", "tessa correll",
    "Armaan Tamber", "Cillian Moss", "Felix Giesen" 
]

for x in range(len(student_led_seminar_students)):
    first, last = student_led_seminar_students[x].split(" ")
    student_led_seminar_students[x] = last.lower() + "." + first.lower() + "@doversherborn.org"

# TODO: output to pdf
# TODO: some output thing
# TODO: STUDENT LED SEMINAR

# for lunches:
# create a class node period 3 and 4 that takes (half?) of the students with weight 0 going to it, any students who choose or are selected for lunch
# will only have an edge to lunch at cost 0. essentially overwrite their choices

# lunches are done, freshman and sophomores are put into first lunch, juniors and seniors into second lunch. Preferences are overwritten.
# alternative, create a preference to first or second lunch, could be formatted with help from google forms

# duplicate preferences can be done during preproccesing >>> done
# duplicate students has also been handled (incase that happens somehow)

# students not responding can be dealt with in pre or post processing
# pre-processing would be adding missing students with random preferences  >>> done, missing students also have the least weight
# post-processing would be adding missing students into any avaliable seminars



output_directory = ''

csv_file_paths = {}

forms_reader = 0
forms_csv = 0

preferences_reader = 0
preferences_csv = 0

studenttograde = {}
emailtoname = {}
roomtocapacity = {
    "0":0,
"105":22,
"106":22,
"107":22,
"110A":22,
"110B":22,
"114":22,
"115":22,
"116":22,
"119":22,
"120":22,
"121":22,
"122":22,
"123":22,
"202":22,
"203":22,
"204":22,
"205":22,
"206":22,
"207":22,
"213":22,
"214":22,
"215":22,
"216":22,
"220":22,
"221":22,
"222":22,
"223":22,
"224":22,
"225":22,
"226":22,
"227":22,
"103 S":22,
"105 S":22,
"106 S":22,
"107 S":22,
"109 S":22,
"112 S":22,
"114 S":22,
"Auditorium":125,
"Band Room":75,
"Fitness/Weight Room":18,
"HS Gym":75,
"Library":48,
"MS Choral Room":60
}

total_emails = []
emails = []
schedules = []

classes_reader = 0
num_periods = 5

seminars_by_period = [[] for _ in range(num_periods)]

classes = []
class_capacities = [[] for _ in range(num_periods)]
master_list = []

class Status():
    #Web interface displays whatever this variable is set to
    currentLog = 'Starting...'

    #def __init__(this, stringvar: tk.StringVar, window: tk.Tk):
        #this.stringvar = stringvar
        #this.window = window

    def log(this, string):
        #this.stringvar.set(string)
        #this.window.update()
        #this.window.update_idletasks()
        this.currentLog = string
        print(string)

    #def get(this):
        #return this.stringvar.get()

status = Status()

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

    studenttograde = {}
    emailtoname = {}

    total_emails = []
    emails = []
    schedules = []

    classes_reader = 0
    num_periods = 5

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
        preferences_csv = open(csv_file_paths['prefs'])
        preferences_reader = csv.reader(preferences_csv)

        studenttograde_csv = open(csv_file_paths['grades'])
        studenttograde_reader = csv.reader(studenttograde_csv)

        num_students = sum(1 for _ in preferences_reader)

        preferences_csv.seek(0)

        lunch_capacities = [0, 0]

        for student in studenttograde_reader:
            studenttograde[student[0]] = int(student[1])
            emailtoname[student[0]] = student[2]
            emails += [student[0]]
            if int(student[1]) < 11:
                lunch_capacities[0] += 1
            else:
                lunch_capacities[1] += 1

        schedules = []
        for i in range(num_periods):
            schedules += [[0] * len(emails)]

        classes_csv = open(csv_file_paths['seminars'])
        classes_reader = csv.reader(classes_csv)

        period_capacities = [0, 0, 0, 0, 0]

        for aclass in classes_reader:
            print(aclass)
            classes += [aclass[0]]
            for x, room in enumerate(aclass[1:]):
                class_capacities[x] += [int(roomtocapacity[room.strip()])]
                period_capacities[x] += int(roomtocapacity[room.strip()])

                if room != "0":
                    seminars_by_period[x].append(aclass[0])

        

        # Remove all duplicate students TODO: fill missing students !!!DONE!!!
        rows = []
        missing_students = deepcopy(emails)
        for student in preferences_reader:
            email = student[1]
            total_emails.append(email)
            for x, s in enumerate(missing_students):
                if s == email:
                    missing_students.pop(x)
                    if student[0] == "time":
                        studenttograde[email] = 0

        for email in missing_students:

            print("MISSING STUDENT:", email)

            total_emails.append(email)

            student = ["time", email, "grade"]

            for period in range(num_periods):

                if period == 3:
                    continue

                for _ in range(5):
                    student.append(
                        seminars_by_period[period][random.randint(0, len(seminars_by_period[period])-1)]
                    )

            for _ in range(20):
                student.append("")

            if studenttograde[email] > 10:
                lunch_capacities[1] -= 1
                lunch_capacities[0] += 1

            studenttograde[email] = 0
            rows += [student]
        
        write_prefs = open(csv_file_paths['prefs'], "at", newline='')
        preferences_writer = csv.writer(write_prefs)
        preferences_writer.writerows(rows)
        write_prefs.close()

        preferences_csv.seek(0)


        extras = [
            ["First Lunch", 0, 0, num_students, 0, 0],
            ["Second Lunch", 0, 0, 0, num_students, 0],
            ["Presenting", 0, 0, 0, 0, len(student_led_seminar_students)]
        ]

        for lunch in extras:
            classes += [lunch[0]]
            for x, capacity in enumerate(lunch[1:]):
                class_capacities[x] += [int(capacity)]
        

        for period in range(num_periods):
            try:
                num = num_students/2 if (period == 2 or period == 3) else num_students
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
        status.log(a.args[0])
        return
    except Exception as e:
        raise e.with_traceback()
    
    

    for period in range(num_periods):
        try:
            main(period)
        except Exception as e:
            status.log(f"ERROR SCHEUDLING PERIOD {period}\n {e}")
            raise e
        status.log(f"Period {period} scheduled")

    status.log("Min Cost Flow solved, outputting...")
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
    # for example: time, name, grade, CLASS 1 would be index 3
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
    for student in preferences_reader:
        # formatting to what we've been using (mfw)
        grade = studenttograde[student[1]]
        temp_prefs = deepcopy(student)
        offset = 0
        lunch = 3
        if grade > 10.5:
            offset = 20
            if student[0] == "timee":
                offset = 0
            lunch = 2
        for i in range(20):
            # currently, this sets entries 2 to 26 to be the SEMINAR NAMES
            # TODO: replace SEMINAR NAMES with ROOM NUMBERS or IDS
            student[i + initial_index] = temp_prefs[i + initial_index + offset]

        student_index += 1
        # create edge between source and students
        source_start_nodes += [0]
        source_end_nodes += [num_classes + student_index]
        source_costs += [0]
        senior_flag = (studenttograde[student[1]] == 12)
        missing_flag = (studenttograde[student[1]] == 0)
        flag = student[1] in the_list

        # Since we only capture 4 periods worth of data, we need to make sure we're treating the third set of 5 preferences correctly
        period_offset = 0
        if period > lunch:
            period_offset = 1

        # Time to deal with duplicate and invalid preferences, first create a list of avaliable seminars for the period
        if period != lunch:
            temp = deepcopy(seminars_by_period[period])

            if period == 4 and student[1] == "yuknat.jack@doversherborn.org":
                pass

            # remove the seminars students have already been scheduled into
            if period != 0:
                for p in range(period):
                    try:
                        temp.remove(classes[schedules[p][student_index-1]])
                    except:
                        continue

            replace = []
            for pref in range(5):
                try:
                    temp.remove(student[initial_index + pref + (period - period_offset) * 5])
                except ValueError:
                    replace += [pref]
                
            if len(replace) > 0:

                print(
                    f"Replacing {emailtoname[student[1]]}'s preferences period {period+1}"
                )
                for index, a in enumerate(replace):

                    # If we're replacing the last preference, no need to shift anything over
                    if a != 4:
                        
                        start = initial_index + (period - period_offset)*5 + a + 1
                        end = initial_index + (period - period_offset + 1)*5

                        for pref in range(start, end):

                            student[pref - 1] = student[pref]

                    
                        for pref in range(index+1, len(replace)):
                            replace[pref] -= 1

                    randomval = random.randint(0, len(temp)-1)
                    student[initial_index + 4 + (period - period_offset) * 5] = temp[randomval]


        for j in range(5):
            # find ID of class that student wants
            # insert at preference
            # period = 1: 1 2 3 4 5
            # period = 2: 6 7 8 9 10

            if student[1] in student_led_seminar_students and period == 4:
                class_id = classes.index("Presenting")
            elif period == lunch:
                if period == 2:
                    class_id = classes.index("First Lunch")
                elif period == 3:
                    class_id = classes.index("Second Lunch")
            else:
                pref_class = student[j + classes_per_period * (period - period_offset) + initial_index]
                if pref_class[-2:] == '""':
                    pref_class = pref_class[:-2]
                class_id = classes.index(pref_class)


            # connect student nodes to classes
            student_start_nodes += [num_classes + student_index]
            student_end_nodes += [class_id + 1]
            # j is cost, weighted by weight. heavier means more influence
            weight = 10000 - student_index
            if senior_flag:
                weight *= 10
            elif missing_flag:
                weight = int(weight/10)
            if flag:
                weight *= 100
            student_costs += [weight * j]

    

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

    class_to_room = {}
    for aclass in classes_reader:
        class_to_room[aclass[0]] = aclass[1:]

    class_to_room["First Lunch"] = ["0", "0", "Lunch", "0", "0"]
    class_to_room["Second Lunch"] = ["0", "0", "0", "Lunch", "0"]
    class_to_room["Presenting"] = ["0", "0", "0", "0", "107"]

    try:
        os.mkdir(location + "\\Students")
    except FileExistsError:
        pass
    except PermissionError:
        status.log("Could not create output folders")
        return

    for i in range(len(emails)):

        name = emailtoname[total_emails[i]]

        seminars = []
        for j in range(num_periods):
            seminars += [str(classes[schedules[j][i]])]
        print(emails[i], seminars)

        if total_emails[i] in student_led_seminar_students:
            seminars[4] = "Student Run Seminar - Arcade Extravaganza"

        rooms = []
        for x, seminar in enumerate(seminars):
            rooms.append(class_to_room[seminar][x])

        fin = []
        for x in range(num_periods):
            fin.append(f"{rooms[x]}: {seminars[x]}\n")

        status.log("Creating schedule for student " + name)

        f = open(f"{location}\\Students\\{name} Schedule.txt","w", newline='')
        f.writelines(fin)
        f.close()

    status.log("Schedules complete")

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
            
            status.log(f"Creating attendance for class {classes[i]} period {j+1}")

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

    status.log("Master Lists complete")
    #Identified by web interface to tell if completed
    status.log("Success")

    # emerson hirsch, daniel spilman, karn chutinan, serena baranello, selin gulden, amethyst xue, iris chen, ethan filip, cecilia ritchey, addison hirsch