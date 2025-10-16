from typing import TYPE_CHECKING

import mixbox
import numpy as np
from matplotlib import pyplot as plt
import colour
from colour.models import RGB_COLOURSPACE_sRGB

if TYPE_CHECKING:
    import numpy.typing as npt

# https://gist.github.com/wolfiex/64d2faa495f8f0e1b1a68cdbdf3817f1#file-bivariate-py
# def cmap_from_bivariate_data(Z1, Z2, cmap1=plt.cm.Blues, cmap2=plt.cm.Reds) -> "npt.NDArray":
#     z1mn = Z1.min()
#     z2mn = Z2.min()
#     z1mx = Z1.max()
#     z2mx = Z2.max()

#     # Rescale values to fit into colormap range (0->255)
#     Z1_plot = np.array((Z1 - z1mn) / (z1mx - z1mn))
#     Z2_plot = np.array((Z2 - z2mn) / (z2mx - z2mn))

#     Z1_color = cmap1((255 * Z1_plot).astype(np.int32))
#     Z2_color = cmap2((255 * Z2_plot).astype(np.int32))

#     Z_color = np.zeros_like(Z1_color)

#     # Color for each point
#     it = np.nditer(np.zeros(Z_color.shape[:-1]), flags=["multi_index"], op_flags=["readwrite"])
#     while not it.finished:
#         # print(it)
#         # max_multiindex_value = max(it.multi_index)
#         # mi = (max(it.multi_index), max(it.multi_index))
#         mi = tuple(max(it.multi_index) for _ in range(len(it.multi_index)))
#         divider = Z1_plot[it.multi_index] + Z2_plot[it.multi_index]
#         loc_diff = Z2_plot[it.multi_index] - Z1_plot[it.multi_index]
#         # print(Z2_plot[it.multi_index], Z1_plot[it.multi_index])
#         position = (loc_diff + 1) / 2  # 0..1
#         first_colour = Z1_color[it.multi_index] * 255
#         second_colour = Z2_color[it.multi_index] * 255
#         middle_colour = mixbox.lerp(Z1_color[mi] * 255, Z2_color[mi] * 255, 0.5)

#         # if loc_diff > 0:
#         #     Z_color[it.multi_index] = mixbox.lerp(middle_colour, second_colour, loc_diff)
#         # elif loc_diff < 0:
#         #     Z_color[it.multi_index] = mixbox.lerp(middle_colour, first_colour, loc_diff * -1)
#         # else:
#         #     Z_color[it.multi_index] = middle_colour

#         # Z_color[it.multi_index] = mixbox.lerp(first_colour, second_colour, 0.5)
#         Z_color[it.multi_index] = mixbox.lerp(first_colour, second_colour, position)

#         it.iternext()

#     return Z_color / 255


def cmap_from_bivariate_data(
    Z1, Z2, cmap1=plt.cm.Blues, cmap2=plt.cm.Reds, corner_colour=None
) -> "npt.NDArray":
    z1mn = Z1.min()
    z2mn = Z2.min()
    z1mx = Z1.max()
    z2mx = Z2.max()

    # Rescale values to fit into colormap range (0->1)
    Z1_plot = np.array((Z1 - z1mn) / (z1mx - z1mn))
    Z2_plot = np.array((Z2 - z2mn) / (z2mx - z2mn))

    Z1_color = cmap1((255 * Z1_plot).astype(np.int32))[..., :3]
    Z2_color = cmap2((255 * Z2_plot).astype(np.int32))[..., :3]

    Z1_color_oklab = colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(Z1_color))
    Z2_color_oklab = colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(Z2_color))

    Z_color = np.zeros_like(Z1_color)

    it = np.nditer(np.zeros(Z_color.shape[:-1]), flags=["multi_index"], op_flags=["readwrite"])
    while not it.finished:
        pos_x, pos_y = Z1_plot[it.multi_index], Z2_plot[it.multi_index]

        loc_diff = pos_x - pos_y
        position = (loc_diff + 1) / 2

        c1 = Z1_color_oklab[it.multi_index]
        c2 = Z2_color_oklab[it.multi_index]

        mixed_colour = _lerp(c1, c2, position)
        mixed_colour_rgb = np.clip(colour.XYZ_to_sRGB(colour.Oklab_to_XYZ(mixed_colour)), 0, 1)

        Z_color[it.multi_index] = mixed_colour_rgb
        it.iternext()

    return Z_color


