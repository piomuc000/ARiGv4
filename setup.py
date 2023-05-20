from surface_functions import SurfaceFunctions
from animal_list import AnimalList
from animal import Animal
import numpy as np


class Setup:
    def __init__(self):
        self.x_start = 0.0
        self.x_end = 0.0
        self.y_start = 0.0
        self.y_end = 0.0
        self.ranges_set = False
        self.sfo = None
        self.animal_list = None

    def set_adaptation(self, adaptation: str):
        sfo = SurfaceFunctions()
        sfo.select_function(adaptation)
        self.sfo = sfo
        return sfo

    def get_adaptation_object(self):
        return self.sfo or ValueError(f"Surface function not configured")

    def set_ranges(self, x_start: float, x_end: float, y_start: float = None, y_end: float = None):
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start or x_start
        self.y_end = y_end or x_end
        self.ranges_set = True

    def get_ranges(self):
        if self.ranges_set:
            return self.x_start, self.x_end, self.y_start, self.y_end
        else:
            raise ValueError(f"Ranges not configured")

    def create_animal_list(self, count: int):
        if self.ranges_set and self.sfo is not None:
            self.animal_list = AnimalList()
            for animal_number in range(count):
                animal_tmp = Animal()
                animal_tmp.set_sfo(self.sfo)
                animal_tmp.set_features(x1=np.random.uniform(self.x_start, self.x_end),
                                        x2=np.random.uniform(self.y_start, self.y_end))
                self.animal_list.add_animal(animal_tmp)
            return self.animal_list
        else:
            raise ValueError(f"Setup object not configured yet to create animal list")

    def get_animal_list(self):
        return self.animal_list or ValueError(f"Animal list not initialized")
