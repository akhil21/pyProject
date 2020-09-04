from .util import name_to_alpha

def do_prep(pauli, init, alpha):
    if pauli in ["I","Z"]:
        if init is "0":
            return ""
        else:
            return "P0 HPI{0} P0 HPI{0}".format(alpha)
    elif pauli is "X":
        if init is "0":
            return "P90 HPI{0}".format(alpha)
        else:
            return "P270 HPI{0}".format(alpha)
    elif pauli is "Y":
        if init is "0":
            return "P180 HPI{0}".format(alpha)
        else:
            return "P0 HPI{0}".format(alpha)

def do_meas(pauli, alpha):
    if pauli in ["I","Z"]:
        return ""
    elif pauli is "X":
        return "P270 HPI{0}".format(alpha)
    elif pauli is "Y":
        return "P0 HPI{0}".format(alpha)

def do_experiment(instrument, vz, registry):
    
    spam_conditions = []
    for job in registry.queue.values():
        spam_conditions.append(list(job.clique_key) + [job.preparation_index])
    
    sweep_id = 0
    sweep_axis = []
    for idx, qubit_name in enumerate(vz.qubit_info):
        alpha = name_to_alpha(qubit_name)
        instrument.seq[qubit_name].readout.seq     = "MEAS{0}".format(alpha)
        instrument.seq[qubit_name].qubit.seq       = "C{0}C T{1} ".format(sweep_id, vz.trigger_point) + vz.sequence[qubit_name] + "T{0} C{1}C T".format(vz.trigger_point+1, sweep_id+1)
        instrument.seq[qubit_name].cr1.seq         = "T"
        instrument.seq[qubit_name].cr2.seq         = "T"
        
        prep_gate = []
        meas_gate = []
        for spam in spam_conditions:
            prep_gate.append(do_prep(spam[0][idx], spam[2][idx], alpha))
            meas_gate.append(do_meas(spam[1][idx], alpha))

        instrument.seq.config_variable_command("C{0}C".format(sweep_id), prep_gate, "State preparation")
        instrument.seq.config_variable_command("C{0}C".format(sweep_id+1), meas_gate, "Measurement axis")
        sweep_id += 2
        sweep_axis.append(0)
        sweep_axis.append(0)

    for cross_name in vz.cross_info:
        if cross_name[2] is "cr1":
            instrument.seq[cross_name[1]].cr1.seq     = "T{0} ".format(vz.trigger_point) + vz.sequence[cross_name] + "T{0} T".format(vz.trigger_point+1)
        if cross_name[2] is "cr2":
            instrument.seq[cross_name[1]].cr2.seq     = "T{0} ".format(vz.trigger_point) + vz.sequence[cross_name] + "T{0} T".format(vz.trigger_point+1)

    instrument.qla.status.shots                       = 1000

    dataset_name = "Direct fidelity estimation"
    dataset = instrument.take_data(dataset_name,save=True,sweep_axis=sweep_axis)

    return dataset