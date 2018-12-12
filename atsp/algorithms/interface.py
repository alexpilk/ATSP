from .brute_force import BruteForceSolver
from .branch_and_bound import BranchAndBoundSolver
from .simulated_annealing import SimulatedAnnealing


class Atsp(object):

    def __init__(self, city_map):
        self.city_map = city_map

    def brute_force(self):
        return BruteForceSolver(self.city_map).solve()

    def simulated_annealing(self, start_temperature=9000, end_temperature=0.1, cooling_factor=0.999, timeout=30):
        return SimulatedAnnealing(self.city_map, start_temperature, end_temperature, cooling_factor)\
            .solve(timeout=timeout)

    def branch_and_bound(self, timeout=30):
        return BranchAndBoundSolver(self.city_map).solve(timeout=timeout)

    def first_branch_and_bound_solution(self, timeout=30):
        return BranchAndBoundSolver(self.city_map).find_first_solution(timeout=timeout)
