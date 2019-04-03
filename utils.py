from functools import wraps
from time import time

def time_it(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print('{} has run in {} sec'.format(f.__name__, end-start))
        return result
    return wrapper