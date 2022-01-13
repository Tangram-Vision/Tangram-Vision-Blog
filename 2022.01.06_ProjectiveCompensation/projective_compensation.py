#!/usr/bin/env python3

import brewer2mpl as b2m
import matplotlib.pyplot as plt
import numpy as np


# Colour map used to define plot colours
colormap = b2m.get_map("Dark2", "qualitative", 8).mpl_colors

# Marker size to use (for scaling the points to a sane size)
marker_size = 20

# Font size to use for scaling text on the figures
font_size = 25


def new_axes():
    fig = plt.figure(figsize=(9, 9))
    fig.clear()

    ax = fig.add_subplot()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.axis("equal")

    return (fig, ax)


def initial_problem():
    (fig, ax) = new_axes()

    ax.plot([5, 6.13], [0, 0], "k-", linewidth=3)
    ax.plot([6.13, 8], [0, 0], "k-", linewidth=3)

    ax.plot(5, 0, "^", color=colormap[0], ms=marker_size)
    ax.plot(8, 0, "^", color=colormap[0], ms=marker_size)

    ax.plot(6.13, 0, "o", color=colormap[2], ms=marker_size)

    ax.text(4.8, -0.25, r"$(5, 0)$", fontsize=font_size)
    ax.text(7.8, -0.25, r"$(8, 0)$", fontsize=font_size)
    ax.text(6, -0.25, r"$(x, 0)$", fontsize=font_size)

    ax.text(5.4, 0.15, r"$d_1$", fontsize=font_size)
    ax.text(7, 0.15, r"$d_2$", fontsize=font_size)

    fig.show()


def problem_with_error():
    (fig, ax) = new_axes()

    ax.plot([5, 6.13], [0, 0], "k-", linewidth=3)
    ax.plot([6.13, 8], [0, 0.0], "k--", linewidth=3, alpha=0.7)
    ax.plot([6.22, 8], [0, 0.6], "k-", linewidth=3)

    ax.plot(5, 0, "^", color=colormap[0], ms=marker_size)
    ax.plot(8, 0, "k^", ms=marker_size, alpha=0.7)
    ax.plot(8, 0.6, "^", color=colormap[0], ms=marker_size)

    ax.plot(6.13, 0, "o", color=colormap[3], ms=marker_size)
    ax.plot(6.22, 0, "o", color=colormap[2], ms=marker_size)

    ax.text(4.8, -0.25, r"$(5, 0)$", fontsize=font_size)
    ax.text(7.8, -0.25, r"$(8, 0)$", fontsize=font_size)
    ax.text(7.8, 0.75, r"$(8, 0.6)$", fontsize=font_size)

    ax.text(5.4, 0.15, r"$d_1$", fontsize=font_size)
    ax.text(7, 0.4, r"$d_2$", fontsize=font_size)

    fig.show()


def problem_with_extra_observations():
    (fig, ax) = new_axes()

    ax.plot([5, 6.13], [0, 0], "k-", linewidth=3)
    ax.plot([6.22, 8], [0, 0.6], "k-", linewidth=3)
    ax.plot([5.5, 6.13], [1.2, 0], "k-", linewidth=3)
    ax.plot([6.13, 6.13], [-1, 0], "k-", linewidth=3)

    ax.plot(5, 0, "^", color=colormap[0], ms=marker_size)
    ax.plot(8, 0.6, "^", color=colormap[0], ms=marker_size)
    ax.plot(5.5, 1.2, "^", color=colormap[0], ms=marker_size)
    ax.plot(6.13, -1, "^", color=colormap[0], ms=marker_size)

    ax.plot(6.13, 0, "o", color=colormap[3], ms=marker_size)
    ax.plot(6.22, 0, "o", color=colormap[2], ms=marker_size)

    ax.text(4.8, -0.25, r"$(5, 0)$", fontsize=font_size)
    ax.text(7.8, 0.75, r"$(8, 0.6)$", fontsize=font_size)
    ax.text(5, 1.4, r"$(5.5, 1.2)$", fontsize=font_size)
    ax.text(5.3, -1.4, r"$(6.13, -1)$", fontsize=font_size)

    ax.text(5.4, 0.15, r"$d_1$", fontsize=font_size)
    ax.text(7, 0.4, r"$d_2$", fontsize=font_size)
    ax.text(5.85, 0.6, r"$d_3$", fontsize=font_size)
    ax.text(6.2, -0.5, r"$d_4$", fontsize=font_size)

    fig.show()


def least_squares_solution_to_problem(d, ps, x_initial):
    """
    Sets up the least squares problem described by the figures.

    The problem is fundamentally a trilateration problem, so we can say that our base model is:

        d = norm_2(q)

    or in plain English: the distance measured is equal to the 2-norm between points q and p, for
    any two points q and p. Our functional model is only solving for x so we have only set `norm_2`
    to vary according to the `x` coordinate.

    This produces a Jacobian of the form:

        J = [ d/dx (norm_2) ]

    and a gradient of the form:

        G = [ norm_2(x_initial) - d ]

    From there, we can use the Jacobian and Gradient to perform a linear least-squares solution to
    our problem.

    @param d - an array of all observations.
    @param ps - an array of all the points that have observations to our point `q`. Must be the same
           length as `d`
    @param x_initial - the initial x coordinate of point `q` to use as the seed for the
           least-squares adjustment.

    @returns (x, r) - the x coordinate of q, and the residual vector sharing the same length as `d`
             for each observation
    """
    q_initial = (x_initial, 0)
    j = ((ps[:, 0] - x_initial) / np.linalg.norm(ps - q_initial, axis=1)).reshape((-1, 1))
    g = np.linalg.norm(ps - q_initial, axis=1) - d

    N = j.T @ j
    U = j.T @ g

    delta = np.linalg.solve(-N, U)
    x = x_initial - delta
    r = j @ delta + g

    return (x, r)


if __name__ == "__main__":
    initial_problem()
    problem_with_error()
    problem_with_extra_observations()

    ## Problem 1:
    d = np.array([1.12, 1.86])
    ps = np.array([(5, 0), (8, 0)])
    x_initial = 6

    (x, r) = least_squares_solution_to_problem(d, ps, x_initial)

    print(f"x: {x}")
    print(f"r: {r}")
    print()

    ## Problem 2 -- Problem 1 but with error in second point
    d = np.array([1.12, 1.86])
    ps = np.array([(5, 0), (8, 0.6)])
    x_initial = 6

    (x, r) = least_squares_solution_to_problem(d, ps, x_initial)

    print(f"x: {x}")
    print(f"r: {r}")
    print()

    ## Problem 3 -- Problem 2 but we add two more points & observations
    d = np.array([1.12, 1.86, 1.36, 1.02])
    ps = np.array([(5, 0), (8, 0.6), (5.5, 1.2), (6.13, -1)])
    x_initial = 6

    (x, r) = least_squares_solution_to_problem(d, ps, x_initial)

    print(f"x: {x}")
    print(f"r: {r}")
    print()
