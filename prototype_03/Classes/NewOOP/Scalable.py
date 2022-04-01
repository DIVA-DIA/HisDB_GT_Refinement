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
    def resize(self, size : Tuple):
        """
        :param size: (x,y)
        """
        pass