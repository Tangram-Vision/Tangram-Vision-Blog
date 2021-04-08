#!/usr/bin/env python3

import brewer2mpl as b2m
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import FancyArrowPatch, Circle, Arc
from matplotlib.lines import Line2D
from matplotlib.path import Path
from mpl_toolkits.mplot3d.proj3d import proj_transform, proj_transform_clip
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Patch3D


# This Arrow3D implementation taken from this gist:
# https://gist.github.com/WetHat/1d6cd0f7309535311a539b42cccca89c
class Arrow3D(FancyArrowPatch):
    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)


def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    """Add an 3d arrow to an `Axes3D` instance."""

    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)


setattr(Axes3D, "arrow3D", _arrow3D)


class WorldFramePlotter:
    def __init__(self, title, origin_name, xlim, ylim, zlim, text_offset_scale):
        self.text_offset_scale = text_offset_scale
        self.fig = plt.figure(figsize=(12, 9))
        self.ax = self.fig.add_subplot(projection="3d")
        self.colormap = b2m.get_map("Dark2", "qualitative", 8).mpl_colors

        self.ax.set_title(title, fontsize=25)

        self.ax.axis("off")

        # Set up x-axis
        self.ax.set_xlim(xlim)
        self.ax.set_xticks([])
        self.ax.text(
            xlim[1],
            ylim[0],
            zlim[0],
            r"$x_{}$  ".format(origin_name),
            fontsize=22,
        )
        xcolor = self.colormap[1]

        # Add arrowhead to x-axis
        self.ax.arrow3D(
            0,
            0,
            0,
            xlim[1],
            ylim[0],
            zlim[0],
            lw=3,
            mutation_scale=15,
            arrowstyle="-|>",
            color=xcolor,
            clip_on=False,
        )

        # Set up y-axis
        self.ax.set_ylim(ylim)
        self.ax.set_yticks([])
        self.ax.text(
            xlim[0],
            ylim[1],
            zlim[0],
            r"$y_{}$  ".format(origin_name),
            fontsize=22,
        )
        ycolor = self.colormap[0]

        # Add arrowhead to y-axis
        self.ax.arrow3D(
            0,
            0,
            0,
            xlim[0],
            ylim[1],
            zlim[0],
            lw=3,
            mutation_scale=15,
            arrowstyle="-|>",
            color=ycolor,
            clip_on=False,
        )

        # Set up z-axis
        self.ax.set_zlim(zlim)
        self.ax.set_zticks([])
        self.ax.set_yticks([])
        self.ax.text(
            xlim[0],
            ylim[0],
            zlim[1],
            r"$z_{}$  ".format(origin_name),
            fontsize=22,
        )
        zcolor = self.colormap[2]

        # Add arrowhead to y-axis
        self.ax.arrow3D(
            0,
            0,
            0,
            xlim[0],
            ylim[0],
            zlim[1],
            lw=3,
            mutation_scale=15,
            arrowstyle="-|>",
            color=zcolor,
            clip_on=False,
        )

        # Plot origin
        self.ax.plot(0, 0, 0, "ko", clip_on=False)
        self.ax.text(
            -1 * 0.04 * xlim[1],
            -1 * 0.04 * ylim[1],
            -1 * 0.04 * zlim[1],
            r"$O_{}$".format(origin_name),
            fontsize=22,
        )

    def print_offset(self, limits):
        (lower, upper) = limits
        return self.text_offset_scale * (upper - lower)

    def add_labeled_point(self, x, y, z, label):
        self.ax.plot(x, y, z, "ko")
        self.ax.text(
            x + self.print_offset(self.ax.get_xlim()),
            y + self.print_offset(self.ax.get_ylim()),
            z + self.print_offset(self.ax.get_zlim()),
            f"${label}: ({x}, {y}, {z})$",
            fontsize=18,
        )

    def add_grid_lines_for_point(self, x, y):
        self.ax.plot(
            [x, 0, 0], [y, y, y], [z, z, z], "--", lw=1.0, color="black", alpha=0.3
        )
        self.ax.plot(
            [x, x, x], [0, y, 0], [z, z, z], "--", lw=1.0, color="black", alpha=0.3
        )
        self.ax.plot(
            [x, x, x], [y, y, y], [0, 0, z], "--", lw=1.0, color="black", alpha=0.3
        )

    def add_coordinate_frame(
        self, label, rotations, translation, scales, colors, label_origin=True
    ):
        (x, y, z) = translation
        (omega, phi, kappa) = rotations

        w = omega * np.pi / 180
        p = phi * np.pi / 180
        k = kappa * np.pi / 180

        Rx = np.array(
            [
                [1, 0, 0],
                [0, np.cos(w), -np.sin(w)],
                [0, np.sin(w), np.cos(w)],
            ]
        )

        Ry = np.array(
            [
                [np.cos(p), 0, np.sin(p)],
                [0, 1, 0],
                [-np.sin(p), 0, np.cos(p)],
            ]
        )

        Rz = np.array(
            [
                [np.cos(k), -np.sin(k), 0],
                [np.sin(k), np.cos(k), 0],
                [0, 0, 1],
            ]
        )

        R = Rz @ Ry @ Rx

        (sx, sy, sz) = scales
        S = np.array(
            [
                [sx, 0, 0],
                [0, sy, 0],
                [0, 0, sz],
            ]
        )

        SR = S @ R

        self.ax.arrow3D(
            x,
            y,
            z,
            SR[0, 0],
            SR[0, 1],
            SR[0, 2],
            lw=1.5,
            mutation_scale=10,
            arrowstyle="-|>",
            color=colors[0],
        )
        self.ax.arrow3D(
            x,
            y,
            z,
            SR[1, 0],
            SR[1, 1],
            SR[1, 2],
            lw=1.5,
            mutation_scale=10,
            arrowstyle="-|>",
            color=colors[1],
        )
        self.ax.arrow3D(
            x,
            y,
            z,
            SR[2, 0],
            SR[2, 1],
            SR[2, 2],
            lw=1.5,
            mutation_scale=10,
            arrowstyle="-|>",
            color=colors[2],
        )

        self.ax.plot(x, y, z, "ko", clip_on=False)
        if label_origin:
            self.ax.text(
                x - self.print_offset(self.ax.get_xlim()),
                y - self.print_offset(self.ax.get_ylim()),
                z - self.print_offset(self.ax.get_zlim()),
                r"$O_{}$".format(label),
                fontsize=22,
            )

        self.ax.text(
            x + SR[0, 0] + self.print_offset(self.ax.get_xlim()) / 2,
            y + SR[0, 1],
            z + SR[0, 2],
            r"$x_{}$".format(label),
            fontsize=16,
        )
        self.ax.text(
            x + SR[1, 0],
            y + SR[1, 1] + self.print_offset(self.ax.get_ylim()) / 2,
            z + SR[1, 2],
            r"$y_{}$".format(label),
            fontsize=16,
        )

        self.ax.text(
            x + SR[2, 0],
            y + SR[2, 1],
            z + SR[2, 2] + self.print_offset(self.ax.get_zlim()) / 2,
            r"$z_{}$".format(label),
            fontsize=16,
        )

    def show(self):
        self.fig.show()


