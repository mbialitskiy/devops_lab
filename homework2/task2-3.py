#!/bin/python
import math


def calc_fact(numb):
    if numb == 1:
        return 1
    else:
        return int(numb)*calc_fact(int(numb)-1)


input_file = open("input.txt", "r")
number = input_file.read()
input_file.close()
if number.isdigit():
    output_file = open("output_file", "w")
    output_file.write("Result of build-in function:")
    output_file.write(str(math.factorial(int(number)))+"\n")
    output_file.write("Result of my recursion:")
    output_file.write(str(calc_fact(number)))
    output_file.close()