def corners_cmap_from_bivariate_data(
    Z1,
    Z2,
    c1=[1, 0.5, 0],
    c2=[0, 0.5, 1],
    start_colour=[0.8, 0.8, 0.8],
    end_colour=[0.15, 0.15, 0.15],
) -> "npt.NDArray":
    z1mn = Z1.min()
    z2mn = Z2.min()
    z1mx = Z1.max()
    z2mx = Z2.max()

    # Rescale values to fit into colormap range (0->1)
    Z1_plot = np.array((Z1 - z1mn) / (z1mx - z1mn))
    Z2_plot = np.array((Z2 - z2mn) / (z2mx - z2mn))

    Z_color = np.zeros((*Z1_plot.shape, 3))

    c1_oklab = colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(np.array(c1)))
    c2_oklab = colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(np.array(c2)))
    sc_oklab = colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(np.array(start_colour)))
    ec_oklab = colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(np.array(end_colour)))

    it = np.nditer(np.zeros(Z_color.shape[:-1]), flags=["multi_index"], op_flags=["readwrite"])
    while not it.finished:
        pos_x, pos_y = Z1_plot[it.multi_index], Z2_plot[it.multi_index]

        bottom_colour = _lerp(sc_oklab, c2_oklab, pos_x)
        top_colour = _lerp(c1_oklab, ec_oklab, pos_x)
        middle_colour = _lerp(bottom_colour, top_colour, pos_y)

        mixed_colour_rgb = np.clip(colour.XYZ_to_sRGB(colour.Oklab_to_XYZ(middle_colour)), 0, 1)

        Z_color[it.multi_index] = mixed_colour_rgb
        it.iternext()

    return Z_color


def bilinear_cmap_from_bivariate_data(
    Z1, Z2, c1=[1, 0.5, 0], c2=[0, 0.5, 1], dark_end: bool = True
) -> "npt.NDArray":
    if dark_end:
        return corners_cmap_from_bivariate_data(
            Z1, Z2, c1, c2, start_colour=[1, 1, 1], end_colour=[0.15, 0.15, 0.15]
        )

    return corners_cmap_from_bivariate_data(
        Z1, Z2, c1, c2, start_colour=[0.15, 0.15, 0.15], end_colour=[1, 1, 1]
    )

    z1mn = Z1.min()
    z2mn = Z2.min()
    z1mx = Z1.max()
    z2mx = Z2.max()

    # Rescale values to fit into colormap range (0->1)
    Z1_plot = np.array((Z1 - z1mn) / (z1mx - z1mn))
    Z2_plot = np.array((Z2 - z2mn) / (z2mx - z2mn))

    Z_color = np.zeros((*Z1_plot.shape, 3))

    Z1_color_oklab = Z1_plot[..., None] * colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(np.array(c1)))
    Z2_color_oklab = Z2_plot[..., None] * colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(np.array(c2)))

    if light_mode:
        Z1_color_oklab = (1 - Z1_plot[..., None]) * np.array([1, 0, 0]) + Z1_color_oklab
        Z2_color_oklab = (1 - Z2_plot[..., None]) * np.array([1, 0, 0]) + Z2_color_oklab

    it = np.nditer(np.zeros(Z_color.shape[:-1]), flags=["multi_index"], op_flags=["readwrite"])
    while not it.finished:
        pos_x, pos_y = Z1_plot[it.multi_index], Z2_plot[it.multi_index]

        loc_diff = pos_y - pos_x
        position = (loc_diff + 1) / 2

        c1 = Z1_color_oklab[it.multi_index]
        c2 = Z2_color_oklab[it.multi_index]

        mixed_colour = c1 * (1 - position) + c2 * position
        mixed_colour_rgb = np.clip(colour.XYZ_to_sRGB(colour.Oklab_to_XYZ(mixed_colour)), 0, 1)

        Z_color[it.multi_index] = mixed_colour_rgb
        it.iternext()

    return Z_color


