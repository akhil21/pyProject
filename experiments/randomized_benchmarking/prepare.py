import numpy as np
import itertools
import hashlib
from ...objects.registry import Registry, Job

def get_hash(matrix):
    matrix = np.ascontiguousarray(matrix.round(5)+10)
    code   = hashlib.md5(matrix).hexdigest()
    return code

def prepare_dicts(group):
    for i in range(len(group.element)):
        group.element[i] *= np.linalg.det(group.element[i])**(-1/2**group.num_qubit)

    code_dict = {}
    for i in range(len(group.element)):
        code = get_hash(group.element[i])
        code_dict[code] = i

    inv_dict = {}
    for i in range(len(group.element)):
        for j in [1,1j,-1,-1j]:
            code = get_hash(j*group.element[i].T.conj())
            if code in code_dict.keys():
                inv_dict[i] = code_dict[code]
    return code_dict, inv_dict

def get_sequences(group, length, random, seed, code_dict, inv_dict):
    sources   = np.random.randint(0,len(group.element),[random,length-1]).tolist()
    sequences = []
    for source in sources:
        last_idx = get_last_idx(group, source, code_dict, inv_dict)
        sequences.append(source+[last_idx])
    return np.array(sequences)

def get_last_idx(group, source, code_dict, inv_dict):
    gate = np.identity(2**group.num_qubit)
    for i in source:
        gate = group.element[i]@gate
    for j in np.exp(0.5j*np.pi*np.arange(2**group.num_qubit)):
        code = get_hash(j*gate)
        if code in code_dict.keys():
            idx     = code_dict[code]
            last_idx = inv_dict[idx]
            return last_idx

def get_registry(group, sequence, seed=0):
    code_dict, inv_dict = prepare_dicts(group)

    registry    = Registry()
    for (length, random, shot) in sequence:
        sequences = get_sequences(group, length, random, seed, code_dict, inv_dict)
        for idx, sequence in enumerate(sequences):
            key         = str(length) + "_" + str(idx)
            condition   = {
                "expriment_type"    : "randomized benchmarking",
                "group"             : group.name,
                "number_of_qubit"   : group.num_qubit,
                "sequence_length"   : length,
                "sequence_idx"      : idx,
                "sequence_shot"     : shot,
                "sequence"          : sequence,
            }
            job  = Job(key,condition)
            registry.submit(job)
    return registry