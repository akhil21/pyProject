from .visualize import show_report
from ..direct_fidelity_estimation import DirectFidelityEstimation
from ...objects.dataset import DataSet
from ...objects.stepper import Stepper
from ...optimizer import optimizer

class VariationalQuantumGateOptimization:
    def __init__(
        self,
        direct_fidelity_estimation,
        n_param,
        iteration,
        p_seed                  = 0,
        initp                   = None,
        optimizer_strategy      = "sequential_minimal_optimization",
        generate_take_data      = None,
        ):

        self.dfe                = direct_fidelity_estimation
        self.generate_take_data = generate_take_data

        def sub_execute(phi):
            take_data = self.generate_take_data(phi)

            self.dfe.reset()
            self.dfe.execute(take_data)
            self.dfe.get_report()
            report                  = {}
            report["number_of_job"] = len(self.dfe.registry.queue.keys())
            report["score"]         = 1 - self.dfe.report["fidelity"]
            report["register"]      = self.dfe.report["ptm_ansatz"]
            return report

        self.stepper = Stepper(
            execute = sub_execute,
            n_param = n_param
        )

        self.optimize       = optimizer[optimizer_strategy]
        self.p_seed         = p_seed
        self.iteration      = iteration
        self.initp          = initp

    def execute(self):
        self.optimize(
            model       = self.stepper,
            p_seed      = self.p_seed,
            iteration   = self.iteration,
            initp       = self.initp
            )
        self.generate_report()

    def generate_report(self):
        self.report = {
            "score"         : self.stepper.score,
            "phi"           : self.stepper.phi,
            "iteration"     : self.stepper.iteration,
            "ptm_ansatz"    : self.stepper.register,
            "ptm_target"    : self.dfe.ptm_target.ptm
        }

    def show_report(self):
        show_report(self.report)