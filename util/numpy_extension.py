import math
import numpy as np

dtype = np.complex128

I = np.array([[1, 0], [0, 1]], dtype=dtype)
X = np.array([[0, 1], [1, 0]], dtype=dtype)
Y = np.array([[0, -1j], [1j, 0]], dtype=dtype)
Z = np.array([[1, 0], [0, -1]], dtype=dtype)

def tensor(gate_list):
    out = gate_list[0]
    for gate in gate_list[1:]:
        out = np.kron(out,gate)
    return out