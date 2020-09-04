import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def get_mean(length, dataset):
    result = dict(zip(length,[[]]*len(length)))
    for k, v in dataset["data"].items():
        result[v["sequence_length"]].append(v["histogram"]["0"*dataset["group"].num_qubit])

    mean = []
    std  = []
    for l in length:
        mean.append(result[l].mean())
        std.append(result[l].std())
    return mean, std

def rb_decay(x,a,b,p):
    y = a*p**x + b
    return y

def fit_result(length, mean):
    popt, pcov = curve_fit(rb_decay,length,mean,p0=[mean[0],0.5,0.9])
    return popt, pcov

def get_fidelity(n,p):
    fidelity = (1 + (2**n-1)*p)/2**n
    return fidelity

def get_report(number_of_qubit, length, dataset):
    mean, std   = get_mean(length, dataset)
    popt, pcov  = fit_result(length, mean)
    fidelity    = get_fidelity(number_of_qubit, popt[2])

    report = {
        "sequence_length"           : length,
        "mean_value"                : mean,
        "standard_deviation"        : std,
        "slope"                     : popt[0],
        "offset"                    : popt[1],
        "deporalizing_parameter"    : popt[2],
        "fidelity"                  : fidelity
    }
    return report