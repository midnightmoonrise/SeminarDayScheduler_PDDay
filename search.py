import os
import csv

dir = 'C:\\Users\\ethan\\Desktop\\Projects\\Other\\SeminarDayScheduler\\output\\Students'
target_person = 'person89'

def get_student_schedule(student_name):
    path = os.path.join(dir, student_name + 'Schedule.csv')
    output = ''

    with open(path, newline='') as csv_f:
        csv_reader = csv.reader(csv_f, delimiter=' ', quotechar='|')
        for row in csv_reader:
            output+=' '.join(row)
        
    return output

print(f"{target_person}'s Schedule: {get_student_schedule(target_person)}")
