import os

import pytest

from atsp import Map, SolutionExplorer


@pytest.fixture()
def city_map(test_set):
    test_set_path = os.path.join(os.path.dirname(__file__), 'test_data', '{}.txt'.format(test_set))
    return Map.from_file(test_set_path)


@pytest.fixture()
def solver(city_map):
    return SolutionExplorer(city_map)


def verify(solver, expected_path, expected_cost):
    assert solver.solve() == (expected_path, expected_cost)


@pytest.mark.parametrize(
    'test_set,expected_path,expected_cost',
    [
        ('tsp_6_1', [0, 1, 2, 3, 4, 5, 0], 132),
        ('tsp_6_2', [0, 5, 1, 2, 3, 4, 0], 80),
        ('tsp_10', [0, 3, 4, 2, 8, 7, 6, 9, 1, 5, 0], 212),
        ('tsp_12', [0, 1, 8, 4, 6, 2, 11, 9, 7, 5, 3, 10, 0], 264),
        ('tsp_13', [0, 10, 3, 5, 7, 9, 11, 2, 6, 4, 8, 1, 12, 0], 269),
        ('tsp_14', [0, 10, 3, 5, 7, 9, 13, 11, 2, 6, 4, 8, 1, 12, 0], 282),
        ('tsp_15', [0, 12, 1, 14, 8, 4, 6, 2, 11, 13, 9, 7, 5, 3, 10, 0], 291),
        ('tsp_17', [0, 11, 13, 2, 9, 10, 1, 12, 15, 14, 5, 6, 3, 4, 7, 8, 16, 0], 39)
    ])
def test_first_solution(expected_path, expected_cost, solver):
    paths, cost = solver.solve()
    assert cost == expected_cost


@pytest.mark.parametrize(
    'test_set,expected_path,expected_cost',
    [
        ('tsp_6_1', [0, 1, 2, 3, 4, 5, 0], 132),
        ('tsp_6_2', [0, 5, 1, 2, 3, 4, 0], 80),
        ('tsp_10', [0, 3, 4, 2, 8, 7, 6, 9, 1, 5, 0], 212),
        ('tsp_12', [0, 1, 8, 4, 6, 2, 11, 9, 7, 5, 3, 10, 0], 264),
        ('tsp_13', [0, 10, 3, 5, 7, 9, 11, 2, 6, 4, 8, 1, 12, 0], 269),
        ('tsp_14', [0, 10, 3, 5, 7, 9, 13, 11, 2, 6, 4, 8, 1, 12, 0], 282),
        ('tsp_15', [0, 12, 1, 14, 8, 4, 6, 2, 11, 13, 9, 7, 5, 3, 10, 0], 291),
        # ('tsp_17', [0, 11, 13, 2, 9, 10, 1, 12, 15, 14, 5, 6, 3, 4, 7, 8, 16, 0], 39)
    ])
def test_all_solutions(expected_path, expected_cost, solver):
    paths, cost = solver.find_all_solutions()
    assert cost == expected_cost
    assert expected_path in paths
