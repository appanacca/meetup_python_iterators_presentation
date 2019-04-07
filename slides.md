---

# Decortors and Iterators in the wild

## Thibault Ducret & Nicola Luminari

<!--
Speakers note to the best presentation ever
-->

---

# Collection-Based for loop 
we are python coders tell you C buddies to get lost !! 



```python {style="font-size: 11pt}
for *var* in *iterable*:
    *statement(s)*
```

```python {style="font-size: 11pt}
list_of_stuff = [1, 2, 3, "toto", ("a", 7)]
for item in list_of_stuff:
    print(item)
```

{.column}

```c++
for(int i = 0; i < N; i++){
    *var* = *iterable*[i]
}
```

---

# What is an iterable ? interact with him
An object that can be used in an iteration... umhh
An object that can be passed to the iter()... are you kidding me !?


```python {style="font-size: 11pt}
>>> iter('foobar')                            
<str_iterator object at 0x036E2750>

>>> iter(['foo', 'bar', 'baz'])              
<list_iterator object at 0x036E27D0>

>>> iter(('foo', 'bar', 'baz'))               
<tuple_iterator object at 0x036E27F0>

>>> iter(4.2)                                 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'float' object is not iterable

```

In the axample aboves we pass an *iterable* to the iter() mlethod and we get an *iterator* object

---

# Get elements out of it

```python {style="font-size: 11pt}
>>> it = iter(['what', 'a', 'great', 'meetup' ])
>>> it
<list_iterator object at 0x7f7894892ef0>
>>> next(it)
'what'
>>> next(it)
'a'
>>> next(it)
'great'
>>> next(it)
'meetup'
>>> next(it)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

```

---
# What is an iterator ?



---

# Iteration protocol



---

# Example
iter() should retourn an iterator that an be the object itself

```python {style="font-size: 11pt}
class ImageDataset:
    def __init__(self, photo_directory: str):
        self.images = [os.path.join(photo_directory, img_name) for img_name in os.listdir(photo_directory)] 

    def __iter__(self):
         self.n = 0
        return self
    
    def __next__(self):
        if self.n <= len(self.images):
            img = cv.imread(self.images[self.n], 0)
            self.n += 1
            return img
        else:
            raise StopIteration

    def __len__(self):
        return len(self.images)
```

---

# Under the scenes

```python {style="font-size: 11pt}
my_dataset = ImageDatset('~/Documents/cats')
for item in my_dataset:
    plt.imshow(item)
    plt.show()
```


```python {style="font-size: 11pt}
my_dataset = ImageDatset('~/Documents/cats')
iterator = my_dataset.__iter__()
while True:
    item = iterator.__next__()
    plt.imshow(item)
    plt.show()
```


+ the for loop call the method iter() on the *iterable* object getting an iterator
+ the next() method is called on the iterator getting the *var*
+ repeat next() till _StopIteration_ and exit the for loop

<!--
How can this idiomatic iteration works 
-->

---

# Why iterators ? Design pattern

Decoupling the data structure iteration from the algorithm

```python {style="font-size: 11pt}
def reduce(iterable, fun, zero_val):
    res = zero_val
    for item in iterable:
        res = fun(res, item)

l = [1, 2, 3]
res = reduce(l, add, 10)
print(res)

s = "world !"
res = reduce(s, add, "Hello ")
print(res)
```

---

# But Mommy I am __lazy__...

```python {style="font-size: 11pt}
# it takes time and 10 int of space in memory
def compute():
    rv = []
    for i in range(10):
        sleep(.5)
        rv.append(i)
    return rv
```
{.column}

```python {style="font-size: 11pt}
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
```

---

# Generators 

```python {style="font-size: 11pt}
# much easier way to define a lazy iterator
def compute():
    for i in range(10):
        sleep(.5)
        yield i
```

---
# Api design example

```python {style="font-size: 11pt}
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

```

{.column}


```python {style="font-size: 11pt}
# this generator implementation garantee you that the sequence of the functions calls are the correct ones 
def api():
    first_computation()
    yield
    second_computation()
    yield
    third_computation()
    yield
```

---
# Generator expressions and "X" comprehensions

Concise syntax to filter some iterator output and/or perform some basic operation


```python {style="font-size: 11pt}
my_list = [1,2,3]

# Generator expression -- returns a generator
squared_gen = (item**2 for item in my_list if item > 2)

def square_gen(data):
    for i in data:
        if i > 2:
            yield i**2


# List comprehension -- returns list
squared_list = [item**2 for item in my_list if item > 2]

s_list = []
for i in my_list:
    if i > 2:
        s_list.append(i**2)
```

---
# Comprehensions mis-usage

Do not use it only for it's side effects:
```python {style="font-size: 11pt}
[print(x) for x in seqeunce]
```

Please check out this blog:
:heart: [links](https://treyhunner.com/2019/03/abusing-and-overusing-list-comprehensions-in-python/)

---
# Builtin iterators

map, filter, enumerate, zip, sorted

```python {style="font-size: 11pt}

my_list = [1,2,3]

m = map(lambda i: i**2, my_list) # square

f= filter(lambda i: bool(i%2) , s) # filter out even numbers

for j, item in [1,2,5]:
    print("The {}th item contains: {}".format(j, item))

my_tuple = ("bob", "alice", " toto")
for item_l, item_t in zip(my_list, my_tuple):
    ...
```

--- 
# Itertools

The  module  itertools  is  a  collection  of  very  powerful—and  care‐fully  designed—functions  for  performing  iterator  algebra. 

[itertools](https://docs.python.org/3.6/library/itertools.html)
[more-itertools](https://github.com/erikrose/more-itertools)
[toolz](https://toolz.readthedocs.io/en/latest/#)

---

things to look at 
+ https://python-patterns.guide/gang-of-four/iterator/

+ https://realpython.com/python-for-loop/#the-python-for-loop

+ https://dbader.org/blog/python-iterators

+ https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Iterators.html

