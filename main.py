"""Linear assignment example."""
from ortools.graph.python import min_cost_flow
import csv
import tkinter as tk
from tkinter import filedialog


def main(period):
    """Solving an Assignment Problem with MinCostFlow."""
    # Instantiate a SimpleMinCostFlow solver.
    smcf = min_cost_flow.SimpleMinCostFlow()

    root = tk.Tk()
    root.withdraw()

    input("Press any button to choose a file: ")

    file_path = filedialog.askopenfilename()
    csvfile = open(file_path)
    reader = csv.reader(csvfile)

    # Define the directed graph for the flow.
    students = []
    classes = ["skibidi seminar", "business seminar", "cube seminar", "orange seminar", "cheese seminar"]
    class_capacities = [10, 15, 20, 20, 15]

    num_classes = len(classes)

    period = 0

    source_start_nodes = []
    source_end_nodes = []

    student_start_nodes = []
    student_end_nodes = []

    #initialize all class
    class_start_nodes = [x+1 for x in range(num_classes)] * 2
    # tldr loop through this shit twice

    student_index = 0

    classes_per_period = 5
    initial_index = 2

    min_per_class = 5

    for student in reader:
        student_index += 1
        # create edge between source and students
        source_start_nodes += [0]
        source_end_nodes += [num_classes + student_index]
        for j in range(5):
            # find ID of class that student wants
            # insert at preference
            # period = 1: 1 2 3 4 5
            # period = 2: 6 7 8 9 10
            class_id = classes.index(student[j + classes_per_period * period + initial_index])
            # connect student nodes to classes
            student_start_nodes += [num_classes + student_index]
            student_end_nodes += [class_id + 1]
        
    # 0, number of classes, number of students, THEN the sink
    # 1 + num_classes + student_index
    class_end_nodes = [num_classes + student_index + 1] * len(class_start_nodes) * 2

    source_capacities = [1] * len(source_start_nodes)
    student_capacities = [1] * len(student_start_nodes)

    # the malicious
    class_capacities += [min_per_class] * num_classes


    start_nodes = (
        
    )
    end_nodes = (
        [1, 2, 3, 4] + [5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8] + [9, 9, 9, 9]
    )
    capacities = (
        [1, 1, 1, 1] + [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] + [1, 1, 1, 1]
    )
    costs = (
        [0, 0, 0, 0]
        + [90, 76, 75, 70, 35, 85, 55, 65, 125, 95, 90, 105, 45, 110, 95, 115]
        + [0, 0, 0, 0]
    )


    for student in reader:
        num_students += 1
        start_nodes += [0]
        end_nodes += [student_index]
        for preference in range(5):
            

    source = 0
    sink = 9
    tasks = 4
    supplies = [tasks, 0, 0, 0, 0, 0, 0, 0, 0, -tasks]

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
            # Can ignore arcs leading out of source or into sink.
            if smcf.tail(arc) != source and smcf.head(arc) != sink:

                # Arcs in the solution have a flow value of 1. Their start and end nodes
                # give an assignment of worker to task.
                if smcf.flow(arc) > 0:
                    print(
                        "Worker %d assigned to task %d.  Cost = %d"
                        % (smcf.tail(arc), smcf.head(arc), smcf.unit_cost(arc))
                    )
    else:
        print("There was an issue with the min cost flow input.")
        print(f"Status: {status}")


if __name__ == "__main__":
    for period in range(6):
        main(period)