"""Linear assignment example."""
from ortools.graph.python import min_cost_flow
import csv
import tkinter as tk
from tkinter import filedialog

preferences_reader = 0

studenttograde = {}

emails = []
p1 = []
p2 = []
p3 = []
p4 = []

classes_reader = 0

classes = []
class_capacities = [[]]*4

def csv_processing():

    root = tk.Tk()
    root.withdraw()

    global preferences_reader, studenttograde, classes_reader, classes, class_capacities

    input("Press any button to select the file with the student preferences for each seminar")

    preferences_csv = filedialog.askopenfilename()
    preferences_reader = csv.reader(preferences_csv)

    studenttograde_csv = "TO BE HARDCODED"
    studenttograde_reader = csv.reader(studenttograde_csv)

    input("Press any button to select the file with all the avaliable seminars and their capacities.")

    classes_csv = filedialog.askopenfilename()
    classes_reader = csv.reader(classes_csv)

    for aclass in classes_reader:
        classes += aclass[0]
        for x, capacity in enumerate(aclass[1:]):
            class_capacities[x] += capacity

    for student in studenttograde_reader:
        studenttograde[student[0]] = student[1]

    

    input("Press any button to select the file with the rooms that classes will be in.")

    roomclass_csv = filedialog.askopenfilename() # might be hardcoded or already provided
    roomclass_reader = csv.reader(preferences_csv)

def main(period):

    global preferences_reader, classes, class_capacities, studenttograde, emails, p1, p2, p3, p4

    """Solving an Assignment Problem with MinCostFlow."""
    # Instantiate a SimpleMinCostFlow solver.
    smcf = min_cost_flow.SimpleMinCostFlow()

    num_classes = len(classes)

    period = 0

    source_start_nodes = []
    source_end_nodes = []
    source_costs = []

    student_start_nodes = []
    student_end_nodes = []
    student_costs = []

    #initialize all class
    class_start_nodes = [x+1 for x in range(num_classes)] * 2

    # tldr loop through this shit twice because of the two costs thingy

    class_costs += [-10000000000] * num_classes
    class_costs = [0] * num_classes
    
    # priority to fill minimum
    

    student_index = 0

    classes_per_period = 5

    #index in the csv where periods start
    # for example: time, time, CLASS 1 would be index 2
    initial_index = 2

    min_per_class = 1

    
    # the malicious
    class_capacities += [min_per_class] * num_classes
    # subtract off MIN VAL to make sure all capacities are as intended
    for i in range(num_classes):
        if class_capacities[i] >= min_per_class:
            class_capacities[i] -= min_per_class
        else:
            # set corresp. to 0
            class_capacities[i + num_classes] = class_capacities[i]
            class_capacities[i] = 0
    
    

    for student in preferences_reader:
        student_index += 1
        # create edge between source and students
        source_start_nodes += [0]
        source_end_nodes += [num_classes + student_index]
        source_costs += [0]
        senior_flag = (studenttograde[student[1].split("@")[0]] == 12)
        emails += [student[1]]

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
        source_capacities + student_capacities + class_capacities
    )
    costs = (
        source_costs + student_costs + class_costs
    )
            

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

    final_data = []

    if status == smcf.OPTIMAL:
        print("Total cost = ", smcf.optimal_cost())
        print()
        for arc in range(smcf.num_arcs()):
            if smcf.flow(arc) > 0 and smcf.tail(arc) != source and smcf.head(arc) != sink:
                print(
                    "Student %s assigned to class %s.  Cost = %d, Flow = %d"
                    % (emails[smcf.tail(arc) - num_classes - 1], classes[smcf.head(arc) - 1], smcf.unit_cost(arc), smcf.flow(arc))
                )
    else:
        print("There was an issue with the min cost flow input.")
        print(f"Status: {status}")


if __name__ == "__main__":

    csv_processing()

    for period in range(1):
        main(period)