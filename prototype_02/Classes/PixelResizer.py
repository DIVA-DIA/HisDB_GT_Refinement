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


class MeanWins(ResizingStrategy):
    # TODO: Implementation for Mean fails, I assume because it outputs floats.
    def __init__(self):
        super().__init__()
        # self.resize_factor = resize_factor

    def resize(self, img_as_array, resize_factor):
        x = 6496 // resize_factor
        y = 4872 // resize_factor

        return img_as_array.reshape((x, resize_factor,
                                     y, resize_factor, 3)).mean(axis=3, dtype=int).mean(axis=1, dtype=int)


class FlexibleResizer(ResizingStrategy):
    # TODO: Finish FlexibleResizer and test it.
    def __init__(self):
        super().__init__()
        pass

    def resize(self, img_as_array, resize_factor):
        pass

    def flexibel_resize(self, im: Image, number_rows: int, number_col: int):
        nR0 = len(im)  # source number of rows
        nC0 = len(im[0])  # source number of columns
        return [[im[int(nR0 * r / number_rows)][int(nC0 * c / number_col)]
                 for c in range(number_col)] for r in range(number_rows)]


# TODO it would be better to have a static resizer object which provides the method "resize()" instead of having
#  to create a new resizing object for every image

class Resizer():

    @abstractmethod
    def __init__(self, img: Image, strategy: ResizingStrategy):
        self.img: Image = img
        self.strategy: ResizingStrategy = strategy

    @abstractmethod
    def resize(self, scaling_factor) -> np.array:
        print("abstract method of AbstractResizer(). has to be implemented.")


# simple resizer which only allows for resizing to multiples of the original image
class NaiveResizer(Resizer):

    def __init__(self, img: Image, strategy):
        super().__init__(img=img, strategy=strategy)

    def resize(self, scaling_factor) -> np.array:
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
    source_img_path = Path("../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0098v_max.png")
    source_img = Image.open(source_img_path)
    resizer = NaiveResizer(source_img, MinorityWins())
    img_asarray = resizer.resize(4)
    img = Image.fromarray(img_asarray)
    img.show()
    #img.save(Path("../Output/Resizing/resized02(pixel_based)_factor_by_8_minority_wins.jpg"))
