import path
import numpy as np

image = '../res/paths.png'
col = np.array([62, 255, 0])
# col = col / 255
p = path.path(image, col)
p.show_image()
# p.save_image()
