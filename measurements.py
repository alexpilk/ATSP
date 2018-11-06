from atsp import Atsp, Map
from atsp.branch_and_bound import SolutionExplorer, Solution
import logging
import time


# logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


def find_first_solution(city_map, timeout):
    return SolutionExplorer(city_map).find_first_solution(timeout=timeout)


def find_best_solutions(city_map, timeout):
    return SolutionExplorer(city_map).find_best_solutions(timeout=timeout)


class Measurement(object):

    def __init__(self, size, repetitions=100, timeout=30):
        self.size = size
        self.repetitions = repetitions
        self.timeout = timeout

    def measure_first_solution(self):
        return self._measure(find_first_solution)

    def measure_best_solutions(self):
        return self._measure(find_best_solutions)

    def _measure(self, action):
        values = []
        timeouts = 0
        for _ in range(self.repetitions):
            city_map = Map.from_random_matrix(size=self.size)
            start = time.time()
            try:
                action(city_map, self.timeout)
            except TimeoutError:
                timeouts += 1
            time_taken = time.time() - start
            values.append(time_taken)
            logger.debug(time_taken)
        return sum(values) / len(values), timeouts


logger.info('Size,First average,First timeouts,Best average,Best timeouts')
for i in range(5, 40, 5):
    measurement = Measurement(i)
    first_average, first_timeouts = measurement.measure_first_solution()
    best_average, best_timeouts = measurement.measure_best_solutions()
    logger.info('{size},{f},{f_timeouts},{b},{b_timeouts}'.format(
        size=i, f=first_average, f_timeouts=first_timeouts, b=best_average, b_timeouts=best_timeouts))
