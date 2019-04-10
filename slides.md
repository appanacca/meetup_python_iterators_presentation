---

# Decorators and Iterators in the wild

## Thibault Ducret & Nicola Luminari

<!--
Speakers note to the best presentation ever
-->

---

# Collection-Based loop 
Pas d'initialisation d'index, check des bords ou increment.

```python {style="font-size: 12pt}
for *var* in *iterable*:
    *statement(s)*
```

```python {style="font-size: 12pt}
>>>list_of_stuff = [1, 2, 3, "toto", ("a", 7)]
>>>for item in list_of_stuff:
>>>    print(item)
1
2
3
toto
('a', 7)
```

{.column}

```c++
for(int i = 0; i < N; i++){
    *var* = *iterable*[i]
}
```

---

# Iterator et iterable ? 
Un *iterable* représente n'importe quel objet sur lequel on peut itérer avec un for loop

```python {style="font-size: 10pt}
>>> iter('foobar')                            
<str_iterator object at 0x036E2750>

>>> iter(['foo', 'bar', 'baz'])              
<list_iterator object at 0x036E27D0>

>>> iter(4.2)                                 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'float' object is not iterable

```
Dans ces exemples on passe un *iterable* à la méthode iter() qui nous donne un objet *iterator*.

---

# Get elements out of it

```python {style="font-size: 12pt}
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

# Iteration protocol

Depuis la doc officielle de Python:

The iterator objects themselves are required to support the following two methods, which together form the iterator protocol:

```python {style="font-size: 12pt}
iterator.__iter__()
```
Return the iterator object itself. This is required to allow both containers and iterators to be used with the for and in statements...

```python {style="font-size: 12pt}
iterator.__next__()
```
Return the next item from the container. If there are no further items, raise the StopIteration exception...

---

# Exemple

```python {style="font-size: 10pt}
class ImageDataset(Iterator):
    def __init__(self, photo_directory: str):
        super().__init__()
        self.images = [os.path.join(photo_directory, img_name) for img_name in os.listdir(photo_directory)]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.images):
            img = Image.open(self.images[self.n])
            self.n += 1
            return img
        else:
            raise StopIteration

    def __len__(self):
        return len(self.images)
```

---

# Under the scenes

```python {style="font-size: 10pt}
my_dataset = ImageDataset('cats')
for item in my_dataset:
    plt.imshow(item)
    plt.show()
```

```python {style="font-size: 10pt}
my_dataset = ImageDataset('cats')
iterator = my_dataset.__iter__()
loop_finish = False
while not loop_finish:
    try:
        item = iterator.__next__()
    except StopIteration:
        loop_finish = True
    else:
        plt.imshow(item)
        plt.show()
```

<!--
+ the for loop call the method iter() on the *iterable* object getting an iterator
+ the next() method is called on the iterator getting the *var*
+ repeat next() till _StopIteration_ is raised and exit the for loop
-->

---

# Iterators, pourquoi ? Design pattern

Séparer la structure des données de l'iteration algorithmique 

```python {style="font-size: 12pt}
def reduce(iterable, fun, zero_val):
    res = zero_val
    for item in iterable:
        res = fun(res, item)
    return res
```
{.column}
```python {style="font-size: 12pt}
my_int_list = [1, 2, 3]
res = reduce(my_int_list, add, 10)
>> 16

my_iterable_string = "chat !"
res = reduce(my_iterable_string, add, "J'aime le ")
>> "J'aime le chat!"
```

---

# Mommy I am __lazy__ !

```python {style="font-size: 11pt}
# 10 int en mémoire et 5 sec d'attente
def compute():
    rv = []
    for i in range(10):
        sleep(.5)
        rv.append(i)
    return rv

results = compute()
```
{.column}

```python {style="font-size: 11pt}
# version lazy iterator 
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

algo = Compute()
for i in algo:
    res = i  # do something with it
```

---

# Generators 

```python {style="font-size: 10pt}
# un meilleur moyen de définir un lazy iterator
def compute():
    for i in range(10):
        sleep(.5)
        yield i

algo = compute()
for i in compute:
    res = i  # do something with it
```

{.column}

```python {style="font-size: 10pt}
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

algo = Compute()
for i in algo:
    res = i  # do something with it
```




---
# Class design exemple

```python {style="font-size: 10pt}
# the tree methods are separated because the user is supposed to do something else between the 3 calls
class MyGoodInterface:
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


```python {style="font-size: 10pt}
# this generator implementation garantee you that the sequence of the functions calls are the correct ones 
def my_good_interface():
    first_computation()
    yield
    second_computation()
    yield
    third_computation()
    yield
```

---
# Generator expressions et "X" comprehensions

```python {style="font-size: 10pt}
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
# Comprehensions mal-usage

Ne l'utilisez pas seulement pour ses effets secondaires
```python {style="font-size: 12pt}
[print(x) for x in sequence]
```

"intelligence" non trivial
```python {style="font-size: 10pt}
matrix = [[row * 3 + incr for incr in range(1, 4)] for row in range(4)]
matrix_better = np.arange(12).reshape((4,3))
```

:heart: [mauvais usages exemples](https://treyhunner.com/2019/03/abusing-and-overusing-list-comprehensions-in-python/)

---
# Builtin iterators

__map__, __filter__, __enumerate__, __zip__, __sorted__

```python {style="font-size: 10pt}

my_list = [1,2,3]

my_mapped = map(lambda i: i**2, my_list) # square

my_mapped_v2 = (i**2 for i in my_list)

my_filtered = filter(lambda i: bool(i%2) , my_list) # filter out even numbers

my_filtered_v2 = (i for i in my_list if bool(i%2))

for j, item in enumerate([1,2,5]):
    print("The {}th item contains: {}".format(j, item))

my_tuple = ("bob", "alice", " toto")
for item_l, item_t in zip(my_list, my_tuple):  # zip_longest
    ...
```

--- 
# Itertools

"The  module  itertools  is  a  collection  of  very  powerful and  care‐fully  designed functions  for  performing  iterator  algebra." 

+ [itertools](https://docs.python.org/3.6/library/itertools.html)
+ [more-itertools](https://github.com/erikrose/more-itertools)
+ [toolz](https://toolz.readthedocs.io/en/latest/#)

---
# Code examples 

[slides examples](https://repl.it/@appanacca/general-iterators)

[fibonacci](https://repl.it/@appanacca/fibonacciiterators)

[jacobi](https://repl.it/@appanacca/jacobiexample)

[lazy_dataset](https://repl.it/@appanacca/imagedataset)

---
# Pour devenir un pro !

+ https://python-patterns.guide/gang-of-four/iterator/

+ https://realpython.com/python-for-loop/#the-python-for-loop

+ https://dbader.org/blog/python-iterators

+ https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Iterators.html

+ https://www.pythonmorsels.com/resources/

+ https://github.com/kachayev/fn.py

+ https://github.com/joelgrus/stupid-itertools-tricks-pydata/blob/master/README.md