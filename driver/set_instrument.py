from .util import name_to_alpha
import sys
sys.path.append("C:\Scalabrad")
from measurement_tool.units import MHz, GHz, ns, us, dB

def set_qubit(instrument, qubit_notes, qubit_information):
    for qubit_name in qubit_information:
        alpha                                             = name_to_alpha(qubit_name)
        note                                              = qubit_notes[qubit_name]
        instrument.pma.config[qubit_name+"_readout"].freq = note.cavity_readout_window_frequency
        instrument.pma.config[qubit_name+"_qubit"].freq   = note.qubit_dressed_frequency_jazz
        instrument.mwb.config[qubit_name].ratten          = note.cavity_readout_attenuation
        instrument.mwb.config[qubit_name].qatten          = note.pi_pulse_qubit_pump_attenuation
        instrument.mwb.config[qubit_name].rxatten         = 0*dB
        instrument.mwb.config[qubit_name].rgain           = note.cavity_readout_gain
        instrument.mwb.config[qubit_name].qgain           = note.pi_pulse_qubit_pump_gain
        instrument.mwb.config[qubit_name].c1gain          = -30*dB
        instrument.mwb.config[qubit_name].c1atten         = 31*dB
        instrument.mwb.config[qubit_name].c2gain          = -30*dB
        instrument.mwb.config[qubit_name].c2atten         = 31*dB
        instrument.qla.status.shots                       = 1000
        instrument.qla.config[qubit_name].window          = (note.cavity_readout_window_weight_I, note.cavity_readout_window_weight_Q)
        instrument.qla.status.cooltime                    = 50*us
        instrument.qla.set_acquisition_mode(averaging_shots = False, averaging_waveform = True)
        instrument.seq[qubit_name].readout.delay          = note.cavity_readout_trigger_delay + note.cavity_readout_window_delay
        instrument.seq[qubit_name].readout.duration       = note.cavity_readout_window_length

        instrument.seq.set_user_command("HPI{0}".format(alpha), "A{0} DT{1} B{2} D{2} B{2}".format(note.pi_pulse_power, note.half_pi_pulse_drag_coeff, note.half_pi_pulse_length_precise["ns"]))
        instrument.seq.set_user_command("MEAS{0}".format(alpha), "A{0} T B10 M F3000".format(note.cavity_readout_window_power))

        instrument.seq[qubit_name].readout.seq            = "MEAS{0}".format(alpha)
        instrument.seq[qubit_name].qubit.seq              = "T"
        instrument.seq[qubit_name].cr1.seq                = "T"
        instrument.seq[qubit_name].cr2.seq                = "T"

def set_cross(instrument, cross_notes, cross_information):
    num2alpha   = lambda c: chr(c+64)
    for cross_name in cross_information:
        note = cross_notes[str(cross_name)]
        
        if cross_name[2] is "cr1":
            instrument.mwb.config[cross_name[1]].c1gain          = note.gain
            instrument.mwb.config[cross_name[1]].c1atten         = note.atten
        if cross_name[2] is "cr2":
            instrument.mwb.config[cross_name[1]].c2gain          = note.gain
            instrument.mwb.config[cross_name[1]].c2atten         = note.atten
        
        calpha = name_to_alpha(cross_name[0])
        talpha = name_to_alpha(cross_name[1])
        instrument.seq.set_user_command("DCR{0}{1}".format(calpha, talpha), "B{0} A{1} P{2} F{3} B{0}".format(note.crw["ns"], note.cra, note.crp, note.crt["ns"]))
        instrument.seq.set_user_command("DCT{0}{1}".format(calpha, talpha), "B{0} A{1} P{2} F{3} B{0}".format(note.crw["ns"], note.cta, note.ctp, note.crt["ns"]))
        instrument.seq.set_user_command("WCR{0}{1}".format(calpha, talpha), "B{0}       B{1} B{0} Z{2}".format(note.crw["ns"], note.crt["ns"], -note.crz))
        # instrument.seq.set_user_command("WCR{0}{1}".format(calpha, talpha), "B{0}            B{1} B{0}".format(note.crw["ns"], note.crt["ns"]))
        instrument.seq.set_user_command("DICR{0}{1}".format(calpha, talpha), "B{0} A{1} P{2} F{3} B{0}".format(note.crw["ns"], note.cra, note.crp+180, note.crt["ns"]))
        instrument.seq.set_user_command("DICT{0}{1}".format(calpha, talpha), "B{0} A{1} P{2} F{3} B{0}".format(note.crw["ns"], note.cta, note.ctp+180, note.crt["ns"]))
