import numpy as np
import itertools
import networkx as nx
from .pauli_extension import check_simul
from .clique_cover import clique_cover

def get_graph(pauli_transfer_matrix):
    nodes = list(pauli_transfer_matrix.ptm.keys())
    edges = []
    for (prep0,meas0), (prep1,meas1) in itertools.combinations(nodes,2):
        if check_simul(prep0,prep1) and check_simul(meas0,meas1):
            edges.append(((prep0,meas0),(prep1,meas1)))
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph

def get_most_complex_pauli_label(paulis):
    n = len(paulis[0])
    pauli_set = {}
    for pauli in paulis:
        for qubit, pauli_qubit in enumerate(pauli):
            if pauli_set.get(qubit) is None:
                if pauli_qubit is not "I":
                    pauli_set[qubit] = pauli_qubit
    pauli_product = ""
    for qubit in range(n):
        if pauli_set.get(qubit) is None:
            pauli_product += "I"
        else:
            pauli_product += pauli_set[qubit]
    return pauli_product

def get_clique_key(nodes):
    prep_labels, meas_labels = np.array(nodes).T
    clique_prep_label = get_most_complex_pauli_label(prep_labels)
    clique_meas_label = get_most_complex_pauli_label(meas_labels)
    clique_label = (clique_prep_label,clique_meas_label)
    return clique_label

def get_clique_dict(pauli_transfer_matrix,strategy):
    graph       = get_graph(pauli_transfer_matrix)
    nodes_list  = clique_cover(graph,strategy)
    clique_dict = {}
    for nodes in nodes_list:
        clique_key = get_clique_key(nodes)
        clique_dict[clique_key] = nodes
    return clique_dict