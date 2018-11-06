import logging
import time
from copy import deepcopy
from math import inf

from .map import SplitPointNotFound

logger = logging.getLogger(__name__)


class ExpansionError(Exception):
    pass


class IncompletePathError(Exception):
    pass


class BacktrackError(Exception):
    pass


class Solution(object):

    def __init__(self, city_map, parent=None):
        self.map = city_map
        self.parent = parent
        self.left = None
        self.right = None
        self.completed = False
        self.max_depth = len(self.map.cities)
        self.depth = self.parent.depth + 1 if self.parent else 0

    @property
    def is_leaf(self):
        r = set(tuple(set(row)) for row in self.map._matrix)
        return r == {(inf,)}

    def mark_as_completed(self):
        self.completed = True

    @property
    def lower_bound(self):
        return self.map.lower_bound

    @property
    def expanded(self):
        return self.left and self.right

    def expand(self):
        point = self.map.find_split_point()
        left_map, right_map = deepcopy(self.map), deepcopy(self.map)
        left_map.choose_edge(*point)
        right_map.discard_edge(*point)
        self.left = Solution(left_map, parent=self)
        self.right = Solution(right_map, parent=self)

    def __repr__(self):
        return 'Lower bound: {}, chosen edges {}, completed edges {}, map:\n{}'.format(
            self.lower_bound, self.map.chosen_edges, self.map.discarded_edges, self.map
        )


class SolutionExplorer(object):

    def __init__(self, city_map):
        self.map = city_map
        logger.info('Start map:\n{}'.format(city_map))
        self.start_solution = Solution(self.map)
        self.current_solution = self.start_solution
        self.best_path = []
        self.best_cost = inf

    def find_best_solutions(self, timeout=30):
        return self._solve(exit_on_first_solution=False, timeout=timeout)

    def find_first_solution(self, timeout=30):
        return self._solve(exit_on_first_solution=True, timeout=timeout)

    def _solve(self, exit_on_first_solution, timeout):
        start = time.time()
        solution_found = self.check_current_solution()
        while True:
            if time.time() - start > timeout:
                raise TimeoutError
            if solution_found and exit_on_first_solution:
                break
            try:
                self.find_next_solution_for_expansion()
            except BacktrackError:
                break
            solution_found = self.check_current_solution()
        return self.best_path, self.best_cost

    def check_current_solution(self):
        try:
            self.expand_current_solution()
            self.save_current_solution()
            return True
        except (ExpansionError, IncompletePathError):
            return False

    def expand_current_solution(self):
        while not self.current_solution.is_leaf:
            if self.current_solution.lower_bound <= self.best_cost:
                try:
                    self.current_solution.expand()
                except SplitPointNotFound:
                    self.current_solution.mark_as_completed()
                    raise ExpansionError('Split point not found')
                left_bound, right_bound = self.current_solution.left.lower_bound, self.current_solution.right.lower_bound
                self.current_solution = self.current_solution.left if left_bound <= right_bound else self.current_solution.right
                logger.info('Expanded to {}'.format(self.current_solution))
            else:
                self.current_solution.mark_as_completed()
                raise ExpansionError('Lower bound exceeds best cost')
        self.current_solution.mark_as_completed()

    def save_current_solution(self):
        logger.info('Saving current solution')
        new_best_path = self.current_solution.map.build_total_path()
        new_best_cost = self.current_solution.map.total_path_cost
        if len(new_best_path) < self.map.size + 1:
            raise IncompletePathError('Incomplete path {} for edges {}'.format(new_best_path, self.current_solution.map.chosen_edges))
        if not self.best_cost or self.best_cost != new_best_cost:
            self.best_path = [new_best_path]
            self.best_cost = new_best_cost
        else:
            self.best_path.append(new_best_path)

    def find_next_solution_for_expansion(self):
        self.backtrack()
        self.backtrack()
        self.backtrack()
        while self.current_solution.completed or \
                self.best_cost < self.current_solution.right.lower_bound or \
                self.current_solution.right.completed:
            self.backtrack()
        self.current_solution.mark_as_completed()
        self.current_solution = self.current_solution.right
        logger.info('New expansion node {}'.format(self.current_solution))

    def backtrack(self):
        if self.current_solution.parent:
            self.current_solution = self.current_solution.parent
            logger.info('Backtracked to {}\n{}'.format(self.current_solution.lower_bound, self.current_solution.map))
        else:
            raise BacktrackError('Reached the top of the tree')
