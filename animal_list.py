from animal import Animal


class AnimalList:
    def __init__(self):
        self.animals = []

    def add_animal(self, animal):
        if not isinstance(animal, Animal):
            raise TypeError("Only Animal objects can be added to the list")
        self.animals.append(animal)

    def remove_animal(self, animal):
        self.animals.remove(animal)

    def sort_by_adaptation(self):
        self.animals.sort(key=lambda animal: animal.get_adaptation(), reverse=True)

    def get_animal(self, index: int):
        return self.animals[index]

    def get_animal_count(self):
        return len(self.animals)
