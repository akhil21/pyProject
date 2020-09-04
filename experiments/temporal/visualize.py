import numpy as np
import matplotlib.pyplot as plt
from .analyze import rb_decay

def show_report(report):
    length  = report["sequence_length"]
    mean    = report["mean_value"]
    std     = report["standard_deviation"]
    a       = report["slope"]
    b       = report["offset"]
    p       = report["deporalizing_parameter"]
    fidelity = report["fidelity"]

    print("fidelity is {0}".format(fidelity))

    plt.figure(figsize=(5,5))
    plt.errorbar(x=length,y=mean,yerr=std,fmt='k.')
    xfit = np.linspace(0,length[-1],1001)
    yfit = rb_decay(xfit,a,b,p)
    plt.plot(xfit,yfit,'r-')
    plt.xlabel('Sequence length')
    plt.ylabel("Population")
    plt.ylim(-0.1,1.1)
    plt.legend()
    plt.show()