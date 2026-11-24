import matplotlib.pyplot as plt
import numpy as np
from phantominator import ct_shepp_logan


# [intensity, x-radius, y-radius, center_x, center_y, angle_degrees]
SHEPP_LOGAN_PARAMS = np.array([
    [ 1.0, 0.69,   0.92,  0.00,  0.0000,   0],
    [-0.8, 0.6624, 0.874, 0.00, -0.0184,   0],
    [-0.2, 0.11,   0.31,  0.22,  0.0000, -np.pi*0.1],
    [-0.2, 0.16,   0.41, -0.22,  0.0000,  np.pi*0.1],
    [ 0.1, 0.21,   0.25,  0.00,  0.3500,   0],
    [ 0.1, 0.046,  0.046, 0.00,  0.1000,   0],
    [ 0.1, 0.046,  0.046, 0.00, -0.1000,   0],
    [ 0.1, 0.046,  0.023,-0.08, -0.6050,   0],
    [ 0.1, 0.023,  0.023, 0.00, -0.6060,   0],
    [ 0.1, 0.023,  0.046, 0.06, -0.6050,   0],
], dtype=float)

phantom = ct_shepp_logan(N=512, E=SHEPP_LOGAN_PARAMS)

plt.imshow(phantom, cmap="Grays", origin='lower')
plt.axis("off")
plt.show()