def transform_as_separate_operations(
    sx, sy, sz, omega, phi, kappa, tx, ty, tz, x_A, y_A, z_A
):
    """
    Transforms a point (x, y) by the translation (tx, ty), rotation (theta) and scale (sx, sy)
    factors, by formulating the transformation according to:

    S = [[sx  0  0]
         [ 0 sy  0]
         [ 0  0 sz]]

    We stick to using the ZYX formulation here. First rotate X, then Y, then Z.

    R = Rz @ Ry @ Rx = [[rxx rxy rxz]
                        [ryx ryy ryz]
                        [rzx rzy rzz]]

    T = [tx ty tz]

    Inputs:

    sx, sy, sz        - Scale factors for the x and y axes, respectively
    omega, phi, kappa - Rotation (counter-clockwise positive) in degrees between the two coordinate
                        frames
    tx, ty, tz        - Translation along x and y axes, respectively
    x_A, y_A, z_A     - Point coordinates to be transformed

    Returns:

    A tuple (x_B, y_B, z_B) representing the transformed point
    """
    w = omega * np.pi / 180
    p = phi * np.pi / 180
    k = kappa * np.pi / 180

    Rx = np.array(
        [
            [1, 0, 0],
            [0, np.cos(w), -np.sin(w)],
            [0, np.sin(w), np.cos(w)],
        ]
    )

    Ry = np.array(
        [
            [np.cos(p), 0, np.sin(p)],
            [0, 1, 0],
            [-np.sin(p), 0, np.cos(p)],
        ]
    )

    Rz = np.array(
        [
            [np.cos(k), -np.sin(k), 0],
            [np.sin(k), np.cos(k), 0],
            [0, 0, 1],
        ]
    )

    rotation = Rz @ Ry @ Rx

    scale = np.array(
        [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, sz],
        ]
    )

    translation = np.array([tx, ty])

    p_A = np.array([x_A, y_A, z_A])

    [x_B, y_B, z_B] = scale @ rotation @ p_A + translation

    return (x_B, y_B, z_B)


