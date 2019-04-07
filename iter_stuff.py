from itertools import count, tee, cycle, accumulate, islice, repeat
from functools import partial
from operator import add

from utils import time_it
import functools
from typing import Any
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import TextIO
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union


@time_it
def lazy_int(n=0):
    while True:
        yield n
        n += 1

xs_functools = count(0, 1)  # its the functools version of the above

xs = lazy_int()

l1 = [next(xs) for _ in range(10)]  

l2 = [next(xs) for _ in range(10)] # the second call still has the state of the first in memory

print(l1, l2)

squares = (x**2 for x in lazy_int())  # squares is a generator -> lazy computation
#squares_list = [x**2 for x in lazy_int()]  # this is a list that would go forever...

ls1 = [next(squares) for _ in range(10)]  
print(ls1)

#  cat log_file.log | grep -i ERROR | wc -l

with open("log_file.log", "r") as f:
    lines = (line for line in f)
    error_line = filter(lambda line: "ERROR" in line.upper(), lines)

    line_count = len(list(error_line)) # list() is used to force an evaluation before closing the file

print(line_count)


# tee(it, n=2)
# cycle(it)
# chain(it1, it2, ...itn)
# accumulate

def take(n, it) -> list:
    return [x for x in islice(it, n)]

def drop(n ,it) -> Iterator:
    return islice(it, n, None)

head = next
tail = partial(drop, 1)

def iterate(f, x) -> Iterator:
    return accumulate(repeat(x), lambda fx, _: f(fx))  # the lambda takes 2 inputs but it only uses the first

def iterate_2(f, x):
    yield x
    yield from iterate_2(f, f(x))

def add1():
    return partial(add, 1)

def lazy_int_2() -> Iterator:
    return iterate(add1, 0)

## all fibonacci examples !!!!
# very very good
# you can couple it with the @timeit decorator
