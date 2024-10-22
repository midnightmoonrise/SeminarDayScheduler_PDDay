"""Linear assignment example."""
from ortools.graph.python import min_cost_flow
import csv
import tkinter as tk
from tkinter import filedialog
import threading

window = Tk()

def tkwindowthread():

    global window

    width = window.winfo_screenwidth() / 8
    height = window.winfo_screenheight() / 2
    
    window.rowconfigure([x for x in range(6)], weight=1, minsize=height/8)
    window.columnconfigure([x for x in range(2)], weight=1, minsize=width/2)

    frame = tk.Frame(
        master=window,
        relief=tk.RAISED,
        borderwidth=1
    )
    frame.grid(row=i, column=j)
    label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
    label.pack()

    

    #wip
    print("wip")

    window.mainloop()

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

def csv_processing():

    root = tk.Tk()
    root.attributes('-topmost',True)
    root.withdraw()

    global num_period, preferences_csv, preferences_reader, studenttograde, classes_reader, classes, class_capacities, emails, master_list, schedules

    input("Press any button to select the file with the student preferences for each seminar")
    
    preferences_csv = open(filedialog.askopenfilename())
    #preferences_reader = csv.reader(preferences_csv)
    
    preferences_reader = csv.reader(preferences_csv)
    root.destroy()

    input("Press any button to select the file with student grade info.")
    studenttograde_csv = open(filedialog.askopenfilename())
    studenttograde_reader = csv.reader(studenttograde_csv)

    for student in studenttograde_reader:
        #print(student)
        #print(student[0],student[1])
        studenttograde[student[0]] = student[1]
        emails += [student[0]]

    schedules = []
    for i in range(num_period):
        schedules += [[0] * len(emails)]

    input("Press any button to select the file with all the avaliable seminars and their capacities.")

    classes_csv = open(filedialog.askopenfilename())
    classes_reader = csv.reader(classes_csv)

    for aclass in classes_reader:
        classes += [aclass[0]]
        for x, capacity in enumerate(aclass[1:]):
            class_capacities[x] += [int(capacity)]
    master_list = []
    for i in range(len(classes)):
        ohio = []
        for j in range(num_period):
            ohio += [ [] ]
        master_list += [ohio]

    

    

    #input("Press any button to select the file with the rooms that classes will be in.")

    #roomclass_csv = filedialog.askopenfilename() # might be hardcoded or already provided
    #roomclass_reader = csv.reader(preferences_csv)

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
    
    
    preferences_csv.seek(0)
    preferences_reader = csv.reader(preferences_csv)
    for student in preferences_reader:
        student_index += 1
        # create edge between source and students
        source_start_nodes += [0]
        source_end_nodes += [num_classes + student_index]
        source_costs += [0]
        senior_flag = (studenttograde[student[1]] == 12)

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


if __name__ == "__main__":

    tkwindowthread()

    csv_processing()

    for period in range(num_period):
        main(period)
        print("Yup")

    location = filedialog.askdirectory()

    for i in range(len(emails)):
        fin = []
        for j in range(num_period):
            fin += [str(schedules[j][i])]
        print(emails[i], fin)

        f = open(location + "Student" + str(i) + ".csv","x")
        f.write(",".join(fin))
        f.close()
    
    # master_list: it works like, master_list[class][period]
    for i in range(len(classes)):
        for j in range(4):
            print(classes[i], "Period " + str(j), master_list[i][j])