#!/usr/bin/env python
# coding: utf-8

# # Welcome to Jupyter!

# This repo contains an introduction to [Jupyter](https://jupyter.org) and [IPython](https://ipython.org).
# 
# Outline of some basics:
# 
# * [Notebook Basics](../examples/Notebook/Notebook%20Basics.ipynb)
# * [IPython - beyond plain python](../examples/IPython%20Kernel/Beyond%20Plain%20Python.ipynb)
# * [Markdown Cells](../examples/Notebook/Working%20With%20Markdown%20Cells.ipynb)
# * [Rich Display System](../examples/IPython%20Kernel/Rich%20Output.ipynb)
# * [Custom Display logic](../examples/IPython%20Kernel/Custom%20Display%20Logic.ipynb)
# * [Running a Secure Public Notebook Server](../examples/Notebook/Running%20the%20Notebook%20Server.ipynb#Securing-the-notebook-server)
# * [How Jupyter works](../examples/Notebook/Multiple%20Languages%2C%20Frontends.ipynb) to run code in different languages.

# You can also get this tutorial and run it on your laptop:
# 
#     git clone https://github.com/ipython/ipython-in-depth
# 
# Install IPython and Jupyter:
# 
# with [conda](https://www.anaconda.com/download):
# 
#     conda install ipython jupyter
# 
# with pip:
# 
#     # first, always upgrade pip!
#     pip install --upgrade pip
#     pip install --upgrade ipython jupyter
# 
# Start the notebook in the tutorial directory:
# 
#     cd ipython-in-depth
#     jupyter notebook

# In[144]:


# import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec
import matplotlib.pylab as pl
from matplotlib.colors import ListedColormap
import numpy as np

# Our 2-dimensional distribution will be over variables X and Y
N = 60
X = np.linspace(-1, 5, N)
Y = np.linspace(-1, 5, N)
X, Y = np.meshgrid(X, Y)

# Mean vector and covariance matrix
mu = np.array([2., 2])
Sigma = np.array([[ 0.2 , 0], 
                  [0,  0.8]])

# Pack X and Y into a single 3-dimensional array
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X
pos[:, :, 1] = Y

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

# The distribution on the variables X, Y packed into pos.
Z = multivariate_gaussian(pos, mu, Sigma)

# Choose colormap
cmap = pl.cm.Reds
red_cmap = cmap(np.arange(cmap.N))
red_cmap[:,-1] = np.linspace(0.2, 1.0, cmap.N)
red_cmap = ListedColormap(red_cmap)

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
    
plot_gaussian(X, Y, Z, red_cmap)
plt.show()


# In[172]:


#Showing variance vs covariance 
Sigma_var = np.array([[ 0.5 , 0.4], 
                  [0.1,  0.8]])
Z_var = multivariate_gaussian(pos, mu, Sigma_var)

# Choose colormap
cmap = pl.cm.Reds
red_cmap = cmap(np.arange(cmap.N))
red_cmap[:,-1] = np.linspace(0.2, 1.0, cmap.N)
red_cmap = ListedColormap(red_cmap)
plot_gaussian(X, Y, Z_var, red_cmap)
plt.show()


# In[169]:


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

delta_t = 0.2
# ...seems reasonable.

# Now let's add in our prediction matrix: 
F = np.array([[1 , delta_t], 
              [0,  1]])

# ...and our control matrix:
B = np.array([[(delta_t * delta_t)/2], [delta_t]]) 

u = 2
# ...pretty fast.

Q = np.array([[0.2 , 0.2], 
              [0.5,  0.4]])

mu2 = np.array([2.44, 
                2.4])
Sigma2 = F * Sigma * F.transpose() + Q
Z2 = multivariate_gaussian(pos, mu2, Sigma2)

# Choose colormap
cmap = pl.cm.Reds
red_cmap = cmap(np.arange(cmap.N))
red_cmap[:,-1] = np.linspace(0.3, 0.3, cmap.N)
red_cmap = ListedColormap(red_cmap)

cmap = pl.cm.Blues
blu_cmap = cmap(np.arange(cmap.N))
blu_cmap[:,-1] = np.linspace(0.2, 1.0, cmap.N)
blu_cmap = ListedColormap(blu_cmap)

(ax, ax2) = plot_gaussian(X, Y, Z, red_cmap)
(ax, ax2) = add_gaussian(X, Y, Z2, ax, ax2, blu_cmap)
plt.show()

#################################

# Now to derive our updates!

# We're only taking positional data, so let's use an observation
# matrix that only selects for position:
H = np.array([[1, 0], 
              [0, 0]])

# What about our measurements? Let's sketch that out:
z = np.array([[2.4], 
              [0]])
R_t = np.array([[0.2, 0],
                [0, 0]])

# ...velocity is 0 because we didn't measure it! This will
# work out later on in the math.

# Our Kalman gain with all of this is:
a = (H * Sigma2)
b = ((H * Sigma2 * H.transpose()) + R_t)
K = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
print (K)

# and so:
mu_add = np.matmul(K, (z - np.matmul(H, mu_2)))
print (mu_add)
mu_final = mu_2 + mu_add
print(mu_final)

Sigma_sub = np.matmul(K, np.matmul(H, Sigma2))
Sigma_final = Sigma2 - Sigma_sub
print(Sigma_final)

Z_final = multivariate_gaussian(pos, np.transpose(mu_final), Sigma_final)
Z_final /= 2 * 
(ax, ax2) = plot_gaussian(X, Y, Z2, red_cmap)
(ax, ax2) = add_gaussian(X, Y, Z_final, ax, ax2, blu_cmap)
plt.show()


# In[ ]:




