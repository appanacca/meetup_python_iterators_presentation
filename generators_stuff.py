from time import sleep

class Adder:
    def __call__(self, x, y):
        return x + y

def add(x, y):
    return x + y

# it takes time and 10 int of space in memory
def compute():
    rv = []
    for i in range(10):
        sleep(.5)
        rv.append(i)
    return rv

# lazy iterator class version
class Compute:
    def __init__(self):
        self.value = 0

    def __iter__(self):
        return self

    def __next__(self):
        rv = self.value
        self.value += 1
        if self.value > 10:
            raise StopIteration
        else:
            sleep(.5)
            return rv

# much easier way to define a lazy iterator
def compute_g():
    for i in range(10):
        sleep(.5)
        yield i


# the tree methods are separated because the user is supposed to do something else between the 3 calls
class Api:
    def first_computation(self):
        pass
    def second_computation(self):
        pass
    def third_computation(self):
        pass

    # if the 3 methods could be executed sequentially probably we would have had something like this
    def compute(self):
        self.first_computation()
        self.second_computation()
        self.third_computation()


def first_computation():
    print("first")
    pass
def second_computation():
    print("second")
    pass
def third_computation():
    print("third")
    pass

# this generator implementation garantee you that the sequence of the functions calls are the correct ones 
def api():
    first_computation()
    yield
    second_computation()
    yield
    third_computation()
    yield

if __name__ == "__main__":

    algo = api()

    next(algo)
    
    print("doing some stuff ")
    next(algo)

    next(algo)
