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

def multivariate_gaussian(pos, mu, Sigma):
    """Return the multivariate Gaussian distribution on array pos.

    pos is an array constructed by packing the meshed arrays of variables
    x_1, x_2, x_3, ..., x_k into its _last_ dimension.
    """
    n = mu.shape[0]
    Sigma_det = np.linalg.det(Sigma)
    Sigma_inv = np.linalg.inv(Sigma)
    N = np.sqrt((2*np.pi)**n * Sigma_det)
    # This einsum call calculates (x-mu)T.Sigma-1.(x-mu) in a vectorized
    # way across all the input variables.
    fac = np.einsum('...k,kl,...l->...', pos-mu, Sigma_inv, pos-mu)

    return np.exp(-fac / 2) / N


def plot_gaussian(X1, Y1, Z1, cmap):
    # Create a surface plot and projected filled contour plot under it.
    fig = plt.figure(figsize=(16,8))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2,2])
    ax = plt.subplot(gs[0], projection='3d')
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

    ax2 = plt.subplot(gs[1])
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
    # Our 2-dimensional distribution will be over variables X and Y
    N = 60
    X = np.linspace(-1, 5, N)
    Y = np.linspace(-1, 5, N)
    X, Y = np.meshgrid(X, Y)

    # Mean vector and covariance matrix
    mu = np.array([2.0, 2.0])
    Sigma = np.array([[0.2, 0.0],
                      [0.0, 0.8]])

    # Pack X and Y into a single 3-dimensional array
    pos = np.empty(X.shape + (2,))
    pos[:, :, 0] = X
    pos[:, :, 1] = Y

    # The distribution on the variables X, Y packed into pos.
    Z = multivariate_gaussian(pos, mu, Sigma)

    plot_gaussian(X, Y, Z, colormap(pl.cm.Reds, 0.2, 1.0))
    plt.show()

    #Showing variance vs covariance
    Sigma_var = np.array([[0.5, 0.4],
                          [0.1, 0.8]])
    Z_var = multivariate_gaussian(pos, mu, Sigma_var)

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
    Z2 = multivariate_gaussian(pos, mu_pred.reshape(2), Sigma_pred)

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
    z = np.array([[2.4],
                  [0.0]])

    R_t = np.array([[0.2, 0.0],
                    [0.0, 0.0]])

    # ...velocity is 0 because we didn't measure it! This will
    # work out later on in the math.

    # Our Kalman gain with all of this is:
    a = (H @ Sigma_pred)
    b = ((H @ Sigma_pred @ H.T) + R_t)
    K = np.divide(a, b, out=np.zeros_like(a), where=b!=0)

    # and so:
    mu_add = K @ (z - (H @ mu_pred))
    mu_final = (mu_pred + mu_add).reshape((2,-1))
    Sigma_sub = K @ (H @ Sigma_pred)
    Sigma_final = Sigma_pred - Sigma_sub

    Z_final = multivariate_gaussian(pos, mu_final.T, Sigma_final)

    (ax, ax2) = plot_gaussian(X, Y, Z2, colormap(pl.cm.Reds, 0.3, 0.3))
    (ax, ax2) = add_gaussian(X, Y, Z_final, ax, ax2, colormap(pl.cm.Blues, 0.2, 1.0))
    plt.show()

if __name__ == "__main__":
    main()
