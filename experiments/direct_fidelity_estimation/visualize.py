from ...util.pauli_transfer_matrix import PauliTransferMatrix
from ...util.plot_extension import show_ptm

def show_report(report):
    print("Subspace averaged gate fidelity : {0}".format(report["fidelity"]))
    print("Pauli transfer matrix : Target")
    ptm_target = PauliTransferMatrix(None,report["ptm_target"])
    show_ptm(ptm_target)
    print("Pauli transfer matrix : Ansatz")
    ptm_ansatz = PauliTransferMatrix(None,report["ptm_ansatz"])
    show_ptm(ptm_ansatz)


