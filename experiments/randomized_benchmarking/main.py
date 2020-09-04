from .prepare import get_registry
from .analyze import get_report
from .visualize import show_report
from ...objects.dataset import DataSet

class RandomizedBenchmarking:
    def __init__(
        self,
        group,
        sequence,
        seed=0
        ):

        self.registry = get_registry(
            group       = group,
            sequence    = sequence,
            seed        = seed
            )

        self.dataset = DataSet()
        self.report = None
        
        self.number_of_qubit = gourp.number_of_qubit
        self.length = []
        for (l, randmom, shot) in sequence:
            self.length.append(l)

    def execute(self, take_data):
        take_data(self.registry, self.dataset)

    def get_report(self):
        self.report = get_report(
            number_of_qubit = self.number_of_qubit,
            length          = self.length,
            dataset         = self.dataset
            )

    def visualize(self):
        show_report(self.report)

    def reset(self):
        self.dataset.reset()
        self.registry.flag_reset()
        self.report = None

