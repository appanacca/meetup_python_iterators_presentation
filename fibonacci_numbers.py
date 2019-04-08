from more_itertools import take, tail, iterate
from itertools import tee
from toolz import drop
from operator import add

# [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

def fib_v1():
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a + b


def fib_v2(n):
    if n == 0: return 1
    if n == 1: return 1
    return fib_v2(n-1) + fib_v2(n-2)


def fib_v3():
    yield 1
    yield 1
    fibs1, fibs2 = tee(fib_v3(), 2)
    yield from map(add, fib_v3(), drop(1, fib_v3()))


def next_fib(pair):
    x, y = pair
    return (y, x + y)

def fib_v4():
    return (y for x, y in iterate(next_fib, (0, 1)))


if __name__ == "__main__":
    
    N = 20
    
    seq = take(N, fib_v1())

    print(seq)

    seq_2 = [fib_v2(i) for i in range(N)]

    print(seq_2)

    seq = take(N, fib_v3())

    print(seq)

    seq = take(N, fib_v4())

    print(seq)