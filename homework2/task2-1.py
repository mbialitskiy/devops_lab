#!/bin/python


def check_for_numbers(income_string):
    while any(c.isalpha() for c in income_string):
        income_string = raw_input("Please, enter only digits:")
    return income_string


n = raw_input("Please, enter number of students:")
n = check_for_numbers(n)
while int(n) not in range(1, 11):
        n = int(raw_input("Amount of students must be in 2..10 range. Please, repeat input:"))
students = {}
for i in range(int(n)):
    input_string = (raw_input("Please enter students data:").split())
    marks = check_for_numbers(''.join(input_string[1:]))
    marks = map(float, marks.split())
    while max(marks) not in range(101):
        marks = map(int, raw_input("Marks must be lower than 100. Repeat only marks for {0}:".format(input_string[0])).split())
    students.update({input_string[0]: marks})
student_to_average = raw_input("What student average marks you want to get?")
while student_to_average not in students:
    student_to_average = raw_input("No such student. Please repeat:")
average = sum(students[student_to_average])/len(students[student_to_average])
print "Average for {student} is {aver}".format(student=student_to_average, aver=round(average, 2))




