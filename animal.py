class Animal:

    def __init__(self):
        self.x1 = None
        self.x2 = None
        self.sfo = None

    def set_sfo(self, sfo):
        self.sfo = sfo

    def set_features(self, **features) -> None:
        value: float
        for key, value in features.items():
            if key == "x1":
                self.x1 = value
            elif key == "x2":
                self.x2 = value
            else:
                raise ValueError(f"Unknown feature: {key}")

    def clone(self):
        new_animal = Animal()
        new_animal.x1 = self.x1
        new_animal.x2 = self.x2
        new_animal.sfo = self.sfo
        return new_animal

    def get_features(self, key: str = None):
        if key is not None:
            if key == "x1":
                return self.x1
            if key == "x2":
                return self.x2
        else:
            return self.x1, self.x2

    def get_adaptation(self):
        if self.sfo is not None:
            return self.sfo.evaluate(self.x1, self.x2)
        else:
            raise ValueError(f"Surface function not initialized for Animal object")
