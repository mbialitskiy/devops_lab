#!/bin/python


def check_input(h, w):

    while not ((w % h == 0) and (int(w / h) == 3)):
        h, w = map(int, raw_input("First digit must be 3 times smaller then second. Enter size:").split())
    return h, w


n, m = map(int, raw_input("Enter size:").split())
n, m = check_input(n, m)

for i in range(1, n, 2):
    print "-" * ((m - 3 * i) / 2) + ".|." * i + "-" * ((m - 3 * i) / 2)
print "-" * ((m - 7) / 2) + "WELCOME" + "-" * ((m - 7) / 2)
for i in range(n-2, -1, -2):
    print "-" * ((m - 3 * i) / 2) + ".|." * i + "-" * ((m - 3 * i) / 2)
