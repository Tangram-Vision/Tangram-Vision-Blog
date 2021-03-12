#!/usr/bin/env python3

import brewer2mpl as b2m
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

class WorldFramePlotter:
    def __init__(self, title, origin_name, xlim, ylim, text_offset_scale):
        self.text_offset_scale = text_offset_scale
        self.fig = plt.figure(figsize=(12, 9))
        self.ax = self.fig.add_subplot()
        self.colormap = b2m.get_map("Dark2", "qualitative", 8).mpl_colors

        self.ax.set_title(title, fontsize=25)

        # Hide top and right border lines
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)

        # Set up x-axis
        self.ax.set_xlim(xlim)
        self.ax.set_xticks([])
        self.ax.set_xlabel(r"$x_{}$  ".format(origin_name), loc="right", fontsize=22)

        xcolor = self.colormap[1]
        self.ax.spines["bottom"].set_color(xcolor)
        self.ax.spines["bottom"].set_linewidth(3)
        # Add arrowhead to x-axis
        self.ax.plot(xlim[1], ylim[0], ">", ms=16, color=xcolor, clip_on=False)

        # Set up y-axis
        self.ax.set_ylim(ylim)
        self.ax.set_yticks([])
        self.ax.set_ylabel(r"$y_{}$  ".format(origin_name), loc="top", rotation="horizontal", fontsize=22)

        ycolor = self.colormap[0]
        self.ax.spines["left"].set_color(ycolor)
        self.ax.spines["left"].set_linewidth(3)
        # Add arrowhead to y-axis
        self.ax.plot(xlim[0], ylim[1], "^", ms=16, color=ycolor, clip_on=False)

        # Plot origin
        self.ax.plot(0, 0, 'ko', zorder=1000, clip_on=False)
        self.ax.text(-1 * 0.04 * xlim[1], -1 * 0.04 * ylim[1], r"$O_{}$".format(origin_name), fontsize=22)

    def print_offset(self, limits):
        (lower, upper) = limits
        return self.text_offset_scale * (upper - lower)

    def add_labeled_point(self, x, y, label):
        self.ax.plot(x, y, 'ko')
        self.ax.text(x + self.print_offset(self.ax.get_xlim()),
                     y + self.print_offset(self.ax.get_ylim()),
                     f"${label}: ({x}, {y})$", fontsize=18)

    def add_grid_lines_for_point(self, x, y):
        self.ax.plot([0, x], [y, y], '--', lw=1.0, color="black", alpha=0.3)
        self.ax.plot([x, x], [0, y], '--', lw=1.0, color="black", alpha=0.3)

    def add_coordinate_frame(self, label, rotation, translation, scale, colors, label_origin=True):
        (x, y) = translation
        rot_rad = rotation * np.pi / 180
        R = np.array([[np.cos(rot_rad), -np.sin(rot_rad)],
                      [np.sin(rot_rad),  np.cos(rot_rad)]])

        (xx, xy) = scale * R @ np.array([1, 0])
        (yx, yy) = scale * R @ np.array([0, 1])

        self.ax.arrow(x, y, xx, xy, width=0.3, color=colors[0])
        self.ax.arrow(x, y, yx, yy, width=0.3, color=colors[1])

        self.ax.plot(x, y, 'ko', zorder=1000, clip_on=False)
        if label_origin:
            self.ax.text(x - self.print_offset(self.ax.get_xlim()),
                         y - self.print_offset(self.ax.get_ylim()),
                         r"$O_{}$".format(label),
                         fontsize=22)

        self.ax.text(x + xx + self.print_offset(self.ax.get_xlim()) / 2,
                     y + xy,
                     r"$x_{}$".format(label),
                     fontsize=16)
        self.ax.text(x + yx,
                     y + yy + self.print_offset(self.ax.get_ylim()) / 2,
                     r"$y_{}$".format(label),
                     fontsize=16)

    def show(self):
        self.fig.show()

def cartesian_grid():
    plot = WorldFramePlotter("Points on a Cartesian grid", " ", (0, 5), (0, 5), 0.04)
    plot.add_labeled_point(2, 2, "p")
    plot.add_grid_lines_for_point(2, 2)

    plot.add_labeled_point(3, 4, "q")
    plot.add_grid_lines_for_point(3, 4)

    plot.add_labeled_point(4, 1, "r")
    plot.add_grid_lines_for_point(4, 1)

    plot.show()

def world_frame_1():
    plot = WorldFramePlotter("World frame with constituent local frames", "W", (0, 100), (0, 100), 0.04)
    frame1_colors = (plot.colormap[3], plot.colormap[2])
    plot.add_coordinate_frame("A", 40, (25, 65), 20, frame1_colors)

    frame2_colors = (plot.colormap[5], plot.colormap[4])
    plot.add_coordinate_frame("B", -30, (73, 32), 5, frame2_colors)

    plot.add_labeled_point(60, 70, "p_W")

    plot.show()

