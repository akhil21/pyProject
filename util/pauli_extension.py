import re

def check_simul(pauli0, pauli1):
    flag = True
    for i,j in zip(pauli0, pauli1):
        if (i!="I") and (j!="I") and (i!=j):
            flag = False
    return flag

def check_commute(pauli0, pauli1):
    count = 0
    for i,j in zip(pauli0, pauli1):
        if (i!="I") and (j!="I") and (i!=j):
            count += 1
    return not count%2

def find_identity(pauli):
    return [i.start() for i in re.finditer("I",pauli)]

def integrate_histogram(histogram,remove_idx):
    expected_value = 0
    for key, val in histogram.items():
        coeff = count_one(key,remove_idx)
        expected_value += coeff*val
    return expected_value

def count_one(key,remove_idx):
    count = 0
    for idx, string in enumerate(key):
        if idx not in remove_idx:
            if string is "1":
                count += 1
    if count%2:
        coeff = -1
    else:
        coeff = 1
    return coeff