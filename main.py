"""Linear assignment example."""
from ortools.graph.python import min_cost_flow
import csv
import tkinter as tk    
from tkinter import filedialog
from functools import partial 
import random
import os

# TODO: output to pdf, make the gui nicer (kivy or wxpython or qt)

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

window = tk.Tk()

output_directory = tk.StringVar()
output_directory.set(os.getcwd() + "\\Seminar Day Schedules")

csv_files = [[tk.StringVar(), False] for _ in range(3)]

preferences_reader = 0
preferences_csv = 0

myarray = [[] * 3]

studenttograde = {}

emails = []
schedules = []

classes_reader = 0
num_period = 4

classes = []
class_capacities = [[] for _ in range(num_period)]
master_list = []

class Status():

    def __init__(this, stringvar: tk.StringVar, window: tk.Tk):
        this.stringvar = stringvar
        this.window = window

    def log(this, string):
        this.stringvar.set(string)
        this.window.update()
        this.window.update_idletasks()

    def get(this):
        return this.stringvar.get()

status = Status(tk.StringVar(), window)

def reset():

    global preferences_csv, preferences_reader, studenttograde, emails, schedules, classes_reader, num_period, classes, class_capacities, master_list

    preferences_reader = 0
    preferences_csv = 0

    studenttograde = {}

    emails = []
    schedules = []

    classes_reader = 0
    num_period = 4

    classes = []
    class_capacities = [[] for _ in range(num_period)]
    master_list = []

def get_file_name(index):

    global csv_files

    root = tk.Tk()
    root.attributes('-topmost',True)
    root.withdraw()

    var = csv_files[index]
    
    file_path = filedialog.askopenfilename(filetypes=[("Comma Seperated Values",".csv")])
    if file_path[-4:] != ".csv":
        var[0].set("Please select a .csv file")
        var[1] = False
        return
    
    var[0].set(file_path)
    var[1] = True

    root.destroy()
    return

def get_output_folder():
    global output_directory

    root = tk.Tk()
    root.attributes('-topmost',True)
    root.withdraw()

    output_directory.set(filedialog.askdirectory())

    root.destroy()

def tkwindowthread():

    global window, csv_files, status

    width = window.winfo_screenwidth() / 8
    height = window.winfo_screenheight() / 2
    
    window.rowconfigure([x for x in range(6)], weight=1, minsize=height/8)
    window.columnconfigure([x for x in range(2)], weight=1, minsize=width/2)

    button_labels = ["Student Preferences", "Student Grades", "Available Seminars"]

    for i in range(3):
        button = tk.Button(master = window, text="Select "+button_labels[i], command=partial(get_file_name, i))
        button.grid(row=i, column=0)

        label = tk.Label(master=window, textvariable=csv_files[i][0], )
        label.grid(row=i, column=1)
    
    button = tk.Button(master = window, text="Select Output Folder", command=get_output_folder)
    button.grid(row=3, column=0)

    label = tk.Label(master = window, textvariable=output_directory)
    label.grid(row=3, column=1)

    button = tk.Button(master = window, text="Create Schedules", command=csv_processing)
    button.grid(row=4, column=0)

    label = tk.Label(master=window, textvariable=status.stringvar)
    label.grid(row=4, column=1)

    # for i in range(3):
    #     frame = tk.Frame(
    #         master=window,
    #         relief=tk.RAISED,
    #         borderwidth=1
    #     )
    #     frame.grid(row=i, column=0)
    #     button = tk.Button(master = frame, text="Select "+button_labels[i], command=partial(get_file_name, i))
    #     button.pack()

    #     frame = tk.Frame(
    #         master=window,
    #         borderwidth=1
    #     )
    #     frame.grid(row=i, column=1)
    #     label = tk.Label(master=frame, textvariable=csv_files[i][0])
    #     label.pack()
    
    # frame = tk.Frame(
    #     master=window,
    #     relief=tk.RAISED,
    #     borderwidth=1
    # )
    # frame.grid(row=3, column=0)
    # button = tk.Button(master = frame, text="Select Output Folder", command=get_output_folder)
    # button.pack()

    # frame = tk.Frame(
    #     master=window,
    #     borderwidth=1
    # )
    # frame.grid(row=3, column=1)
    # label = tk.Label(master = frame, textvariable=output_directory)
    # label.pack()

    # frame = tk.Frame(
    #     master=window,
    #     relief=tk.RAISED,
    #     borderwidth=1
    # )
    # frame.grid(row=4, column=0)
    # button = tk.Button(master = frame, text="Create Schedules", command=csv_processing)
    # button.pack()


    # frame = tk.Frame(
    #     master=window,
    #     borderwidth=1
    # )
    # frame.grid(row=4, column=1)
    # label = tk.Label(master=frame, textvariable=status.stringvar)
    # label.pack()



    #wip
    # print("wip")

    window.mainloop()

