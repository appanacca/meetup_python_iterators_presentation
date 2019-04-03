from typing import Tuple
import numpy as np
from functools import partial, reduce
from operator import add
from numpy.linalg import norm
import random

from utils import time_it
from iter_stuff import iterate, take


def eucledian_dist(p, q):
    return  sum((p_i - q_i)**2 for p_i, q_i in zip(p, q))

def closest_index(point, cl_centers):
    distances = np.array([eucledian_dist(c, point) for c in cl_centers])
    return np.argmin(distances)

def cluster_mean(points):
    nb = len(points)
    dim = len(points[0])
    sum_points = [sum(point[j] for point in points) for j in range(dim)]
    return [s / nb for s in sum_points]

def new_cl_centers(points, old_cl_centers):
    k = len(old_cl_centers)
    assignment = [closest_index(point, old_cl_centers) for point in points]
    clusters = [[ point for point, c in zip(points, assignment) if c == j ] for j in range(k) ]
    return [cluster_mean(cluster) for cluster in clusters]

def k_meanses(points, k):
    initial_cl_centers = random.sample(list(points), k) # generate the K center
    return iterate(partial(new_cl_centers, points) , initial_cl_centers)



if __name__ == "__main__":

    from sklearn.datasets import make_moons
    import matplotlib
    matplotlib.use('Qt5Agg')
    import matplotlib.pyplot as plt

    X, y = make_moons(n_samples=1000, noise=0.2)

    clu_centers = take(10, k_meanses(X, 2))

    cl_at_10 = clu_centers[0]

    assignment = [closest_index(point, cl_at_10) for point in X]
    y_hat = [[ point for point, c in zip(X, assignment) if c == j ] for j in range(2) ]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(X[:, 0], X[:, 1], s=60, marker='^', c=y_hat)
    ax.set_xlabel('x_1')
    ax.set_ylabel('x_2')
    plt.grid()
    plt.show()