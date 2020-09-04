import numpy as np
from ...objects.registry import Registry, Job

def get_sequences(group, length, random, seed, interleaved):
    if length == 0:
        sequences = [[]]*random
    else:
        sources   = np.random.randint(0,len(group.element),[random,length-1]).tolist()
        sequences = []
        for source in sources:
            sequence = []
            gate = np.identity(2**group.num_qubit)
            for i in source:
                sequence.append(group.element[i])
                gate = group.element[i]@gate
                if interleaved is not None:
                    gate = interleaved@gate
            sequence.append(gate.T.conj())
            sequences.append(sequence)
    return sequences

def get_registry(group, sequence, seed=0, interleaved=None):

    for i in range(len(group.element)):
        group.element[i] *= np.linalg.det(group.element[i])**(-1/2**group.num_qubit)

    registry    = Registry()
    for (length, random, shot) in sequence:
        sequences = get_sequences(group, length, random, seed, interleaved)
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