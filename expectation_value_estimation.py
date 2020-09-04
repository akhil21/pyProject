from __init__ import I,X,Y,Z,rx,ry,rz
import numpy        as np
import itertools
import copy
import newest_trb.pulse_sequencer_2 as ps

def tensor(gates):
    out = gates[0]
    for g in gates[1:]:
        out = np.kron(out,g)
    return out

def hamiltonian_operator(coeff):
    """
    Creates c_II*II + c_ZZ*ZZ + c_XX*XX + c_YY*YY + ... pauli sum 
    that will be our Hamiltonian operator.
    
    """
    [c_II,c_IX,c_IY,c_IZ,c_XI,c_XX,c_XY,c_XZ,
              c_YI,c_YX,c_YY,c_YZ,c_ZI,c_ZX,c_ZY,c_ZZ,] = coeff
    pauli_dict =  [
    {"coeff": c_II, "label": {"Q0":"I","Q1":"I"}},
    {"coeff": c_IX, "label": {"Q0":"I","Q1":"X"}},
    {"coeff": c_IY, "label": {"Q0":"I","Q1":"Y"}},
    {"coeff": c_IZ, "label": {"Q0":"I","Q1":"Z"}},
    
    {"coeff": c_XI, "label": {"Q0":"X","Q1":"I"}},
    {"coeff": c_XX, "label": {"Q0":"X","Q1":"X"}},
    {"coeff": c_XY, "label": {"Q0":"X","Q1":"Y"}},
    {"coeff": c_XZ, "label": {"Q0":"X","Q1":"Z"}},
    
    {"coeff": c_YI, "label": {"Q0":"Y","Q1":"I"}},
    {"coeff": c_YX, "label": {"Q0":"Y","Q1":"X"}},
    {"coeff": c_YY, "label": {"Q0":"Y","Q1":"Y"}},
    {"coeff": c_YZ, "label": {"Q0":"Y","Q1":"Z"}},
    
    {"coeff": c_ZI, "label": {"Q0":"Z","Q1":"I"}},
    {"coeff": c_ZX, "label": {"Q0":"Z","Q1":"X"}},
    {"coeff": c_ZY, "label": {"Q0":"Z","Q1":"Y"}},
    {"coeff": c_ZZ, "label": {"Q0":"Z","Q1":"Z"}}
              ]
    
    return pauli_dict

def decompose_hamiltonian(pauli_dict):
    hamiltonian_dict = copy.copy(pauli_dict)

    for idx,term in enumerate(hamiltonian_dict):
        if term['coeff'] == 0:
            hamiltonian_dict.pop(idx)
        else:
            pass

    #n  = int(np.log2(gate.shape[0]))
    #P  = np.array([tensor(list(i)) for i in itertools.product([I,X,Y,Z], repeat=n)])
    
    return (hamiltonian_dict)
def prep_state(pauli,pulse_info):
    
    n = len(pauli)
    
    programs = []
    eigens   = []
    
    for k in list(itertools.product([0,1],repeat=n)):
        q   = ps.Pulse_Gate(pulse_info)
        eig = 1
        for i in range(n):
            if   pauli[i] is 'I':
                if k[i] == 0:
                    q.gate(I,target=i)
                else:
                    q.gate(X,target=i)
            elif pauli[i] is 'X':
                if k[i] == 0:
                    q.gate(ry( 0.5*np.pi),target=i)
                else:
                    q.gate(ry(-0.5*np.pi),target=i)
                    eig *= -1
            elif pauli[i] is 'Y':
                if k[i] == 0:
                    q.gate(rx(-0.5*np.pi),target=i)
                else:
                    q.gate(rx( 0.5*np.pi),target=i)
                    eig *= -1
            elif pauli[i] is 'Z':
                if k[i] == 0:
                    q.gate(I,target=i)
                else:
                    q.gate(X,target=i)
                    eig *= -1
                    
        programs.append(q)
        eigens.append(eig)
        
    return {'program':programs,'eig':eigens,'state':pauli}
def prep_meas(q,pauli):
    n = len(pauli)
    idx = []
    for i in range(len(pauli)):
        if   pauli[i] is 'I':
            q.gate(I,target=i)
            idx.append(i)
        elif pauli[i] is 'X':
            q.gate(ry(-0.5*np.pi),target=i)
        elif pauli[i] is 'Y':
            q.gate(rx( 0.5*np.pi),target=i)
        elif pauli[i] is 'Z':
            q.gate(I,target=i)
        else:
            pass
    return {'program':q,'idx':idx,'meas':pauli}
def calc_pauli(result,idx,n):
    for i in itertools.product(range(2),repeat=n):
        if not np.allclose(np.array(i)[idx],[0]*len(idx)):
            k = np.array(i)
            k[idx] = np.zeros(np.array(k)[idx].shape)
            result[tuple(k)] += result[i]
            result[i] = 0

    result = np.array(result,dtype=np.float)/result.sum()
    pauli_value = 0
    for i in itertools.product(range(2),repeat=n):
            pauli_value += (1 - 2*np.mod(np.sum(i),2))*result[i]
    return pauli_value

def expectation_value_estimation(coeff_list, do_meas, pulse_info, n=2):
    pauli_dict = hamiltonian_operator(coeff_list)
    hamiltonian_dict = decompose_hamiltonian(pauli_dict)
    plabel = [''.join(i) for i in itertools.product(['I','X','Y','Z'], repeat = n)]
    #If we want the initial state just as II, then give II instead of plabel.
    for j,k in enumerate(['II']):
        initial_state = prep_state(pauli=k,pulse_info=pulse_info)
        for idx,term in enumerate(hamiltonian_dict):
            print(initial_state)
            
    #         end_state   = func(initial_state['program'][k])
    #         meas        = prep_meas(end_state,pauli=j)  
    #         result      = do_meas(
    #             pg   = meas['program'],
    #             idcs = ['Q'+''.join(str(i)) for i in range(n)],
    #             name = 'DFE_state_%s_meas_%s_eig_%s'%(i,j,k)
    #             )
    #         pauli_value = calc_pauli(result,meas['idx'],n)
    #         ptmij      += initial_state['eig'][k]*pauli_value
    #     ptm.append(ptmij)
    # ptm = np.array(ptm)/(2**n)
    # print('object ptm %s'%(ptm.round(3)))
    # gate_fidelity = ((ptm*df['ptmij']).sum()/(2**n) + 1)/(2**n+1)
    # print('object agf %s'%(gate_fidelity))
    # return gate_fidelity, ptm