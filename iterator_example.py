from collections.abc import Iterator
import os
import rasterio
import numpy as np
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
            with rasterio.open(self.images[self.n]) as image:
                img = image.read()
                img = np.moveaxis(img, 0, -1)
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

    my_dataset = ImageDataset( os.path.join(os.getcwd(), "images") )

    for img in my_dataset:
        plt.imshow(img)
        plt.show()
