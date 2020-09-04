from .prepare import get_registry
from .analyze import get_report
from .visualize import show_report
from ...util.pauli_transfer_matrix import StabilizerPauliTransferMatrix
from ...util.clique_cover_extension import get_clique_dict
from ...objects.dataset import DataSet

class DirectFidelityEstimation:
    def __init__(
        self,
        gate_notation,
        stabilizer_prep,
        stabilizer_meas,
        clique_cover_strategy,
        average_shot_number,
        ):

        self.ptm_target = StabilizerPauliTransferMatrix(
            gate            = gate_notation,
            ptm_dict        = None,
            stabilizer_prep = stabilizer_prep,
            stabilizer_meas = stabilizer_meas
            )
        self.ptm_target.calculate()

        self.clique_dict = get_clique_dict(
            pauli_transfer_matrix   = self.ptm_target,
            strategy                = clique_cover_strategy
            )

        self.registry = get_registry(
            pauli_transfer_matrix   = self.ptm_target,
            clique_dict             = self.clique_dict,
            average_shot_number     = average_shot_number
            )

        self.dataset = DataSet()

        self.report = None

    def execute(self, take_data):
        take_data(self.registry, self.dataset)

    def get_report(self):
        self.report = get_report(
            pauli_transfer_matrix   = self.ptm_target,
            clique_dict             = self.clique_dict,
            result                  = self.dataset.data
            )

    def visualize(self):
        show_report(self.report)

    def reset(self):
        self.dataset.reset()
        self.registry.flag_reset()
        self.report = None

