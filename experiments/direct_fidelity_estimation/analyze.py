import numpy as np
import itertools
from ...util.pauli_extension import find_identity, integrate_histogram

def get_node_ptm(node,results):
    prep, meas = node
    prep_remove_idx = find_identity(prep)
    meas_remove_idx = find_identity(meas)

    prep_histogram = {}
    for prep_key, meas_histogram in results.items():
        expected_value = integrate_histogram(meas_histogram, meas_remove_idx)
        prep_histogram[prep_key] = expected_value

    expected_value = integrate_histogram(prep_histogram, prep_remove_idx)
    return expected_value

def get_fidelity(ptm_target, ptm_ansatz):
    n           = ptm_target.n
    inner_prod  = 0
    for node in ptm_target.ptm.keys():
        inner_prod += ptm_target.ptm[node]*ptm_ansatz[node]
    inner_prod *= 4**n/np.sum(np.abs(list(ptm_target.ptm.values()))**2) # Normalization
    fidelity    = (inner_prod/(2**n)+1)/(1+2**n)
    return fidelity

def generate_table(pauli_transfer_matrix, clique_dict, result):
    n       = pauli_transfer_matrix.n
    index   = ["".join(i) for i in itertools.product(["0","1"],repeat=n)]
    table   = {}
    for clique_key in clique_dict.keys():
        table[clique_key] = {}
        for idx in index:
            table[clique_key][idx] = result[str(clique_key) + "_" + idx]["histogram"]
    return table

def generate_report(pauli_transfer_matrix, clique_dict, table):
    n       = pauli_transfer_matrix.n
    report  = {
        "ptm_target"        : pauli_transfer_matrix.ptm,
        "ptm_ansatz"        : {},
        "ptm_ansatz_std"    : {},
        "fidelity"          : None,
        "fidelity_std"      : None
    }
    for clique_key, nodes in clique_dict.items():
        for node in nodes:
            report["ptm_ansatz"][node] = get_node_ptm(node, table[clique_key])/(2**n)

    report["fidelity"] = get_fidelity(pauli_transfer_matrix, report["ptm_ansatz"])
    return report

def get_report(pauli_transfer_matrix,clique_dict,result):
    table = generate_table(pauli_transfer_matrix, clique_dict, result)
    report = generate_report(pauli_transfer_matrix, clique_dict, table)
    return report