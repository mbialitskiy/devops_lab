#!/bin/python


def get_set(size):
    while True:
        new_set = set(map(int, raw_input("Enter the set of {0} numbers:".format(str(size))).split()))
        if len(new_set) == size:
            break
    return new_set


n = int(raw_input("Please, type amount of numbers in N set:"))
n_set = get_set(n)

m = int(raw_input("Please, type amount of numbers in M set:"))
m_set = get_set(m)


difference = n_set.intersection(m_set)

for i in difference:
    #print next(iter(difference))
    n_set.discard(i)
    m_set.discard(i)

n_set = n_set.union(m_set)
for i in n_set:
    print i




