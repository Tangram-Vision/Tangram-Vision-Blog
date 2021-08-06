#!/usr/bin/env python3

import brewer2mpl as b2m
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# Settings for grid display
lower = -1
upper = 1
spacing = 8

# X and Y values for our gridspace
coords = np.linspace(lower, upper, spacing)
(xs, ys) = np.meshgrid(coords, coords)

# Colour map used to define plot colours
colormap = b2m.get_map("Dark2", "qualitative", 8).mpl_colors


class DistortionPlotter:
    def __init__(self, mesh_xs, mesh_ys, title):
        self.xs = mesh_xs
        self.ys = mesh_ys

        self.fig = plt.figure(figsize=(9, 9))
        self.ax = self.fig.add_subplot()

        self.ax.plot(xs, ys, "k--")
        self.ax.plot(ys, xs, "k--")

        self.ax.spines["top"].set_visible(False)
        self.ax.spines["left"].set_visible(False)

        self.ax.spines["bottom"].set_visible(False)
        self.ax.spines["right"].set_visible(False)

        self.ax.set_title(title, fontsize=25)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.axis("equal")

    def add_distortion(self, distortions, color):
        if distortions["kind"] == "Brown-Conrady":
            k1 = distortions["k1"] if "k1" in distortions else 0.0
            k2 = distortions["k2"] if "k2" in distortions else 0.0

            p1 = distortions["p1"] if "p1" in distortions else 0.0
            p2 = distortions["p2"] if "p2" in distortions else 0.0

            r = self.xs ** 2 + self.ys ** 2

            # We do this here so that we don't accidentally divide by zero if a point at the centre
            # of our grid (i.e. (0, 0)) is part of our mesh grid set of xs and ys.
            dr_over_r = k1 * r ** 2 + k2 * r ** 4

            dxr = self.xs * dr_over_r
            dyr = self.ys * dr_over_r

            dxt = p1 * (self.ys ** 2 + 3 * xs ** 2) + 2 * p2 * xs * ys
            dyt = p2 * (self.xs ** 2 + 3 * ys ** 2) + 2 * p1 * xs * ys

            distorted_xs = self.xs - dxr - dxt
            distorted_ys = self.ys - dyr - dyt

            self.ax.plot(distorted_xs, distorted_ys, "-", color=color)
            self.ax.plot(distorted_ys, distorted_xs, "-", color=color)
        elif distortions["kind"] == "Kannala-Brandt":
            # We only currently support the symmetric radial components of Kannala-Brandt
            #
            # The other terms are straightforward to add, but coming up with useful examples for the
            # numbers to display can be difficult.
            f = distortions["f"] if "f" in distortions else 1.0
            k1 = distortions["k1"] if "k1" in distortions else 0.0
            k2 = distortions["k2"] if "k2" in distortions else 0.0
            k3 = distortions["k3"] if "k3" in distortions else 0.0
            k4 = distortions["k4"] if "k4" in distortions else 0.0

            r = self.xs ** 2 + self.ys ** 2

            theta = np.arctan(r / f)

            dr = k1 * theta + k2 * theta ** 3 + k3 * theta ** 5 + k4 * theta ** 7

            # If the radius is less than 1e-9 (some epsilon) we can say it is zero, so we just set
            # that to 1.0 to avoid dividing by zero in the subsequent computation for dxr and dyr
            #
            # This won't affect the math because if r ~= 0 then x and y will be both zero
            r[r.abs() < 1e-9] = 1.0

            dxr = self.xs / r * dr
            dyr = self.ys / r * dr

            distorted_xs = self.xs - dxr
            distorted_ys = self.ys - dyr

            self.ax.plot(distorted_xs, distorted_ys, "-", color=color)
            self.ax.plot(distorted_ys, distorted_xs, "-", color=color)
        else:
            raise NotImplementedError(
                f"This script does not support the \"{distortions['kind']}\" model."
            )

        self.ax.axis("equal")
        pass

    def show(self):
        self.fig.show()


