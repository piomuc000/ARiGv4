import numpy as np
import matplotlib.pyplot
import surface_functions


def plot_surface(x_start: float, x_end: float, y_start: float, y_end: float, function_name: str) -> None:
    functions = surface_functions.SurfaceFunctions()

    functions.select_function(function_name)

    x_values = np.linspace(x_start, x_end, 100)
    y_values = np.linspace(y_start, y_end, 100)
    x_mesh, y_mesh = np.meshgrid(x_values, y_values)
    z_mesh = functions.evaluate(x_mesh, y_mesh)

    matplotlib.pyplot.figure()
    ax = matplotlib.pyplot.axes(projection='3d')
    ax.plot_surface(x_mesh, y_mesh, z_mesh, cmap='viridis')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    matplotlib.pyplot.savefig('plot3d.png')
