from animal_list import AnimalList
from animal import Animal
import numpy as np
import math


class Genetic:
    def __init__(self):
        self.animal_list_parents = None  # class AnimalList
        self.animal_list_kids = None
        self.generation_counter = 0
        self.setup = None
        self.best_to_copy: float = 0.002
        self.best_to_repl: float = 0.004
        self.random_tail: float = 0.05
        self.history: dict[int, AnimalList] = {}

    def load_setup(self, setup):
        self.setup = setup
        self.animal_list_parents: AnimalList = self.setup.get_animal_list()

    def configure_params(self, best_to_copy=None, best_to_repl=None, random_tail=None):
        self.best_to_copy: float = best_to_copy or self.best_to_copy
        self.best_to_repl: float = best_to_repl or self.best_to_repl
        self.random_tail: float = random_tail or self.random_tail

    def mutate_features(self, animal: Animal, sigma=0.05, mutation_probability=0.02):
        """Performs mutation on provided Animal object (animal, [sigma, probability])"""
        x1_start, x1_end, x2_start, x2_end = self.setup.get_ranges()
        if np.random.uniform() < mutation_probability:
            x1m = np.random.normal(animal.get_features("x1"), (x1_end-x1_start)*sigma)
            animal.set_features(x1=x1m)
        if np.random.uniform() < mutation_probability:
            x2m = np.random.normal(animal.get_features("x2"), (x2_end-x2_start)*sigma)
            animal.set_features(x2=x2m)
        self.animal_fix(animal)

    def generate_random_animal(self) -> Animal:
        new_animal = Animal()
        new_animal.set_sfo(self.setup.get_adaptation_object())
        x1s, x1e, x2s, x2e = self.setup.get_ranges()
        new_animal.set_features(x1=np.random.uniform(x1s, x1e))
        new_animal.set_features(x2=np.random.uniform(x2s, x2e))
        return new_animal

    def generate_kid(self, mummy: Animal, daddy: Animal) -> Animal:
        kid = mummy.clone()
        kid.set_features(x1=self.mix_features(mummy.get_features("x1"), daddy.get_features("x1")))
        kid.set_features(x2=self.mix_features(mummy.get_features("x2"), daddy.get_features("x2")))
        self.animal_fix(kid)
        return kid

    def mix_features(self, f1: float, f2: float) -> float:
        average = (f1+f2)/2.0
        delta = abs((f1-f2)/2.0)
        modifier = np.random.uniform(-3.0*delta, 3.0*delta)
        return average + modifier

    def animal_fix(self, animal: Animal):
        """Make sure that provided Animal object's features are confined to ranges"""
        x1_start, x1_end, x2_start, x2_end = self.setup.get_ranges()
        animal_x1, animal_x2 = animal.get_features()
        if animal_x1 < x1_start:
            animal.set_features(x1=x1_start)
        if animal_x1 > x1_end:
            animal.set_features(x1=x1_end)
        if animal_x2 < x2_start:
            animal.set_features(x2=x2_start)
        if animal_x2 > x2_end:
            animal.set_features(x2=x2_end)

    def execute(self, epochs: int):
        """
        Performs genetic algorithm execution with hardcoded iteration count

        Returns a dictionary [ generation_number: int, list: AnimalList ]
        """
        self.history[0] = self.animal_list_parents
        for self.generation_counter in range(epochs):
            self.animal_list_kids: AnimalList = self.make_next_generation(self.animal_list_parents)
            self.animal_list_kids.sort_by_adaptation()
            best_adaptation = self.animal_list_kids.get_animal(0).get_adaptation()
            num_of_animals = self.animal_list_kids.get_animal_count()
            feature_1, feature_2 = self.animal_list_kids.get_animal(0).get_features()
            print(f"Best adaptation : {best_adaptation:.15f}, "
                  f"Winner features ({feature_1:.15f}, {feature_2:.15f}), "
                  f"Total number of animals : {num_of_animals}")
            self.animal_list_parents = self.animal_list_kids
            self.history[self.generation_counter+1] = self.animal_list_kids

    def make_next_generation(self, parents: AnimalList) -> AnimalList:
        """
        Takes whole generation AnimalList object and returns generation+1 object
        This is essential genetic algorithm code
        """
        parents.sort_by_adaptation()
        num_of_animals = parents.get_animal_count()
        raw_btc: int = math.floor(self.best_to_copy * num_of_animals) + 1
        raw_btr: int = math.floor(self.best_to_repl * num_of_animals) + 1
        raw_t: int = math.floor(self.random_tail * num_of_animals) + 1
        kids = AnimalList()
        for counter in range(raw_btc):
            kids.add_animal(parents.get_animal(counter))
        for counter in range(num_of_animals-raw_btc-raw_t):
            index_1, index_2 = self.make_pair(raw_btc+raw_btr)
            kid = self.generate_kid(parents.get_animal(index_1), parents.get_animal(index_2))
            self.mutate_features(kid)
            kids.add_animal(kid)
        for counter in range(raw_t):
            kids.add_animal(self.generate_random_animal())
        return kids

    def make_pair(self, selected_count: int):
        """
        Takes selected population headcount
        returns a pair of indexes (different)
        """
        index_1, index_2 = np.random.choice(selected_count, 2, replace=False)
        return index_1, index_2

    def get_history(self):
        return self.history