def no_distortion():
    plot = DistortionPlotter(xs, ys, "No Distortion")
    plot.show()


def barrel_radial_distortion():
    plot = DistortionPlotter(xs, ys, "Barrel Radial Distortion")
    distortions = {
        "kind": "Brown-Conrady",
        "k1": 4.9565e-2,
        "k2": 1.213e-5,
    }
    plot.add_distortion(distortions, colormap[0])
    plot.show()


def pincushion_radial_distortion():
    plot = DistortionPlotter(xs, ys, "Pincushion Radial Distortion")
    distortions = {
        "kind": "Brown-Conrady",
        "k1": -4.9565e-2,
        "k2": -1.213e-5,
    }
    plot.add_distortion(distortions, colormap[0])
    plot.show()


def tangential_distortion():
    plot = DistortionPlotter(xs, ys, "Tangential (Decentering) Distortion")
    distortions = {
        "kind": "Brown-Conrady",
        "p1": 2.2e-2,
        "p2": 2.05e-2,
    }
    plot.add_distortion(distortions, colormap[1])
    plot.show()


def compound_distortion():
    plot = DistortionPlotter(xs, ys, "Compound Distortion")
    distortions = {
        "kind": "Brown-Conrady",
        "k1": 4.9565e-2,
        "k2": -3.213e-4,
        "p1": 2.2e-2,
        "p2": 2.05e-2,
    }
    plot.add_distortion(distortions, colormap[2])
    plot.show()


def radial_effect():
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_linewidth(4)
    ax.spines["bottom"].set_linewidth(4)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_xlim([0, 8])
    ax.set_ylim([0, 8])

    ax.set_xlabel("x", fontsize=20)
    ax.set_ylabel("y", fontsize=20)
    ax.set_title("Geometric effect of radial distortion on a point", pad=25, fontsize=25)

    ax.plot(0, 8, "k^", ms=16, clip_on=False)
    ax.plot(8, 0, "k>", ms=16, clip_on=False)

    ax.plot(5, 5, "ko")
    ax.plot([0, 5], [0, 5], "k-", linewidth=2)

    ax.plot(7, 7, "ko")
    ax.plot([5, 7], [5, 7], "--", color=colormap[0], linewidth=2)

    ax.plot([5, 7], [5, 5], "k-", color=colormap[1], linewidth=2)
    ax.plot([7, 7], [5, 7], "-", color=colormap[2], linewidth=2)

    ax.text(2.5, 3.5, "r", fontsize=20)
    ax.text(5.5, 6.5, r"$\delta r$", color=colormap[0], fontsize=20)
    ax.text(6.0, 4.5, r"$\delta x_{r}$", color=colormap[1], fontsize=20)
    ax.text(7.25, 6.0, r"$\delta y_{r}$", color=colormap[2], fontsize=20)

    arc = mpatches.Arc([0, 0], 3.5, 3.5, theta2=45, ls=(0, (5, 5)), alpha=0.6, linewidth=2)
    ax.text(2.0, 0.75, r"$\psi$", fontsize=20, alpha=0.6)
    ax.add_patch(arc)

    fig.show()


