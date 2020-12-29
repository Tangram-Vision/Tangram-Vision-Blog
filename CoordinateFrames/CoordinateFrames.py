#!/usr/bin/env python3

import prettyplotlib as ppl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
import numpy as np

def plot_cartesian_axes():
    fig = plt.figure(figsize=(12, 9), edgecolor='r')
    ax = fig.add_subplot()

    ax.set_title("Points on a Cartesian grid")

    ax.set_xlim((0, 5))
    ax.set_ylim((0, 5))

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("blue")
    ax.spines["left"].set_linewidth(3)

    ax.spines["bottom"].set_color("red")
    ax.spines["bottom"].set_linewidth(3)

    ax.plot(5, 0, ">k", clip_on=False)
    ax.plot(0, 5, "^k", clip_on=False)

    ax.plot(2, 2, 'ko')
    ax.text(2.1, 2.1, "p: (2, 2)")

    ax.plot(3, 4, 'ko')
    ax.text(3.1, 4.1, "q: (3, 4)")

    ax.plot(4, 1, 'ko')
    ax.text(4.1, 1.1, "r: (2, 2)")

    ax.plot(0, 0, 'ko', clip_on=False)
    ax.text(-0.2, -0.2, r"$O$")

    fig.show()

if __name__ == "__main__":
    plot_cartesian_axes()
