import numpy as np
from ...util.pauli_transfer_matrix import PauliTransferMatrix
from ...util.plot_extension import plt, show_ptm

def show_report(report):
    plt.figure(figsize=(5,5))
    plt.plot(report["iteration"],1-np.array(report["score"]),'k.-')
    plt.ylim(0,1)
    plt.ylabel("Fidelity")
    plt.xlabel("# of experiments")
    plt.show()

    print("Pauli transfer matrix : Target")
    ptm_theory  = PauliTransferMatrix(ptm_dict=report["ptm_target"])
    show_ptm(ptm_theory)
    print("Pauli transfer matrix : Initial")
    print("Fidelity {0}".format(1 - report["score"][0]))
    ptm_initial = PauliTransferMatrix(ptm_dict=report["ptm_ansatz"][0])
    show_ptm(ptm_initial)
    # print("Pauli transfer matrix : Final")
    # ptm_final   = PauliTransferMatrix(ptm_dict=report["ptm_ansatz"][-1])
    # show_ptm(ptm_final)
    best_index = np.argmin(report["score"])
    print("Pauli transfer matrix : Best [{0}]".format(best_index))
    print("Fidelity {0}".format(1 - report["score"][best_index]))
    ptm_best   = PauliTransferMatrix(ptm_dict=report["ptm_ansatz"][best_index])
    show_ptm(ptm_best)

