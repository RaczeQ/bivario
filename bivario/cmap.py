from typing import TYPE_CHECKING

import mixbox
import numpy as np
from matplotlib import pyplot as plt

if TYPE_CHECKING:
    import numpy.typing as npt


# https://gist.github.com/wolfiex/64d2faa495f8f0e1b1a68cdbdf3817f1#file-bivariate-py
def cmap_from_bivariate_data(Z1, Z2, cmap1=plt.cm.Blues, cmap2=plt.cm.Reds) -> "npt.NDArray":
    z1mn = Z1.min()
    z2mn = Z2.min()
    z1mx = Z1.max()
    z2mx = Z2.max()

    # Rescale values to fit into colormap range (0->255)
    Z1_plot = np.array((Z1 - z1mn) / (z1mx - z1mn))
    Z2_plot = np.array((Z2 - z2mn) / (z2mx - z2mn))

    Z1_color = cmap1((255 * Z1_plot).astype(np.int32))
    Z2_color = cmap2((255 * Z2_plot).astype(np.int32))

    Z_color = np.zeros_like(Z1_color)

    # Color for each point
    it = np.nditer(np.zeros(Z_color.shape[:-1]), flags=["multi_index"], op_flags=["readwrite"])
    while not it.finished:
        divider = Z1_plot[it.multi_index] + Z2_plot[it.multi_index]
        loc_diff = Z2_plot[it.multi_index] - Z1_plot[it.multi_index]
        position = (loc_diff + 1) / 2  # 0..1
        Z_color[it.multi_index] = mixbox.lerp(
            Z1_color[it.multi_index] * 255,
            Z2_color[it.multi_index] * 255,
            # 0.5
            position,
            # Z2_plot[it.multi_index] / divider if divider > 0 else 0.5,
        )
        # print(
        #     it.multi_index,
        #     Z1_plot[it.multi_index],
        #     Z2_plot[it.multi_index],
        #     divider,
        #     loc_diff,
        #     position,
        #     Z2_plot[it.multi_index] / divider if divider > 0 else 0.5,
        #     Z1_color[it.multi_index] * 255,
        #     Z2_color[it.multi_index] * 255,
        #     Z_color[it.multi_index]
        # )
        it.iternext()

    return Z_color / 255
