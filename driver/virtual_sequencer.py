import numpy as np
from .util import name_to_alpha
from .decompose import matrix_to_VZ, matrix_to_su4

class PulseSequencer:
    def __init__(self, qubit_info, cross_info):
        self.sequence      = {}
        for qubit_name in qubit_info:
            self.sequence[qubit_name] = ""
        for cross_name in cross_info:
            self.sequence[cross_name] = ""
        
        self.trigger_point = 0
        self.qubit_info    = qubit_info
        self.cross_info    = cross_info
        
    def rz(self, phase, qubit_name):
        if qubit_name not in self.qubit_info:
            raise
        self.sequence[qubit_name] += "Z{:f} ".format(phase*180/np.pi)
        
        for cross_name in self.cross_info:
            if qubit_name == cross_name[1]:
                self.sequence[cross_name] += "Z{:f} ".format(phase*180/np.pi)
        
    def rx90(self, qubit_name):
        if qubit_name not in self.qubit_info:
            raise
        alpha = name_to_alpha(qubit_name)
        self.sequence[qubit_name] += "P0 HPI{0} ".format(alpha)
        
    def cr(self, cross_name):
        if cross_name not in self.cross_info:
            raise
        calpha = name_to_alpha(cross_name[0])
        talpha = name_to_alpha(cross_name[1])
        self.sequence[cross_name[0]] += "T{0} WCR{1}{2} ".format(self.trigger_point, calpha, talpha) # qubit (control)
        self.sequence[cross_name[1]] += "T{0} DCT{1}{2} ".format(self.trigger_point, calpha, talpha) # qubit (target)
        self.sequence[cross_name]    += "T{0} DCR{1}{2} ".format(self.trigger_point, calpha, talpha) # cross (control, target)
        self.trigger_point           += 1

    def icr(self, cross_name):
        if cross_name not in self.cross_info:
            raise
        calpha = name_to_alpha(cross_name[0])
        talpha = name_to_alpha(cross_name[1])
        self.sequence[cross_name[0]] += "T{0} WCR{1}{2} ".format(self.trigger_point, calpha, talpha) # qubit (control)
        self.sequence[cross_name[1]] += "T{0} DICT{1}{2} ".format(self.trigger_point, calpha, talpha) # qubit (target)
        self.sequence[cross_name]    += "T{0} DICR{1}{2} ".format(self.trigger_point, calpha, talpha) # cross (control, target)
        self.trigger_point           += 1

class VirtualSequencer(PulseSequencer):
    def __init__(self, qubit_info, cross_info):
        super().__init__(qubit_info, cross_info)
        
    def gate(self, matrix, qubit_name):
        phases = matrix_to_VZ(matrix)
        self.rz(phases[2], qubit_name)
        self.rx90(qubit_name)
        self.rz(phases[1], qubit_name)
        self.rx90(qubit_name)
        self.rz(phases[0], qubit_name)
        
    def zxr90(self, cross_name):
        self.cr(cross_name)
        self.rx90(cross_name[0])
        self.rx90(cross_name[0])
        self.icr(cross_name)
        self.rx90(cross_name[0])
        self.rx90(cross_name[0])

    def cnot(self, cross_name):
        self.rz(-0.5*np.pi, cross_name[0])
        self.zxr90(cross_name)
        self.rz(np.pi, cross_name[1])
        self.rx90(cross_name[1])
        self.rz(np.pi, cross_name[1])

    def gate2(self, matrix, cross_name):
        gates = matrix_to_su4(matrix)
        self.gate(gates[0][0], cross_name[0])
        self.gate(gates[0][1], cross_name[1])
        self.cnot(cross_name)
        self.gate(gates[1][0], cross_name[0])
        self.gate(gates[1][1], cross_name[1])
        self.cnot(cross_name)
        self.gate(gates[2][0], cross_name[0])
        self.gate(gates[2][1], cross_name[1])
        self.cnot(cross_name)
        self.gate(gates[3][0], cross_name[0])
        self.gate(gates[3][1], cross_name[1])
