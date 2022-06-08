from abc import abstractmethod
from typing import Tuple
from PIL import ImageDraw
# Interface for all scalable objects in this project


class Scalable():

    @abstractmethod
    def draw(self, drawer : ImageDraw):
        """
        :param size: (x,y)
        :param drawer: drawer to be used in the draw method. the dawer points to an image already and it can be trusted
        to draw on the right image (client's responsibility).
        """
        pass

    # TODO there should

    @abstractmethod
    def resize(self, scale_factor: Tuple[float,float]):
        """
        :param size: (width scale factor, height scale factor)
        """
        pass

if __name__ == '__main__':
    my_float_1 = 1/1
    my_float_2 = 2/1

    print(my_float_1)
    print(my_float_2)

    my_int_tuple: Tuple[int,int] = (my_float_1,my_float_2)
    my_float_tuple: Tuple[float,float] = (my_float_1,my_float_2)
    print(my_int_tuple)
    print(my_float_tuple)

