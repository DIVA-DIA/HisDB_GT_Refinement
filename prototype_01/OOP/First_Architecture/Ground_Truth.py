# This class will store the image of the final GTs
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw

class Ground_truth:

    @abstractmethod
    def __init__(self, img: Image):
        self.img = img

    @abstractmethod
    def display_GT(self):
        pass

class GIF_Ground_Truth(Ground_truth):

    def __init__(self, img: Image):
        super().__init__(img)

class PAGE_Ground_Truth(Ground_truth):

    def display_GT(self):
        pass