def gaussian_vs_balanced():
    fig = plt.figure(figsize=(22, 9))
    # Gaussian subplot
    ax_g = fig.add_subplot(121)
    # Balanced subplot
    ax_b = fig.add_subplot(122)

    # Set up Gaussian profile
    ax_g.spines["top"].set_visible(False)
    ax_g.spines["right"].set_visible(False)

    ax_g.spines["left"].set_linewidth(4)
    ax_g.spines["bottom"].set_linewidth(4)

    ax_g.set_xlabel(r"r [pixels]", fontsize=20)
    ax_g.set_ylabel(r"$\delta r_{Gaussian} [pixels]$", fontsize=20)
    ax_g.set_title(r"Gaussian distortion profile", fontsize=25)

    # This data was from a camera with a 14mm sensor, 40um pixel pitch
    pixel_pitch = 0.04
    max_radius = 7 / 2
    (k1, k2, k3) = (-7.6822e-03, -4.3747e-04, 0.0)

    r = np.linspace(0, max_radius, 1000)

    dr_g = k1 * r ** 3 + k2 * r ** 5 + k3 * r ** 7

    ax_g.plot([0, 4 / pixel_pitch], [0, 0], "k--", linewidth=1)
    ax_g.plot(r / pixel_pitch, dr_g / pixel_pitch, color=colormap[0], linewidth=3)
    ax_g.set_xlim([0, (max_radius + 1) / pixel_pitch])

    # Set up Balanced profile
    ax_b.spines["top"].set_visible(False)
    ax_b.spines["right"].set_visible(False)

    ax_b.spines["left"].set_linewidth(4)
    ax_b.spines["bottom"].set_linewidth(4)

    ax_b.set_xlabel(r"r [pixels]", fontsize=20)
    ax_b.set_ylabel(r"$\delta r_{Balanced} [pixels]$", fontsize=20)
    ax_b.set_title("Balanced distortion profile", fontsize=25)

    delta_c_over_c = 1.0
    dr_b = delta_c_over_c * r + ((1 + delta_c_over_c) * dr_g)

    ax_b.plot([0, 4 / pixel_pitch], [0, 0], "k--", linewidth=1)
    ax_b.plot(r / pixel_pitch, dr_b / pixel_pitch, color=colormap[1], linewidth=3)
    ax_b.set_xlim([0, (max_radius + 1) / pixel_pitch])

    (k1b, k2b, k3b) = (1 + delta_c_over_c) * np.array((k1, k2, k3))

    print(k1, k2, k3)
    print(k1b, k2b, k3b)

    fig.show()


def similar_triangle():
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.axis("equal")
    ax.set_title("Re-balancing correction for radial distortion", fontsize=25)

    ax.plot([0, 0], [0, 5], "k-", linewidth=3)
    ax.plot([0, 4], [0, 0], "k-", linewidth=3)
    ax.plot([0, 4], [5, 0], "k-", linewidth=3)
    ax.plot([0, 3], [5, 0], "k-", linewidth=3)
    ax.plot([3, 3], [0, 1.25], "k-", linewidth=3)
    ax.plot([0, 3], [1.25, 1.25], "k-", linewidth=3)

    ax.plot([0.0, 3.0], [-0.5, -0.5], "k-", linewidth=2)
    ax.plot(0.0, -0.5, "k<", linewidth=2)
    ax.plot(2.98, -0.5, "k>", linewidth=2)
    ax.text(1.5, -0.75, r"$r$", fontsize=20)

    ax.plot([3.0, 4.0], [-0.5, -0.5], "k-", linewidth=2)
    ax.plot(3.02, -0.5, "k<", linewidth=2)
    ax.plot(4.0, -0.5, "k>", linewidth=2)
    ax.text(3.35, -0.75, r"$\delta r$", fontsize=20)

    ax.plot([-0.5, -0.5], [0.05, 1.20], "k-", linewidth=2)
    ax.plot(-0.5, 0.05, "kv", linewidth=2)
    ax.plot(-0.5, 1.20, "k^", linewidth=2)
    ax.text(-0.4, 0.5, r"$\Delta f$", fontsize=20)

    ax.plot([-1.0, -1.0], [0.05, 4.95], "k-", linewidth=2)
    ax.plot(-1.0, 0.05, "kv", linewidth=2)
    ax.plot(-1.0, 4.95, "k^", linewidth=2)
    ax.text(-0.9, 2.5, r"$f$", fontsize=20)

    fig.show()


if __name__ == "__main__":
    no_distortion()
    barrel_radial_distortion()
    pincushion_radial_distortion()
    tangential_distortion()
    compound_distortion()
    radial_effect()
    gaussian_vs_balanced()
    similar_triangle()
