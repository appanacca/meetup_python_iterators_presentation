from collections.abc import Iterator
import os
import cv2 as cv
import matplotlib.pyplot as plt
from operator import add

class ImageDataset(Iterator):
    def __init__(self, photo_directory: str):
        super().__init__()
        self.images = [os.path.join(photo_directory, img_name) for img_name in os.listdir(photo_directory)] 
    
    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.images):
            img = cv.imread(self.images[self.n], 0)
            self.n += 1
            return img
        else:
            raise StopIteration

    def __len__(self):
        return len(self.images)


def reduce(iterable, fun, zero_val):
    res = zero_val
    for item in iterable:
        res = fun(res, item)
    return res



if __name__ == "__main__":
    l = [1, 2, 3]
    res = reduce(l, add, 10)
    print(res)

    s = "world !"
    res = reduce(s, add, "Hello ")
    print(res)

    my_dataset = ImageDataset( os.path.join(os.getcwd(), "images") )

    """for img in my_dataset:
        plt.imshow(img, cmap=plt.cm.Greys)
        plt.show()
    """
    iterator = my_dataset.__iter__()
    while True:
        item = iterator.__next__()
        plt.imshow(item, cmap=plt.cm.Greys)
        plt.show()