def world_frame_translation():
    plot = WorldFramePlotter("Translation between coordinate frames A and B",
            "W", (0, 100), (0, 100), 0.04)

    frame1_colors = (plot.colormap[3], plot.colormap[2])
    origin_A = np.array((25, 65))
    plot.add_coordinate_frame("A", 0, origin_A, 10, frame1_colors)

    frame2_colors = (plot.colormap[5], plot.colormap[4])
    origin_B = np.array((73, 32))
    plot.add_coordinate_frame("B", 0, origin_B, 10, frame2_colors)

    coords = np.array([origin_A, origin_B])

    (dx, dy) = origin_B - origin_A

    plot.ax.arrow(
            origin_A[0],
            origin_A[1],
            dx - 2,
            dy + 1,
            ls=(0, (10, 10)),
            lw=0.5,
            head_width=2,
            head_length=2,
            color="black",
            alpha=0.4)

    midpoint = coords.mean(axis=0)
    offset = plot.print_offset(plot.ax.get_ylim())

    plot.ax.text(midpoint[0], midpoint[1] + offset, r"$T^B_A$", alpha=0.4, fontsize=22)

    plot.show()

def world_frame_rotation():
    plot = WorldFramePlotter("Rotation between coordinate frames A and B",
            "W", (0, 100), (0, 100), 0.04)

    frame1_colors = (plot.colormap[3], plot.colormap[2])
    origin = np.array((50, 50))
    plot.add_coordinate_frame("A", 0, origin, 20, frame1_colors)

    frame2_colors = (plot.colormap[5], plot.colormap[4])
    plot.add_coordinate_frame("B", 33, origin, 20, frame2_colors, False)

    arcx = mpatches.Arc(origin, 25, 25, theta2 = 33, ls=(0, (5, 5)), alpha=0.4)
    plot.ax.add_patch(arcx)

    arcy = mpatches.Arc(origin, 25, 25, theta1 = 90, theta2 = 123, ls=(0, (5, 5)), alpha=0.4)
    plot.ax.add_patch(arcy)

    plot.ax.text(63, 53, r"$\theta$", fontsize=18, alpha=0.4)
    plot.ax.text(45, 63, r"$\theta$", fontsize=18, alpha=0.4)

    print_offset = plot.print_offset(plot.ax.get_xlim())
    plot.ax.text(origin[0] - print_offset,
                 origin[1] - 2.5 * print_offset,
                 r"$O_B$",
                 fontsize=22)

    plot.show()

def world_frame_scale():
    plot = WorldFramePlotter("Scale between coordinate frames A and B",
            "W", (0, 100), (0, 100), 0.04)

    frame1_colors = (plot.colormap[3], plot.colormap[2])
    origin1 = np.array((30, 50))
    plot.add_coordinate_frame("A", 0, origin1, 20, frame1_colors)

    frame2_colors = (plot.colormap[5], plot.colormap[4])
    origin2 = np.array((70, 50))
    plot.add_coordinate_frame("B", 0, origin2, 4, frame2_colors)

    plot.show()

def transform_as_separate_operations(sx, sy, theta, tx, ty, x_A, y_A):
    """
    Transforms a point (x, y) by the translation (tx, ty), rotation (theta) and
    scale (sx, sy) factors, by formulating the transformation according to:

    S = [[sx  0]
         [ 0 sy]]

    R = [[cos(theta) -sin(theta)]
         [sin(theta)  cos(theta)]]

    T = [tx ty]

    Inputs:

    sx, sy - Scale factors for the x and y axes, respectively
    theta  - Rotation (counter-clockwise positive) in degrees between the two
             coordinate frames.
    tx, ty - Translation along x and y axes, respectively
    x, y   - Point coordinates to be transformed

    Returns:

    A tuple (x_B, y_B) representing the transformed point
    """
    scale = np.array([[sx, 0],
                      [0, sy]])


    theta_in_radians = theta / 180 * np.pi
    rotation = np.array([[np.cos(theta_in_radians), -np.sin(theta_in_radians)],
                         [np.sin(theta_in_radians),  np.cos(theta_in_radians)]])

    translation = np.array([tx, ty])

    p_A = np.array([x_A, y_A])

    [x_B, y_B] = scale @ rotation @ p_A + translation

    return (x_B, y_B)

def transform_as_gamma_matrix(sx, sy, theta, tx, ty, x_A, y_A):
    """
    Transforms a point (x, y) by the translation (tx, ty), rotation (theta) and
    scale (sx, sy) factors, by formulating the transformation according to:

    Gamma = [[sx*cos(theta)  -sx*sin(theta)  tx],
             [sy*sin(theta)   sy*sin(theta)  ty],
             [            0               0   1]]

    Inputs:

    sx, sy - Scale factors for the x and y axes, respectively
    theta  - Rotation (counter-clockwise positive) in degrees between the two
             coordinate frames.
    tx, ty - Translation along x and y axes, respectively
    x, y   - Point coordinates to be transformed

    Returns:

    A tuple (x_B, y_B) representing the transformed point
    """
    theta_in_radians = theta / 180 * np.pi

    Gamma = np.array([[sx*np.cos(theta_in_radians),  -sx*np.sin(theta_in_radians),  tx],
                      [sy*np.sin(theta_in_radians),   sy*np.cos(theta_in_radians),  ty],
                      [                          0,                             0,   1]])

    p_A = np.array([x_A, y_A, 1])

    [x_B, y_B, _] = Gamma @ p_A
    return (x_B, y_B)


if __name__ == "__main__":
    cartesian_grid()
    world_frame_1()
    world_frame_translation()
    world_frame_rotation()
    world_frame_scale()
