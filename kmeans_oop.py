from typing import Tuple
import numpy as np
from functools import partial, reduce
from operator import add
from numpy.linalg import norm
import random

from utils import time_it


class KMeans_oop:
    """ Doing k-means clustering in OOP paradigm"""
    def __init__(self, k: int):
        self.k = k
        self.means = [None for _ in range(k)]  # are the cluster centers

    def fit(self, points: np.array, num_iters=20):
        """ find the cluster centers """
        assignments = [None for _ in points]
        self.means = random.sample(list(points), self.k) #np.random.choice(points, self.k)  # select k points as center of the clusters

        for _ in range(num_iters):
            #assign each point to the close cluster center
            for i, point in enumerate(points):
                assignments[i] = self.predict(point)

            # predict the new cluster center
            for j in range(self.k):
                cluster = [p for p, c in zip(points, assignments) if c == j]  # get all the points inside the cluster j
                self.means[j] = list(map(lambda x: x / len(cluster), reduce(partial(map, add), cluster) ))

    def predict(self, point: np.array) -> int:
        """" return index of the closest cluster """
        d_min = np.inf
        for j, m in enumerate(self.means):
            d = sum((m_i- p_i)**2 for m_i, p_i in zip(m, point) )  # the second zip is needed because the point and the mean center can be a vector
            
            prediction = 0
            if d < d_min:
                prediction = j
                d_min = d
        return prediction


if __name__ == "__main__":

    from sklearn.datasets import make_moons
    import matplotlib
    matplotlib.use('Qt5Agg')
    import matplotlib.pyplot as plt

    X, y = make_moons(n_samples=1000, noise=0.2)

    model = KMeans_oop(2)
    model.fit(X)
    y_hat = [model.predict(point) for point in X]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(X[:, 0], X[:, 1], s=60, marker='^', c=y_hat)
    ax.set_xlabel('x_1')
    ax.set_ylabel('x_2')
    plt.grid()
    plt.show()