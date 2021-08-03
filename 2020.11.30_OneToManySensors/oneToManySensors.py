#!/usr/bin/env python
# coding: utf-8

# import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec
import matplotlib.pylab as pl
from matplotlib.colors import ListedColormap
import numpy as np
from scipy.stats import multivariate_normal


def multivariate_gaussian(X, Y, mu, Sigma):
    pos = np.empty(X.shape + (2,))
    pos[:, :, 0] = X
    pos[:, :, 1] = Y
    return multivariate_normal(mu, Sigma).pdf(pos)


def plot_gaussian(X1, Y1, mu, Sigma, cmap):
    # Create a surface plot and projected filled contour plot under it.
    Z1 = multivariate_gaussian(X1, Y1, mu.reshape(2), Sigma)

    fig = plt.figure(figsize=(16, 8))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2, 2])
    ax = fig.add_subplot(gs[0], projection="3d")
    ax.plot_surface(X1, Y1, Z1, rstride=3, cstride=3, linewidth=1, antialiased=True, cmap=cmap)
    max_range = (
        np.array([X1.max() - X1.min(), Y1.max() - Y1.min(), Z1.max() - Z1.min()]).max() / 2.0
    )
    mid_x = (X1.max() + X1.min()) * 0.5
    mid_y = (Y1.max() + Y1.min()) * 0.5
    mid_z = (Z1.max() + Z1.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_xlabel("position")
    ax.set_ylabel("velocity")
    ax.view_init(25, 290)

    ax2 = fig.add_subplot(gs[1])
    cset2 = ax2.contourf(X1, Y1, Z1, cmap=cmap)
    ax2.axis("equal")
    ax2.grid("true")
    ax2.set_xlabel("position")
    ax2.set_ylabel("velocity")
    plt.tight_layout()
    return (ax, ax2)


def add_gaussian(X1, Y1, mu, Sigma, ax, ax2, cmap):
    # Create a surface plot and projected filled contour plot under it.
    Z1 = multivariate_gaussian(X1, Y1, mu.reshape(2), Sigma)

    ax.plot_surface(X1, Y1, Z1, rstride=3, cstride=3, linewidth=1, antialiased=True, cmap=cmap)
    max_range = (
        np.array([X1.max() - X1.min(), Y1.max() - Y1.min(), Z1.max() - Z1.min()]).max() / 2.0
    )

    mid_x = (X1.max() + X1.min()) * 0.5
    mid_y = (Y1.max() + Y1.min()) * 0.5
    mid_z = (Z1.max() + Z1.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.view_init(25, 290)
    cset2 = ax2.contourf(X1, Y1, Z1, cmap=cmap)
    ax2.axis("equal")
    ax2.grid("true")
    return (ax, ax2)


def colormap(cmap, alpha_min, alpha_max):
    colormap = cmap(np.arange(cmap.N))
    colormap[:, -1] = np.linspace(alpha_min, alpha_max, cmap.N)
    return ListedColormap(colormap)


def predict(delta_t, mu, Sigma):
    # Now let's add in our prediction matrix:
    F = np.array([[1.0, delta_t], [0.0, 1.0]])
    # ...and our control matrix:
    B = np.array([[(delta_t ** 2) / 2], [delta_t]])
    u = 2
    Q = np.array([[0.2, 0.0], [0.0, 0.4]])
    mu_pred = F @ mu + B * u
    Sigma_pred = F @ Sigma @ F.T + Q
    return (mu_pred, Sigma_pred)


def main():

    # Add our plotting space in 2D
    X, Y = np.mgrid[-1:8:0.01, -1:8:0.01]

    # Mean vector and covariance matrix
    mu = np.array([[2.0], [2.0]])
    Sigma = np.array([[0.8, 0.0], [0.0, 0.2]])

    plot_gaussian(X, Y, mu, Sigma, colormap(pl.cm.Greens, 0.2, 1.0))

    ##################################
    # Showing variance vs covariance
    Sigma_var = np.array([[0.5, 0.4], [0.1, 0.8]])
    plot_gaussian(X, Y, mu, Sigma_var, colormap(pl.cm.Greens, 0.2, 1.0))

    ##################################
    # Prediction

    (ax, ax2) = plot_gaussian(X, Y, mu, Sigma, colormap(pl.cm.Greens, 0.2, 0.9))
    (mu_pred, Sigma_pred) = predict(1, mu, Sigma)
    (ax, ax2) = add_gaussian(X, Y, mu_pred, Sigma_pred, ax, ax2, colormap(pl.cm.Reds, 0.2, 0.9))

    ##################################
    # Moving predicted states into measurement space

    X, Y = np.mgrid[-1:24:0.3, -1:24:0.03]

    # We're only taking positional data, so let's use an observation
    # matrix that only selects for position:
    H = np.array([[3.28084, 0.0], [0.0, 3.28084]])

    # Here, mu and Sigma in the measurement space are the same
    # However, this might not hold in other cases. Best to graph anyway
    mu_state_meas = H @ mu_pred
    Sigma_state_meas = H @ Sigma_pred @ H.T
    (ax, ax2) = plot_gaussian(X, Y, mu_state_meas, Sigma_state_meas, colormap(pl.cm.Reds, 0.0, 0.9))
    (ax, ax2) = add_gaussian(X, Y, mu_pred, Sigma_pred, ax, ax2, colormap(pl.cm.Reds, 0.0, 0.5))
    delta = mu_state_meas - mu_pred
    ax2.arrow(
        mu_pred[0, 0],
        mu_pred[1, 0],
        delta[0, 0],
        delta[1, 0],
        linestyle="-.",
        length_includes_head=True,
        head_width=1.0,
        head_length=1.0,
        fc="k",
        ec="k",
    )

    ##################################
    # Update - Incorporating measurements

    z = mu_state_meas + np.array([[0.1], [-0.3]])
    R_t = np.array([[3.0, 0.3], [0.0, 1.0]])

    (ax, ax2) = plot_gaussian(X, Y, mu_state_meas, Sigma_state_meas, colormap(pl.cm.Reds, 0.0, 0.9))
    (ax, ax2) = add_gaussian(X, Y, z, R_t, ax, ax2, colormap(pl.cm.YlGnBu, 0.0, 0.9))

    # Our Kalman gain can be expressed as:
    # K = a/b, with a being
    a = H @ Sigma_pred
    # ...and b being
    b = (H @ Sigma_pred @ H.T) + R_t

    # Set up as a linear system, we then get:
    #
    #    b @ K = a
    #
    # ...which we can solve for with
    K = np.linalg.solve(b, a)

    # and so:
    mu_add = K @ (z - (H @ mu_pred))
    mu_final = mu_pred + mu_add

    # Factor out the Sigma_pred from each side, and you get:
    Sigma_fac = np.identity(2) - (K @ H)
    Sigma_final = Sigma_fac @ Sigma_pred

    # This is a tricky step. For some updates, Sigma_final can lose its
    # positive semi-definite property. There are elegant mathematical ways to go around this
    # (see https://en.wikipedia.org/wiki/Kalman_filter#Square_root_form for instance)
    # but we're going to take the easy way out here.
    Sigma_final[Sigma_final < 0] = 0
    print(f"\nmu_add: \n{mu_add},\nmu_pred:\n{mu_pred},\nmu_final: \n{mu_final}")
    print(f"Sigma_pred:\n{Sigma_pred},\nSigma_final: \n{Sigma_final}")

    X, Y = np.mgrid[-1:8:0.01, -1:8:0.01]

    (ax, ax2) = plot_gaussian(X, Y, mu_pred, Sigma_pred, colormap(pl.cm.Reds, 0.2, 0.9))
    (ax, ax2) = add_gaussian(X, Y, mu, Sigma, ax, ax2, colormap(pl.cm.Greens, 0.2, 0.9))
    (ax, ax2) = add_gaussian(X, Y, mu_final, Sigma_final, ax, ax2, colormap(pl.cm.Blues, 0.2, 0.9))
    plt.show()


if __name__ == "__main__":
    main()