def csv_processing():

    reset()

    global num_period, preferences_csv, preferences_reader, studenttograde, classes_reader, classes, class_capacities, emails, master_list, schedules, csv_files

    try:
        os.mkdir(output_directory.get())
    except FileExistsError:
        pass
    except PermissionError:
        status.log("Cannot create/open target directory")
        return
    
    for i in range(3):
        try:
            assert csv_files[i][1]
        except AssertionError:
            status.log()


    # break try catch statements
    try:
        preferences_csv = open(csv_files[0][0].get())
        preferences_reader = csv.reader(preferences_csv)

        studenttograde_csv = open(csv_files[1][0].get())
        studenttograde_reader = csv.reader(studenttograde_csv)

        num_students = sum(1 for _ in preferences_reader)

        preferences_csv.seek(0)

        lunch_capacities = [0, 0]

        for student in studenttograde_reader:
            studenttograde[student[0]] = student[1]
            emails += [student[0]]
            if int(student[1]) < 11:
                lunch_capacities[0] += 1
            else:
                lunch_capacities[1] += 1

        schedules = []
        for i in range(num_period):
            schedules += [[0] * len(emails)]

        classes_csv = open(csv_files[2][0].get())
        classes_reader = csv.reader(classes_csv)

        period_capacities = [0, 0, 0, 0]

        for aclass in classes_reader:
            print(aclass)
            classes += [aclass[0]]
            for x, capacity in enumerate(aclass[1:]):
                class_capacities[x] += [int(capacity)]
                period_capacities[x] += int(capacity)

        # Remove all duplicate students TODO: fill missing students
        flag = True
        students = []
        rows = []
        missing_students = list(emails)
        for student in preferences_reader:
            name = student[1]
            duplicate = False
            for s in students:
                if s == name:
                    duplicate = True
                    break
            for x, s in enumerate(missing_students):
                if s == name:
                    missing_students.pop(x)
            if not duplicate:
                students += [name]
                rows += [student]

            if flag:
                flag = False

        for name in missing_students:
            student = ["time", name] + [classes[random.randint(0, len(classes) - 3)] for _ in range(20)]

            if studenttograde[name] > 10:
                lunch_capacities[1] -= 1
                lunch_capacities[0] += 1

            studenttograde[name] = 0
            rows += [student]
        
        write_prefs = open(csv_files[0][0].get(), "wt", newline='')
        preferences_writer = csv.writer(write_prefs)
        preferences_writer.writerows(rows)
        write_prefs.close()

        preferences_csv.seek(0)        

        lunches = [
            ["First Lunch", 0, 0, lunch_capacities[0], 0],
            ["Second Lunch", 0, 0, 0, lunch_capacities[1]]
        ]

        for lunch in lunches:
            classes += [lunch[0]]
            for x, capacity in enumerate(lunch[1:]):
                class_capacities[x] += [int(capacity)]

        for period in range(4):
            try:
                assert (period_capacities[period] >= num_students)
            except AssertionError:
                raise AssertionError(f"Not enough slots for students in period {period}")
        master_list = []
        for i in range(len(classes)):
            ohio = []
            for j in range(num_period):
                ohio += [ [] ]
            master_list += [ohio]
    except AssertionError as a:
        status.log(a.args[0])
        return
    except Exception as e:
        raise e

    for period in range(num_period):
        try:
            main(period)
        except Exception as e:
            status.log(f"ERROR SCHEUDLING PERIOD {period}\n {e}")
            raise e
        status.log(f"Period {period} scheduled")

    status.log("Min Cost Flow solved, outputting...")
    output()

    

