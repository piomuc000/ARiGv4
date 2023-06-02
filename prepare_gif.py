import os
import imageio
import numpy as np
import matplotlib.pyplot as plt


class PrepareGif:
    def __init__(self):
        self.history = {}
        self.num_of_generations = 0
        self.num_of_animals_in_generation_max = 0
        self.np_array = None
        self.setup = None

    def load_history(self, history):
        self.history = history
        self.num_of_generations = len(self.history)
        self.num_of_animals_in_generation_max = 0
        for counter in range(self.num_of_generations):
            self.num_of_animals_in_generation_max = max(
                self.num_of_animals_in_generation_max,
                self.history[counter].get_animal_count()
            )
        self.np_array = np.empty((self.num_of_generations, self.num_of_animals_in_generation_max, 3))
        for counter_generations in range(self.num_of_generations):
            for counter_animals in range(self.num_of_animals_in_generation_max):
                f1, f2 = self.history[counter_generations].get_animal(counter_animals).get_features()
                adap = self.history[counter_generations].get_animal(counter_animals).get_adaptation()
                self.np_array[counter_generations][counter_animals][0] = f1
                self.np_array[counter_generations][counter_animals][1] = f2
                self.np_array[counter_generations][counter_animals][2] = adap

    def load_setup(self, setup):
        self.setup = setup

    def save_image(self, func: str = "unknown-function", algo: str = "unknown-algorithm"):
        filenames_3d = []
        filenames_hm = []
        for img_counter in range(self.num_of_generations):
            fig = plt.figure(figsize=(20, 20))
            ax = fig.add_subplot(projection='3d')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('adaptation value')
            x_start, x_end, y_start, y_end = self.setup.get_ranges()
            x_grid = np.linspace(x_start, x_end, 1000)
            y_grid = np.linspace(y_start, y_end, 1000)
            grid1, grid2 = np.meshgrid(x_grid, y_grid)
            surface_level = np.empty((len(x_grid), len(x_grid)))
            for element in range(len(x_grid)):
                surface_level[element] = \
                    self.setup.get_adaptation_object().evaluate(grid1[element], grid2[element])
            x_vals = self.np_array[img_counter][:, 0]
            y_vals = self.np_array[img_counter][:, 1]
            z_vals = self.np_array[img_counter][:, 2]
            ax.scatter3D(x_vals, y_vals, z_vals, c='r')
            ax.plot_surface(grid1, grid2, surface_level, cmap='viridis', antialiased=False)
            filename_3d = f"plot/ARiG_3d_{func}_{algo}_{img_counter}.png"
            fig.savefig(filename_3d)
            plt.close(fig)
            filenames_3d.append(filename_3d)
            fig2, ax2 = plt.subplots(figsize=(20, 20))
            heatmap = ax2.imshow(surface_level, cmap='viridis', extent=[x_start, x_end, y_start, y_end], origin='lower')
            ax2.scatter(x_vals, y_vals, c='r')
            ax2.set_xlabel('x')
            ax2.set_ylabel('y')
            plt.colorbar(heatmap, ax=ax2)
            filename_hm = f"plot/ARiG_heatmap_{func}_{algo}_{img_counter}.png"
            fig2.savefig(filename_hm)
            plt.close(fig2)
            filenames_hm.append(filename_hm)
        images_3d = []
        images_hm = []
        for filename_3d in filenames_3d:
            images_3d.append(imageio.imread(filename_3d))
        for filename_hm in filenames_hm:
            images_hm.append(imageio.imread(filename_hm))
        gif_3d_filename = f"plot/gif/ARiG_3d_animation_{func}_{algo}.gif"
        gif_hm_filename = f"plot/gif/ARiG_heatmap_animation_{func}_{algo}.gif"
        imageio.mimsave(gif_3d_filename, images_3d, duration=1000)
        imageio.mimsave(gif_hm_filename, images_hm, duration=1000)
        for filename in filenames_3d:
            os.remove(filename)
