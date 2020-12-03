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
    pos[:, :, 0] = X; pos[:, :, 1] = Y
    rv = multivariate_normal(mu, Sigma)
    return rv.pdf(pos)

def plot_gaussian(X1, Y1, Z1, cmap):
    # Create a surface plot and projected filled contour plot under it.
    fig = plt.figure(figsize=(16,8))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2,2])
    ax = fig.add_subplot(gs[0], projection='3d')
    ax.plot_surface(X1, Y1, Z1, rstride=3, cstride=3, linewidth=1, antialiased=True,
                cmap=cmap)
    max_range = np.array([X1.max()-X1.min(), Y1.max()-Y1.min(), Z1.max()-Z1.min()]).max() / 2.0
    mid_x = (X1.max()+X1.min()) * 0.5
    mid_y = (Y1.max()+Y1.min()) * 0.5
    mid_z = (Z1.max()+Z1.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(0, 0.5)
    ax.view_init(25, 290)

    ax2 = fig.add_subplot(gs[1])
    cset2 = ax2.contourf(X1, Y1, Z1, cmap=cmap)
    ax2.axis('equal')
    ax2.grid('true')
    plt.tight_layout()
    return (ax, ax2)


def add_gaussian(X1, Y1, Z1, ax, ax2, cmap):
    ax.plot_surface(X1, Y1, Z1, rstride=3, cstride=3, linewidth=1, antialiased=True,
                cmap=cmap)
    max_range = np.array([X1.max()-X1.min(), Y1.max()-Y1.min(), Z1.max()-Z1.min()]).max() / 2.0

    mid_x = (X1.max()+X1.min()) * 0.5
    mid_y = (Y1.max()+Y1.min()) * 0.5
    mid_z = (Z1.max()+Z1.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(0, 0.5)
    ax.view_init(25, 290)
    cset2 = ax2.contourf(X1, Y1, Z1, cmap=cmap)
    ax2.axis('equal')
    ax2.grid('true')
    return (ax, ax2)


def colormap(cmap, axis_min, axis_max):
    colormap = cmap(np.arange(cmap.N))
    colormap[:,-1] = np.linspace(0.2, 1.0, cmap.N)
    return ListedColormap(colormap)


def main():

    # Add our plotting space in 2D
    X, Y = np.mgrid[-1:5:.01, -1:5:.01]

    # Mean vector and covariance matrix
    mu = np.array([2.0, 2.0])
    Sigma = np.array([[0.2, 0.0],
                      [0.0, 0.8]])

    # The distribution on the variables X, Y packed into pos.
    Z = multivariate_gaussian(X, Y, mu, Sigma)

    plot_gaussian(X, Y, Z, colormap(pl.cm.Reds, 0.2, 1.0))
    plt.show()

    #Showing variance vs covariance
    Sigma_var = np.array([[0.5, 0.4],
                          [0.1, 0.8]])
    Z_var = multivariate_gaussian(X, Y, mu, Sigma_var)

    # Choose colormap
    plot_gaussian(X, Y, Z_var, colormap(pl.cm.Reds, 0.2, 1.0))
    plt.show()

    delta_t = 0.2
    # ...seems reasonable.

    # Now let's add in our prediction matrix:
    F = np.array([[1.0, delta_t],
                  [0.0,     1.0]])

    # ...and our control matrix:
    B = np.array([[(delta_t**2)/2], [delta_t]])

    u = 2
    # ...pretty fast.

    Q = np.array([[0.2 , 0.2],
                  [0.5,  0.4]])

    mu_pred = np.array([[2.44], [2.4]])
    Sigma_pred = F @ Sigma @ F.T + Q
    Z2 = multivariate_gaussian(X, Y, mu_pred.reshape(2), Sigma_pred)

    (ax, ax2) = plot_gaussian(X, Y, Z, colormap(pl.cm.Reds, 0.3, 0.3))
    (ax, ax2) = add_gaussian(X, Y, Z2, ax, ax2, colormap(pl.cm.Blues, 0.2, 1.0))
    plt.show()

    ##################################

    # Now to derive our updates!

    # We're only taking positional data, so let's use an observation
    # matrix that only selects for position:
    H = np.array([[1.0, 0.0],
                  [0.0, 1.0]])

    # What about our measurements? Let's sketch that out:
    z = np.array([[2.41],
                  [2.395]])

    R_t = np.array([[0.2, 0.0],
                    [0.0, 0.1]])

    # Our Kalman gain with all of this is:
    a = (H @ Sigma_pred)
    b = ((H @ Sigma_pred @ H.T) + R_t)
    K = np.divide(a, b, out=np.zeros_like(a), where=b!=0)

    # and so:
    mu_add = K @ (z - (H @ mu_pred))
    mu_final = (mu_pred + mu_add).reshape((2,-1))
    Sigma_sub = K @ (H @ Sigma_pred)
    Sigma_final = Sigma_pred - Sigma_sub
    print(f"\nmu_add: \n{mu_add}, \nmu_final: \n{mu_final}")
    print(f"\nSigma_sub: \n{Sigma_sub}, \nSigma_final: \n{Sigma_final}")

    Z_final = multivariate_gaussian(X, Y, mu_final.T, Sigma_final)

    (ax, ax2) = plot_gaussian(X, Y, Z2, colormap(pl.cm.Reds, 0.3, 0.3))
    (ax, ax2) = add_gaussian(X, Y, Z_final, ax, ax2, colormap(pl.cm.Blues, 0.2, 1.0))
    plt.show()


if __name__ == "__main__":
    main()
