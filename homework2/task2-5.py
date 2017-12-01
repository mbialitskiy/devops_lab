#!/bin/python


def get_path():
    good = 0
    while True:
        if good == 1:
            break
        path = raw_input("Path can contain only 'R''L''D''U' letters.Enter the robot pass:")
        for char in path:
             if "RLDU".find(char) == -1:
                break
        else:
            good = 1
    return path


position = [0, 0]
path = get_path()

for c in path:
    if c == "U":
        position[0] += 1
    if c == "D":
        position[0] -= 1
    if c == "L":
        position[1] -= 1
    if c == "R":
        position[1] += 1

if position[0] == 0 and position[1] == 0:
    print "Robot is back"
else:
    print "Robot is gone"