def transform_as_gamma_matrix(sx, sy, sz, omega, phi, kappa, tx, ty, tz, x_A, y_A, z_A):
    """
    Transforms a point (x, y) by the translation (tx, ty), rotation (theta) and scale (sx, sy)
    factors, by formulating the transformation according to:

    Gamma = [[sx*rxx  sx*rxy  sx*rxz tx],
             [sy*ryx  sy*ryy  sy*ryz ty],
             [sz*rzx  sz*rzy  sz*rzz ty],
             [     0       0       0  1]]

    We stick to using the ZYX formulation here. First rotate X, then Y, then Z. This is consistent
    with the direct formulation as separate operations.

    Inputs:

    sx, sy, sz        - Scale factors for the x and y axes, respectively
    omega, phi, kappa - Rotation (counter-clockwise positive) in degrees between the two coordinate
                        frames
    tx, ty, tz        - Translation along x and y axes, respectively
    x_A, y_A, z_A     - Point coordinates to be transformed

    Returns:

    A tuple (x_B, y_B, z_B) representing the transformed point
    """
    w = omega * np.pi / 180
    p = phi * np.pi / 180
    k = kappa * np.pi / 180

    Rx = np.array(
        [
            [1, 0, 0],
            [0, np.cos(w), -np.sin(w)],
            [0, np.sin(w), np.cos(w)],
        ]
    )

    Ry = np.array(
        [
            [np.cos(p), 0, np.sin(p)],
            [0, 1, 0],
            [-np.sin(p), 0, np.cos(p)],
        ]
    )

    Rz = np.array(
        [
            [np.cos(k), -np.sin(k), 0],
            [np.sin(k), np.cos(k), 0],
            [0, 0, 1],
        ]
    )

    R = Rz @ Ry @ Rx

    S = np.array(
        [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, sz],
        ]
    )

    Gamma = np.zeros((4, 4))
    Gamma[0:3, 0:3] = S @ R
    Gamma[3, 0:3] = [tx, ty, tz]
    Gamma[3, 3] = 1

    p_A = np.array([x_A, y_A, z_A, 1])

    [x_B, y_B, z_B, _] = Gamma @ p_A
    return (x_B, y_B, z_B)


def world_frame_translation():
    plot = WorldFramePlotter(
        "Translation between coordinate frames A and B",
        "W",
        (0, 100),
        (0, 100),
        (0, 100),
        0.04,
    )

    scales = (25, 25, 25)

    frame1_colors = (plot.colormap[3], plot.colormap[2], plot.colormap[4])
    origin_A = np.array((25, 65, 10))
    plot.add_coordinate_frame("A", (0, 0, 0), origin_A, scales, frame1_colors)

    frame2_colors = (plot.colormap[6], plot.colormap[5], plot.colormap[7])
    origin_B = np.array((73, 32, 40))
    plot.add_coordinate_frame("B", (0, 0, 0), origin_B, scales, frame2_colors)

    coords = np.array([origin_A, origin_B])

    (dx, dy, dz) = origin_B - origin_A

    plot.ax.arrow3D(
        origin_A[0],
        origin_A[1],
        origin_A[2],
        dx,
        dy,
        dz,
        ls=(0, (10, 10)),
        lw=1.5,
        mutation_scale=10,
        arrowstyle="-|>",
        color="black",
        alpha=0.4,
    )

    midpoint = coords.mean(axis=0)
    offset = plot.print_offset(plot.ax.get_ylim())

    plot.ax.text(
        midpoint[0],
        midpoint[1] + offset,
        midpoint[2],
        r"$T^B_A$",
        alpha=0.4,
        fontsize=22,
    )

    plot.show()


