from itertools import repeat, accumulate
from typing import Iterator
from more_itertools import iterate
from functools import partial
import numpy as np

def iterate_v1(f, x):
    while True:
        yield x
        x = f(x)

def iterate_v2(f, x):
    yield x
    yield from iterate_v2(f, f(x))

def iterate_v3(f, x) -> Iterator:
    return accumulate(repeat(x), lambda fx, _: f(fx))  # the lambda takes 2 inputs but it only uses the first

iterate_v4 = iterate


def vanilla_jacobi(R, D, b, x):
    """
    https://en.wikipedia.org/wiki/Jacobi_method
    """
    return (b - np.dot(R,x)) / D


if __name__ == "__main__":
    A = np.array([[2.0,1.0],[5.0,7.0]])
    b = np.array([11.0,13.0])
    x = np.array([1.0,1.0])


    D = np.diag(A)
    R = A - np.diagflat(D)

    first_iter = vanilla_jacobi(R, D, b, x)
    print(np.linalg.norm( np.dot(A,first_iter) -b ))


    functional_jacobi = partial(vanilla_jacobi, R, D, b)
    jacobi_algo = iterate_v4(functional_jacobi, x)

    for i in range(30):
        x_sol = next(jacobi_algo)
        residual = np.dot(A, x_sol) -b
        print(np.linalg.norm(residual))