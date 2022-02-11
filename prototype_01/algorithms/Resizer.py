# This class is a naive approach to resizing an image
# The resizing will be possible
# The scaling algorithms could be based on https://stackoverflow.com/questions/48121916/numpy-resize-rescale-image
from PIL import Image, ImageDraw
from abc import abstractmethod
from enum import Enum
import numpy as np
from pathlib import Path


# stores the strategies implemented
class Strategy(Enum):
    MAJORITY_WINS = 0
    MINORITY_WINS = 1
    RANDOM_WINS = 2


# abstract class for the implemented strategies to rescale arrays in general. based on a given Strategy, a smaller (or bigger)
# array is created from the original one.

class ResizingStrategy():

    @abstractmethod
    def __init__(self):
        print("abstract method of ResizingStrategy() was called. has to be implemented.")

    @abstractmethod
    def resize(self, img_as_array, resize_factor):
        print("abstract method of ResizingStrategy() was called. has to be implemented.")


class MajorityWins(ResizingStrategy):

    def __init__(self):
        super().__init__()
        # self.resize_factor = resize_factor

    def resize(self, img_as_array, resize_factor):
        x = 6496 // resize_factor
        y = 4872 // resize_factor
        return img_as_array.reshape((x, resize_factor,
                                     y, resize_factor, 3)).max(3).max(1)

class MinorityWins(ResizingStrategy):

    def __init__(self):
        super().__init__()
        # self.resize_factor = resize_factor

    def resize(self, img_as_array, resize_factor):
        x = 6496 // resize_factor
        y = 4872 // resize_factor
        return img_as_array.reshape((x, resize_factor,
                                     y, resize_factor, 3)).min(3).min(1)



class Resizer():

    @abstractmethod
    def __init__(self, img: Image, strategy: ResizingStrategy):
        self.img: Image = img
        self.strategy: ResizingStrategy = strategy

    @abstractmethod
    def resize(self, scaling_factor):
        print("abstract method of AbstractResizer(). has to be implemented.")


# simple resizer which only allows for resizing to multiples of the original image
class NaiveResizer(Resizer):

    def __init__(self, img: Image, strategy):
        super().__init__(img=img, strategy=strategy)

    def resize(self, scaling_factor):
        img_asarray: np.ndarray = np.asarray(self.img)
        return self.strategy.resize(img_asarray, scaling_factor)


# a class that should resize to custom size (x,y), x and y don't have to be multiples of the original image
class CustomResizer(Resizer):
    pass


if __name__ == '__main__':
    # source_img_path = Path("../../CB55/img/public-test/e-codices_fmb-cb-0055_0098v_max.jpg")
    # source_img = Image.open(source_img_path)
    # print(np.indices((3, 3)))
    # img_asarray = np.asarray(source_img)
    # shape = img_asarray.shape
    # print(shape)
    # print(np.indices((6496, 4872, 3)))
    # print(np.zeros(shape, dtype=int))

    # client code
    source_img_path = Path("../../CB55/img/public-test/e-codices_fmb-cb-0055_0098v_max.jpg")
    source_img = Image.open(source_img_path)
    resizer = NaiveResizer(source_img, MajorityWins())
    img_asarray = resizer.resize(4)
    img = Image.fromarray(img_asarray)
    img.show()
    img.save(Path("../Output/Resizing/resized01_factor_by_4_Majority_wins.jpg"))
    source_img = Image.open(source_img_path)
    resizer = NaiveResizer(source_img, MinorityWins())
    img_asarray = resizer.resize(4)
    img = Image.fromarray(img_asarray)
    img.show()
    img.save(Path("../Output/Resizing/resized01_factor_by_4_minority_wins.jpg"))