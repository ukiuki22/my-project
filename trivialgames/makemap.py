import numpy as np
import matplotlib.pyplot as plt

forest = [255,0,0]
sea    = [255,0,0]

img_rgb = np.array([
                    [[255,0,0],[0,255,0],[0,0,255]],
                    [[255,255,0],[0,255,255],[255,0,255]],
                    [[0,0,0],[127,127,127],[255,255,255]],
], dtype = np.uint8)

#画像の表示
plt.imshow(img_rgb, interpolation = 'none')

plt.show()
