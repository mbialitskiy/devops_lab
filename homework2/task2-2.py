#!/bin/python


def create_dict(input_keys, input_values):
    dictionary = {}
    for i in range(len(input_keys)):
        if i < len(input_values):
            dictionary.update({input_keys[i]: input_values[i]})
        else:
            dictionary.update({input_keys[i]: None})
    return dictionary


print create_dict(['key1', 'key2', 'key3', 'key4', 'key5'], [1, 2, 3, 4, 5, 6, 7])



