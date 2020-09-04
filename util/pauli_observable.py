import numpy as np
import itertools
from .numpy_extension import I,X,Y,Z,tensor

class PauliObservable:
    def __init__(self,observable=None,obs_dict=None):
        if (observable is not None) and (obs_dict is not None):
            raise("input must be only [observable] or [obs_dict]")

        if (observable is None) and (obs_dict is None):
            raise("input must not be None")

        if observable is not None:
            self.observable     = observable
            self.n              = int(np.log2(observable.shape[0]))
            self.obs            = None

        if obs_dict is not None:
            self.n = len(list(obs_dict.keys())[0][0])
            self.obs = obs_dict

        self.pauli = [tensor(list(i)) for i in itertools.product([I,X,Y,Z],repeat=self.n)]
        self.label = [''.join(i) for i in itertools.product(['I','X','Y','Z'],repeat=self.n)]

    def calculate(self):
        self.obs = {}
        for label, pauli in zip(self.label,self.pauli):
            value = np.trace(pauli@self.observable).real/2**self.n
            if value != 0:
                self.obs[label] = value

    def extract_element(self,label):
        return self.obs.get(label)

    def get_complemented_ptm(self):
        out = {}
        for label in self.label:
            out[label] = self.obs.get(label)
        return out