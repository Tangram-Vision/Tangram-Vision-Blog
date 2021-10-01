## Create demonstration assets around accuracy and precision metrics.
##
## For more on the math used here in calculating error, see
## https://ncss-wpengine.netdna-ssl.com/wp-content/themes/ncss/pdf/Procedures/PASS/Confidence_Intervals_for_Linear_Regression_Slope.pdf

import numpy as np
import math
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import t


def save_plot(plt, filename, ylim):
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Glacial Indifference'
    plt.xlabel("X Inputs")
    plt.ylabel("Y Outputs")
    ax = plt.gca()
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    plt.ylim(ylim)
    plt.savefig(filename, bbox_inches="tight")


def main():
    asset_dir = Path(__file__).parent.resolve()

    # Create the line data.
    rng = np.random.default_rng()
    N = 20
    x = np.linspace(0, 10, N)
    y = 1.2*x + (5 * rng.random(N))

    # Fit a line to the data.
    a, b = np.polyfit(x, y, deg=1)
    y_fit = a * x + b

    # This is calculating the standard error of y at x. This is a small sample
    # size, so we should be taking the t score into account.
    tinv = lambda p, df: abs(t.ppf(p/2, df))
    ts = tinv(0.05, N-2) # as we have two degrees of freedom
    y_err = ts * x.std() * np.sqrt(1/len(x) + (x - x.mean())**2 / np.sum((x - x.mean())**2))
    ylim = [min(y - y_err) - 0.5,  max(y + y_err) + 0.5]

    # Show our points
    plt.plot(x, y, 'o', color="#1A073C", markersize=10)
    save_plot(plt, asset_dir.joinpath('inputs.png'), ylim)

    # Show our line fit
    plt.plot(x, y, 'o', color="#1A073C", markersize=10)
    plt.plot(x, y_fit, color="#C75813", linewidth=5)
    save_plot(plt, asset_dir.joinpath('fit.png'), ylim)

    # Show our points and error bars
    plt.plot(x, y, 'o', color="#1A073C", markersize=10)
    plt.plot(x, y_fit, color="#C75813", linewidth=5)
    plt.errorbar(x, y, y_err, linestyle="none", linewidth=3, color="#8E7D96", capsize=8)
    save_plot(plt, asset_dir.joinpath('error.png'), ylim)

    # Show the line, data, and confidence interval in graph form
    plt.plot(x, y, 'o', color="#1A073C", markersize=10)
    plt.plot(x, y_fit, color="#C75813", linewidth=5)
    plt.errorbar(x, y, y_err, linestyle="none", linewidth=3, color="#8E7D96", capsize=8)
    plt.fill_between(x, y_fit + y_err, y_fit - y_err, color="#F8982E", alpha=0.4)
    save_plot(plt, asset_dir.joinpath('confidence.png'), ylim)


if __name__ == "__main__":
    main()