def bilinear_cmap(l=256, c0=[1, 0.5, 0], c1=[0, 0.5, 1]):
    """
    Returns an l by l colormap that interpolates linearly between 4 colors;
    black, c0, c1 and c0+c1.

    Args:
        l: size of the colormap, defaults to 256
        c0: [r,g,b] array-like defining the color at the top left corner, defaults to [1,0.5,0] (orange)
        c1: [r,g,b] array-like defining the color at the bottom right corner, defaults to [0,0.5,1]] (light blue)
    returns:
        a (l,l,3) numpy array of rgb values
    """
    oklab = np.zeros((l, l, 3))
    oklab[:, :, :] = (
        np.linspace(0, 1, l)[:, np.newaxis, np.newaxis]
        * np.array(colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(c0)))[np.newaxis, np.newaxis, :]
    )

    oklab[:, :, :] += (
        np.linspace(0, 1, l)[np.newaxis, :, np.newaxis]
        * np.array(colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(c1)))[np.newaxis, np.newaxis, :]
    )
    rgb = np.clip(colour.XYZ_to_sRGB(colour.Oklab_to_XYZ(oklab)), 0, 1)
    return rgb


# def cmap_from_bivariate_data_old(
#     Z1, Z2, cmap1=plt.cm.Blues, cmap2=plt.cm.Reds, corner_colour=None
# ) -> "npt.NDArray":
#     z1mn = Z1.min()
#     z2mn = Z2.min()
#     z1mx = Z1.max()
#     z2mx = Z2.max()

#     # Rescale values to fit into colormap range (0->1)
#     Z1_plot = np.array((Z1 - z1mn) / (z1mx - z1mn))
#     Z2_plot = np.array((Z2 - z2mn) / (z2mx - z2mn))

#     Z1_color = cmap1((255 * Z1_plot).astype(np.int32))
#     Z2_color = cmap2((255 * Z2_plot).astype(np.int32))

#     Z_color = np.zeros_like(Z1_color)

#     MAX_COLOR_ONE = cmap1.get_over() * 255
#     MAX_COLOR_TWO = cmap2.get_over() * 255
#     END_COLOR = corner_colour or mixbox.lerp(MAX_COLOR_ONE, MAX_COLOR_TWO, 0.5)

#     # Color for each point
#     it = np.nditer(np.zeros(Z_color.shape[:-1]), flags=["multi_index"], op_flags=["readwrite"])
#     while not it.finished:
#         pos_x, pos_y = Z1_plot[it.multi_index], Z2_plot[it.multi_index]
#         # print(pos_x, pos_y)

#         loc_diff = pos_y - pos_x
#         # # print(Z2_plot[it.multi_index], Z1_plot[it.multi_index])
#         position = (loc_diff + 1) / 2  # 0..1

#         # print(pos_x, pos_y, position)

#         BOTTOM_COLOR = Z1_color[it.multi_index] * 255
#         TOP_COLOR = mixbox.lerp(MAX_COLOR_TWO, END_COLOR, pos_x)

#         LEFT_COLOR = Z2_color[it.multi_index] * 255
#         RIGHT_COLOR = mixbox.lerp(MAX_COLOR_ONE, END_COLOR, pos_y)

#         BCL = mixbox.rgb_to_latent(BOTTOM_COLOR)
#         TCL = mixbox.rgb_to_latent(TOP_COLOR)
#         LCL = mixbox.rgb_to_latent(LEFT_COLOR)
#         RCL = mixbox.rgb_to_latent(RIGHT_COLOR)

#         BCR = (1 - pos_y) / 2
#         TCR = pos_y / 2
#         LCR = (1 - pos_x) / 2
#         RCR = pos_x / 2
#         # print(pos_x, pos_y, BCR, TCR, LCR, RCR)
#         # ECL = mixbox.rgb_to_latent(END_COLOR)

#         # BCD = pos_y
#         # LCD = pos_x
#         # ECD = np.sqrt((1 - pos_y) ** 2 + (1 - pos_x) ** 2)

#         # total_dist = BCD + RCD + ECD

#         # BCDR = 1 - BCD
#         # LCDR = 1 - LCD
#         # ECDR = 1 - (ECD / np.sqrt(2))
#         # ECDR = max(1 - ECD, 0)

#         # TR = BCDR + LCDR + ECDR

#         # if pos_y == 0:
#         # print(BCD, LCD, ECD, BCDR, LCDR, ECDR, BCDR / TR, LCDR / TR, ECDR / TR)

#         # z1 = mixbox.rgb_to_latent(rgb1)
#         # z2 = mixbox.rgb_to_latent(rgb2)
#         # z3 = mixbox.rgb_to_latent(rgb3)

#         z_mix = [0] * mixbox.LATENT_SIZE

#         for i in range(len(z_mix)):  # mix together:
#             z_mix[i] = BCR * BCL[i] + LCR * LCL[i] + TCR * TCL[i] + RCR * RCL[i]

#         MIXED_COLOR = mixbox.latent_to_rgb(z_mix)
#         Z_color[it.multi_index] = [*MIXED_COLOR, 255]
#         # print(MIXED_COLOR)

#         # MIXED_COLOR

#         # MIDDLE_VERTICAL_COLOR = mixbox.lerp(
#         #     LEFT_COLOR, mixbox.lerp(BOTTOM_COLOR, TOP_COLOR, pos_y), pos_x
#         # )
#         # MIDDLE_HORIZONTAL_COLOR = mixbox.lerp(
#         #     BOTTOM_COLOR, mixbox.lerp(LEFT_COLOR, RIGHT_COLOR, pos_x), pos_y
#         # )

#         # # MIDDLE_VERTICAL_COLOR = mixbox.lerp(BOTTOM_COLOR, TOP_COLOR, pos_y)
#         # # MIDDLE_HORIZONTAL_COLOR = mixbox.lerp(LEFT_COLOR, RIGHT_COLOR, pos_x)

#         # MIXED_COLOR = mixbox.lerp(MIDDLE_HORIZONTAL_COLOR, MIDDLE_VERTICAL_COLOR, 0.5)

#         # # if pos_y == 0:
#         # #     print(pos_y, pos_x, BOTTOM_COLOR, MIDDLE_VERTICAL_COLOR, MIXED_COLOR)

#         # # BOTTOM_COLOR = mixbox.lerp(ORIGIN_COLOR, MAX_COLOR_ONE, pos_x)
#         # # TOP_COLOR = mixbox.lerp(MAX_COLOR_TWO, END_COLOR, pos_x)
#         # # MIDDLE_COLOR = mixbox.lerp(BOTTOM_COLOR, TOP_COLOR, pos_y)

#         # # LEFT_COLOR = mixbox.lerp(ORIGIN_COLOR, MAX_COLOR_TWO, pos_x)
#         # # RIGHT_COLOR = mixbox.lerp(MAX_COLOR_ONE, END_COLOR, pos_x)
#         # # MIDDLE_COLOR = mixbox.lerp(LEFT_COLOR, RIGHT_COLOR, pos_y)

#         # Z_color[it.multi_index] = MIXED_COLOR

#         # max_multiindex_value = max(it.multi_index)
#         # mi = (max(it.multi_index), max(it.multi_index))
#         # mi = tuple(max(it.multi_index) for _ in range(len(it.multi_index)))
#         # divider = Z1_plot[it.multi_index] + Z2_plot[it.multi_index]
#         loc_diff = Z2_plot[it.multi_index] - Z1_plot[it.multi_index]
#         # # print(Z2_plot[it.multi_index], Z1_plot[it.multi_index])
#         position = (loc_diff + 1) / 2  # 0..1
#         first_colour = Z1_color[it.multi_index]  # * 255
#         second_colour = Z2_color[it.multi_index]  # * 255

#         c0 = colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(first_colour[:3]))
#         c1 = colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(second_colour[:3]))

#         mixed_colour = c0 * (1 - position) + c1 * position
#         # mixed_colour = (c0 + c1) * 0.5
#         # print(c0, c1, mixed_colour_2, mixed_colour)

#         mixed_colour_rgb = np.clip(colour.XYZ_to_sRGB(colour.Oklab_to_XYZ(mixed_colour)), 0, 1)

#         Z_color[it.multi_index] = [*(mixed_colour_rgb * 255), 255]

#         # c0 = ColorCoordinates(first_colour, "srgb1")  # yellow
#         # c1 = ColorCoordinates(second_colour, "srgb1")  # blue

#         # c0.convert("oklab")
#         # c1.convert("oklab")

#         # print(c0)
#         # middle_colour = mixbox.lerp(Z1_color[mi] * 255, Z2_color[mi] * 255, 0.5)

#         # if loc_diff > 0:
#         #     Z_color[it.multi_index] = mixbox.lerp(middle_colour, second_colour, loc_diff)
#         # elif loc_diff < 0:
#         #     Z_color[it.multi_index] = mixbox.lerp(middle_colour, first_colour, loc_diff * -1)
#         # else:
#         #     Z_color[it.multi_index] = middle_colour

#         # Z_color[it.multi_index] = mixbox.lerp(first_colour, second_colour, 0.5)
#         # Z_color[it.multi_index] = mixbox.lerp(first_colour * 255, second_colour * 255, position)

#         it.iternext()

#     return Z_color / 255


def _lerp(c1, c2, t):
    return (1 - t) * c1 + t * c2
