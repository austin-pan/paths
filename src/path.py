import matplotlib.pyplot as plt
import numpy as np

# File to handle "path" objects
class path:
    def __init__(self, file_path, color):
        self.raw_img = plt.imread(file_path)
        self.img = self.raw_img
        image_paths = self.extract_paths(color)
        # image_vertices = self.place_vertices(image_paths)
        # adj_mat = self.to_adj_mat(image_paths)

    def extract_paths(self, color):
        print("extracting ", color)
        [r1, g1, b1] = color # Original value
        r2, g2, b2 = 1, 1, 1 # Value that we want to replace it with
        rel = 5

        red, green, blue = self.raw_img[:, :, 0], self.raw_img[:, :, 1], self.raw_img[:, :, 2]
        mask = (abs(red - r1) <= rel) & (green == g1) & (blue == b1)
        self.img[:, :, :3][~mask] = [r2, g2, b2]

        print("white pixels left: ", np.sum(self.img[:, :, :3] == [1, 1, 1]))

    def place_vertices(self, image_paths):
        pass

    def save_image(self):
        # plt.imshow(self.img)
        # plt.savefig('paths_edited.pdf')
        plt.imsave('paths_edited.png', self.img)

    def show_image(self):
        plt.imshow(self.img)
        plt.show()

    def to_adj_mat(self, image_paths):
        pass
