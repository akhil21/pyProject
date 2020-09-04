import numpy as np
import itertools
from ...util.clique_cover_extension import get_clique_dict
from ...objects.registry import Registry, Job

def get_shot(pauli_transfer_matrix,nodes,average_shot_number):
    shot = None
    return shot

def get_registry(pauli_transfer_matrix, clique_dict, average_shot_number):
    n           = pauli_transfer_matrix.n
    index       = ["".join(i) for i in itertools.product(["0","1"],repeat=n)]

    registry = Registry()
    for clique_key, clique_nodes in clique_dict.items():
        shot = get_shot(pauli_transfer_matrix, clique_nodes, average_shot_number)
        for idx in index:
            key         = str(clique_key) + "_" + idx
            condition   = {
                "expriment_type"    : "direct fidelity estimation",
                "number_of_qubit"   : n,
                "clique_key"        : clique_key,
                "preparation_index" : idx,
                "shot_number"       : shot
            }
            job  = Job(key,condition)
            registry.submit(job)
    return registry