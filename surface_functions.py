import numpy as np


class SurfaceFunctions:
    def __init__(self):
        self.functions = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'upward_paraboloid': lambda x, y: x ** 2 + y ** 2,
            'downward_paraboloid': lambda x, y: -(x ** 2 + y ** 2),
            'egg_holder': lambda x, y: -(y + 47) * np.sin(np.sqrt(abs(x / 2 + (y + 47)))) -
                                        x * np.sin(np.sqrt(abs(x - (y + 47)))),
            'shf_2': lambda x, y: 0.5 + (np.sin(x ** 2 - y ** 2) ** 2 - 0.5) / (1 + 0.001 * (x ** 2 + y ** 2)) ** 2,
            'ras': lambda x, y, a=10: 2 * a + (x ** 2 - a * np.cos(2 * np.pi * x)) +
                                     (y ** 2 - a * np.cos(2 * np.pi * y)),
            'ackley': lambda x, y: -20 * np.exp(-0.2 * np.sqrt(0.5 * (x ** 2 + y ** 2))) -
                                   np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + np.e + 20,
            'him': lambda x, y: (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2,
            'inverted_upward_paraboloid': lambda x, y: -(x ** 2 + y ** 2),
            'inverted_downward_paraboloid': lambda x, y: x ** 2 + y ** 2,
            'inverted_egg_holder': lambda x, y: (y + 47) * np.sin(np.sqrt(abs(x / 2 + (y + 47)))) +
                                                x * np.sin(np.sqrt(abs(x - (y + 47)))),
            'inverted_shf_2': lambda x, y: -1 * (
                        0.5 + (np.sin(x ** 2 - y ** 2) ** 2 - 0.5) / (1 + 0.001 * (x ** 2 + y ** 2)) ** 2),
            'inverted_ras': lambda x, y, a=10: -1 * (2 * a + (x ** 2 - a * np.cos(2 * np.pi * x)) +
                                                     (y ** 2 - a * np.cos(2 * np.pi * y))),
            'inverted_ackley': lambda x, y: -1 * (-20 * np.exp(-0.2 * np.sqrt(0.5 * (x ** 2 + y ** 2))) -
                                                  np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(
                                                      2 * np.pi * y))) + np.e + 20),
            'inverted_him': lambda x, y: -1 * ((x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2)
        }
        self.selected_function = None

    def select_function(self, function_name):
        if function_name in self.functions:
            self.selected_function = self.functions[function_name]
        else:
            raise ValueError(f"Function '{function_name}' does not exist.")

    def evaluate(self, x, y):
        if self.selected_function is None:
            raise ValueError("No function selected.")
        return self.selected_function(x, y)

    def get_formula(self):
        if self.selected_function is None:
            raise ValueError("No function selected.")
        return self.selected_function
