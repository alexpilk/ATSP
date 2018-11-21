import fire
from python_console_menu import AbstractMenu, MenuItem

from atsp import Map, Atsp


class MainMenu(AbstractMenu):
    def __init__(self, city_map):
        self.map = city_map
        self.atsp = Atsp(self.map)
        super().__init__("Welcome to ATSP CLI")

    def initialise(self):
        self.add_menu_item(MenuItem(100, "Exit menu").set_as_exit_option())
        self.add_menu_item(MenuItem(101, "Display map", lambda: print(self.map.original_matrix)))
        self.add_menu_item(MenuItem(102, "Solve using B&B", self.create_handler(self.atsp.branch_and_bound)))
        self.add_menu_item(MenuItem(103, "Find first solution using B&B",
                                    self.create_handler(self.atsp.first_branch_and_bound_solution)))
        self.add_menu_item(MenuItem(104, "Solve using brute force", self.create_handler(self.atsp.brute_force)))

    @staticmethod
    def create_handler(solve):
        return lambda: print('Found path {} with cost {}'.format(*solve()))


def load(file_path):
    city_map = Map.from_file(file_path)
    menu = MainMenu(city_map)
    menu.display()


if __name__ == '__main__':
    fire.Fire(load)
