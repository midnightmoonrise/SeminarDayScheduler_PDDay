import csv

emailtoname = []
with open("PD_CSV/teachernames.csv", newline="") as file:
    teachers = csv.reader(file)
    for teacher in teachers:
        emailtoname.append((teacher[0].strip(),teacher[1].strip()))

preferences = []

with open("PD_CSV/preferences_data.csv", newline="") as file:
    reader = csv.reader(file)
    for line in reader:
        preferences.append(line)

def find_preferences(email):
    for preference in preferences:
        if preference[1] == email:
            return preference

scores = []

for email, name in emailtoname:
    with open(f"Output\\teachers/{name} Schedule.txt") as file:


        schedule = file.readlines()

        for x, seminar in enumerate(schedule):
            schedule[x] = seminar[schedule[x].index(":") + 2:].strip()
        
        preference = find_preferences(email)



        if (schedule[0] == schedule[1] or schedule[1] == schedule[2] or schedule[0] == schedule[2]) and schedule.count("Presenting") <= 1:
            print(name, " HAS REPEAT SEMINARS")

        score = 0

        for j in range(3):

            seminars = preference[3+j*6:3+j*6+5]

            for base in range(5):

                if schedule[j] == seminars[base]:
                    score += 5 - base
                    break
                else:
                    score -= base + 1      
        if score < 15:
            print(f"{name} did not get all first choices.")
        if score < 0:
            print(f"{name} got a score of less than 0.")

        scores.append(score)     

print(scores)
sum = 0
for score in scores:
    sum += score
sum /= len(scores)
print(sum)