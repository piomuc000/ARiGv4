import numpy as np
from animal_list import AnimalList
from animal import Animal


class FireFly2:
    def __init__(self):
        self.animal_list: AnimalList | None = None
        self.history: dict[int, AnimalList] = {}
        self.setup = None
        self.elite = 2
        self.action_counter = 0

    def load_setup(self, setup):
        self.setup = setup
        self.animal_list = self.setup.get_animal_list()

    def get_history(self):
        return self.history

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

    def execute(self, actions: int):
        history_ctr = 0
        self.copy_to_history(self.animal_list, history_ctr)
        for self.action_counter in range(actions):
            self.animal_list.sort_by_adaptation()
            selected_animal_number = np.random.randint(self.elite, self.animal_list.get_animal_count())
            selected_animal = self.animal_list.get_animal(selected_animal_number)
            self.flight(selected_animal)
            self.animal_fix(selected_animal)
            num_of_changes = self.action_counter + 1
            if num_of_changes % 500 and num_of_changes != actions:
                continue
            history_ctr += 1
            self.animal_list.sort_by_adaptation()
            self.copy_to_history(self.animal_list, history_ctr)
            adaptation = self.animal_list.get_animal(0).get_adaptation()
            x1, x2 = self.animal_list.get_animal(0).get_features()
            print(f"adaptation={adaptation:.15f}, features=({x1:.15f}, {x2:.15f}), steps={num_of_changes}")

    def flight(self, animal: Animal):
        """Firefly mission dispatcher"""
        mission_roulette = np.random.uniform()
        if mission_roulette < 0.98:
            self.flight_light(animal)
        elif mission_roulette < 0.99:
            self.flight_roam(animal)
        else:
            self.flight_random(animal)

    def flight_random(self, animal: Animal):
        x1s, x1e, x2s, x2e = self.setup.get_ranges()
        animal.set_features(x1=np.random.uniform(x1s, x1e))
        animal.set_features(x2=np.random.uniform(x2s, x2e))

    def flight_roam(self, animal: Animal):
        x1s, x1e, x2s, x2e = self.setup.get_ranges()
        x1m = np.random.normal(animal.get_features("x1"), abs(x1e-x1s)*0.01)
        animal.set_features(x1=x1m)
        x2m = np.random.normal(animal.get_features("x2"), abs(x2e-x2s)*0.01)
        animal.set_features(x2=x2m)

    def flight_light(self, animal: Animal):
        elite_idx, target_distance = self.find_near_elite(animal)
        x1m = np.random.normal(self.animal_list.get_animal(elite_idx).get_features("x1"), target_distance*0.03)
        animal.set_features(x1=x1m)
        x2m = np.random.normal(self.animal_list.get_animal(elite_idx).get_features("x2"), target_distance*0.03)
        animal.set_features(x2=x2m)

    def calculate_distance(self, animal1: Animal, animal2: Animal) -> float:
        x = animal1.get_features("x1")-animal2.get_features("x1")
        y = animal1.get_features("x2")-animal2.get_features("x2")
        distance = np.sqrt(x * x + y * y)
        return distance

    def find_near_elite(self, animal: Animal) -> tuple[int, float]:
        distances = []
        for animal_counter in range(self.elite):
            distances.append(self.calculate_distance(animal, self.animal_list.get_animal(animal_counter)))
        nearest_num = distances.index(min(distances))
        return nearest_num, distances[nearest_num]

    def copy_to_history(self, animal_list: AnimalList, counter: int):
        new_list = AnimalList()
        for iterator in range(animal_list.get_animal_count()):
            new_list.add_animal(animal_list.get_animal(iterator).clone())
        self.history[counter] = new_list