def main(period):

    global preferences_csv, preferences_reader, classes, class_capacities, studenttograde, emails, schedules

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
    # for example: time, time, CLASS 1 would be index 2
    initial_index = 2

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
    
    flag = True

    preferences_csv.seek(0)
    preferences_reader = csv.reader(preferences_csv)
    for student in preferences_reader:
        student_index += 1
        # create edge between source and students
        source_start_nodes += [0]
        source_end_nodes += [num_classes + student_index]
        source_costs += [0]
        senior_flag = (studenttograde[student[1]] == 12)
        missing_flag = (studenttograde[student[1]] == 0)

        temp = list(classes)
        replace = []
        for pref in range(5):
            try:
                temp.remove(student[2 + pref + period * 5])
            except ValueError:
                replace += [pref]
                
        if len(replace) > 0:
            for a in replace:
                randomval = random.randint(0, len(temp) - 1)
                student[2 + a + period * 5] = temp[randomval]

        if period == 2 and int(studenttograde[student[1]]) < 11:
            for pref in range(5):
                student[2 + pref + 2 * 5] = "First Lunch"
        elif period == 3 and int(studenttograde[student[1]]) > 10:
            for pref in range(5):
                student[2 + pref + 3 * 5] = "Second Lunch"

        for j in range(5):
            # find ID of class that student wants
            # insert at preference
            # period = 1: 1 2 3 4 5
            # period = 2: 6 7 8 9 10
            class_id = classes.index(student[j + classes_per_period * period + initial_index])
            # connect student nodes to classes
            student_start_nodes += [num_classes + student_index]
            student_end_nodes += [class_id + 1]
            # j is cost, weighted by weight. heavier means more influence
            weight = 10000 - student_index
            if senior_flag:
                weight *= 10
            elif missing_flag:
                weight = int(weight/10)
            student_costs += [weight * j]

        if flag and period == 2:
            continue

        
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
    status = smcf.solve()

    if status == smcf.OPTIMAL:
        print("Total cost = ", smcf.optimal_cost())
        print()
        for arc in range(smcf.num_arcs()):
            if smcf.flow(arc) > 0 and smcf.tail(arc) != source and smcf.head(arc) != sink:
                print(
                    "Student %s assigned to class %s.  Cost = %d, Flow = %d"
                    % (emails[smcf.tail(arc) - num_classes - 1], classes[smcf.head(arc) - 1], smcf.unit_cost(arc), smcf.flow(arc))
                )
                schedules[period][smcf.tail(arc) - num_classes - 1] = smcf.head(arc) - 1
                master_list[smcf.head(arc) - 1][period] += [emails[smcf.tail(arc) - num_classes - 1]]

                print(master_list[0][period])

    else:
        print("There was an issue with the min cost flow input.")
        print(f"Status: {status}")

def output():

    global emails, num_period, schedules, classes, master_list

    location = output_directory.get()

    for i in range(len(emails)):

        name = emails[i][:str(emails[i]).find("@gmail.com")]

        fin = []
        for j in range(num_period):
            fin += [str(classes[schedules[j][i]])]
        print(emails[i], fin)

        try:
            os.mkdir(location + "\\Students")
        except FileExistsError:
            pass
        except PermissionError:
            status.log("Could not create output folders")
            return

        status.log("Creating schedule for student " + name)

        f = open(f"{location}\\Students\\{name}Schedule.csv","w")
        f.write(",".join(fin))
        f.close()

    status.log("Schedules complete")
    
    # master_list: it works like, master_list[class][period]
    for i in range(len(classes)):
        for j in range(4):
            print(classes[i], "Period " + str(j), master_list[i][j])
            if len(master_list[i][j]) == 0:
                continue

            try:
                os.mkdir(location + "\\SeminarAttendances")
            except FileExistsError:
                pass
            except PermissionError:
                status.log("Could not create output folders")
                return
            
            status.log(f"Creating attendance for class {classes[i]} period {j+1}")
 
            f = open(f"{location}\\SeminarAttendances\\{classes[i]}Period{j+1}.csv", "w")
            f.write("\n".join(master_list[i][j]))
            f.close()

    status.log("Master Lists complete")

if __name__ == "__main__":

    tkwindowthread()

    # emerson hirsch, daniel spilman, karn chutinan, serena baranello, selin gulden, amethyst xue, iris chen, 