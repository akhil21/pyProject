import numpy as np
import itertools
from .numpy_extension import I,X,Y,Z,tensor
from .pauli_extension import check_commute

ROUND_ERROR = 1e-10

class PauliTransferMatrix:
    def __init__(self,gate=None,ptm_dict=None):
        if (gate is not None) and (ptm_dict is not None):
            raise("input must be only [gate] or [ptm_dict]")

        if (gate is None) and (ptm_dict is None):
            raise("input must not be None")

        if gate is not None:
            self.gate  = gate
            self.n     = int(np.log2(gate.shape[0]))
            self.ptm   = None

        if ptm_dict is not None:
            self.n = len(list(ptm_dict.keys())[0][0])
            self.ptm = ptm_dict

        self.pauli = [tensor(list(i)) for i in itertools.product([I,X,Y,Z],repeat=self.n)]
        self.label = [''.join(i) for i in itertools.product(['I','X','Y','Z'],repeat=self.n)]

    def calculate(self):
        self.ptm = {}
        for prep_label, prep_pauli in zip(self.label,self.pauli):
            for meas_label, meas_pauli in zip(self.label,self.pauli):
                value = np.trace(meas_pauli@self.gate@prep_pauli@self.gate.T.conj()).real/2**self.n
                # if value != 0:
                if abs(value) > ROUND_ERROR:
                    self.ptm[(prep_label,meas_label)] = value

    def extract_element(self,prep,meas):
        return self.ptm.get((prep,meas))

    def get_complemented_ptm(self):
        out = {}
        for prep_label in self.label:
            for meas_label in self.label:
                out[(prep_label,meas_label)] = self.ptm.get((prep_label,meas_label))
        return out

    def get_matrix(self):
        matrix = np.zeros([4**self.n,4**self.n])
        for i, pi in enumerate(self.label):
            for j, pj in enumerate(self.label):
                matrix[i,j] = self.ptm.get((pi,pj))
        return matrix

class StabilizerPauliTransferMatrix(PauliTransferMatrix):
    def __init__(self, gate=None, ptm_dict=None, stabilizer_prep=[], stabilizer_meas=[]):
        super().__init__(gate=gate, ptm_dict=ptm_dict)
        self.stabilizer_prep = stabilizer_prep
        self.stabilizer_meas = stabilizer_meas

    def calculate(self):
        self.ptm = {}
        for prep_label, prep_pauli in zip(self.label,self.pauli):
            for meas_label, meas_pauli in zip(self.label,self.pauli):
                if False not in [check_commute(prep_label,st_prep) for st_prep in self.stabilizer_prep]:
                    if False not in [check_commute(meas_label,st_meas) for st_meas in self.stabilizer_meas]:
                        value = np.trace(meas_pauli@self.gate@prep_pauli@self.gate.T.conj()).real/2**self.n
                        # if value != 0:
                        if abs(value) > ROUND_ERROR:
                            self.ptm[(prep_label,meas_label)] = value