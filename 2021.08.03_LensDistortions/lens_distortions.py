#!/usr/bin/env python3

import brewer2mpl as b2m
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


if __name__ == "__main__":
    no_distortion()
    barrel_radial_distortion()
    pincushion_radial_distortion()
    tangential_distortion()