def world_frame_rotation_z():
    plot = WorldFramePlotter(
        "Rotation about Z between coordinate frames A and B",
        "W",
        (0, 100),
        (0, 100),
        (0, 100),
        0.04,
    )

    scales = (25, 25, 25)
    rotations1 = (0, 0, 0)
    rotations2 = (0, 0, -33)

    frame1_colors = (plot.colormap[3], plot.colormap[2], plot.colormap[4])
    origin = (50, 50, 50)
    plot.add_coordinate_frame("A", rotations1, origin, scales, frame1_colors, False)

    frame2_colors = (plot.colormap[6], plot.colormap[5], plot.colormap[7])
    plot.add_coordinate_frame("B", rotations2, origin, scales, frame2_colors, False)

    t1 = 0
    t2 = -33 * np.pi / 180
    thetas = np.linspace(t1, t2, 1000)
    vertices = 15 * np.array([np.cos(thetas), -np.sin(thetas)]).T
    zs = np.broadcast_to(50, len(vertices))

    plot.ax.plot(50 + vertices[:, 0], 50 + vertices[:, 1], zs, "--", alpha=0.4)

    plot.ax.text(65, 55, 48, r"$\kappa$", fontsize=18, alpha=0.4)

    print_offset = plot.print_offset(plot.ax.get_xlim())

    plot.show()


def world_frame_rotation_x():
    plot = WorldFramePlotter(
        "Rotation about X between coordinate frames A and B",
        "W",
        (0, 100),
        (0, 100),
        (0, 100),
        0.04,
    )

    scales = (25, 25, 25)
    rotations1 = (0, 0, 0)
    rotations2 = (33, 0, 0)

    frame1_colors = (plot.colormap[3], plot.colormap[2], plot.colormap[4])
    origin = (50, 50, 50)
    plot.add_coordinate_frame("A", rotations1, origin, scales, frame1_colors, False)

    frame2_colors = (plot.colormap[6], plot.colormap[5], plot.colormap[7])
    plot.add_coordinate_frame("B", rotations2, origin, scales, frame2_colors, False)

    t1 = 0
    t2 = -33 * np.pi / 180
    thetas = np.linspace(t1, t2, 1000)
    vertices = 15 * np.array([np.cos(thetas), -np.sin(thetas)]).T
    zs = np.broadcast_to(50, len(vertices))

    plot.ax.plot(zs, 50 + vertices[:, 1], 50 + vertices[:, 0], "--", alpha=0.4)

    plot.ax.text(48, 53, 65, r"$\omega$", fontsize=18, alpha=0.4)

    print_offset = plot.print_offset(plot.ax.get_xlim())

    plot.show()


def world_frame_rotation_y():
    plot = WorldFramePlotter(
        "Rotation about Y between coordinate frames A and B",
        "W",
        (0, 100),
        (0, 100),
        (0, 100),
        0.04,
    )

    scales = (25, 25, 25)
    rotations1 = (0, 0, 0)
    rotations2 = (0, 33, 0)

    frame1_colors = (plot.colormap[3], plot.colormap[2], plot.colormap[4])
    origin = (50, 50, 50)
    plot.add_coordinate_frame("A", rotations1, origin, scales, frame1_colors, False)

    frame2_colors = (plot.colormap[6], plot.colormap[5], plot.colormap[7])
    plot.add_coordinate_frame("B", rotations2, origin, scales, frame2_colors, False)

    t1 = 0
    t2 = -33 * np.pi / 180
    thetas = np.linspace(t1, t2, 1000)
    vertices = 15 * np.array([np.cos(thetas), -np.sin(thetas)]).T
    zs = np.broadcast_to(50, len(vertices))

    plot.ax.plot(50 + vertices[:, 0], zs, 50 + vertices[:, 1], "--", alpha=0.4)

    plot.ax.text(70, 48, 53, r"$\phi$", fontsize=18, alpha=0.4)

    print_offset = plot.print_offset(plot.ax.get_xlim())

    plot.show()


def world_frame_scale():
    plot = WorldFramePlotter(
        "Scale between coordinate frames A and B",
        "W",
        (0, 100),
        (0, 100),
        (0, 100),
        0.04,
    )

    scales1 = (25, 25, 25)
    scales2 = (45, 15, 20)

    rotations = (0, 0, 0)

    frame1_colors = (plot.colormap[3], plot.colormap[2], plot.colormap[4])
    origin1 = np.array((30, 50, 50))
    plot.add_coordinate_frame("A", rotations, origin1, scales1, frame1_colors)

    frame2_colors = (plot.colormap[6], plot.colormap[5], plot.colormap[7])
    origin2 = np.array((70, 50, 50))
    plot.add_coordinate_frame("B", rotations, origin2, scales2, frame2_colors)

    plot.show()


if __name__ == "__main__":
    world_frame_translation()
    world_frame_rotation_z()
    world_frame_rotation_x()
    world_frame_rotation_y()
    world_frame_scale()
